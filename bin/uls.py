#!/usr/bin/env python3

# Copyright 2022 Akamai Technologies, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import signal
import threading
import re
import os
import queue


# ULS specific modules
import modules.aka_log as aka_log
import modules.UlsArgsParser as ArgsParser
import modules.UlsOutput as UlsOutput
import modules.UlsInputCli as UlsInputCli
import modules.UlsMonitoring as UlsMonitoring
import modules.UlsTransformation as UlsTransformation
import modules.UlsTools as UlsTools
import uls_config.global_config as uls_config

stopEvent = threading.Event()


def sigterm_handler(signum, frame):
    """
    Upon SIGTERM, we signal any other pending activities
    to stop right away
    """
    aka_log.log.debug(f"SIGTERM ({signum}) detected, setting stopEvent")
    stopEvent.set()


def control_break_handler():
    """
    Upon CTRL + C, we signal any other pending activities
    to stop right away
    """
    aka_log.log.debug("Control+C detected, setting stopEvent")
    stopEvent.set()


def main():

    signal.signal(signal.SIGTERM, sigterm_handler)

    # Load the Argument / ENV Var handler
    uls_args = ArgsParser.init()

    # Load the LOG system
    aka_log.init(uls_args.loglevel, uls_config.__tool_name_short__, jsonlogs=uls_args.jsonlog, logformat=uls_args.logformat, logdatefmt=uls_args.logdatefmt)

    # Determine root directory
    root_path = str(UlsTools.root_path())

    # Check / Create install id
    UlsTools.create_install_id()

    # OUTPUT Version Information
    if uls_args.version:
        UlsTools.uls_version(root_path=root_path)

    # Verify the given core params (at least input and output should be set)
    UlsTools.uls_check_args(uls_args.input, uls_args.output)

    # Avoid confusion alongside "autoresume" (we do this after the input class have initialized to avoid creation of dumb files)
    if uls_args.autoresume and uls_args.starttime:
        aka_log.log.critical(f"Error using --autoresume alongside --starttime. This is too confusing to me. Exiting.")
        sys.exit(1)
    elif uls_args.autoresume:
        autoresume_file = None
        autoresume_lastwrite = 0
        autoresume_data = UlsTools.check_autoresume(input=uls_args.input, feed=uls_args.feed, checkpoint_dir=uls_args.autoresumepath)
        uls_args.starttime = autoresume_data['checkpoint']
        autoresume_file =  autoresume_data['filename']

    # Avoid usage of CLI_DEBUG alongside any other output than raw, as this would lead to insecure data injections
    if uls_args.clidebug and not uls_args.output == "RAW":
        aka_log.log.critical(f"Error: CLI_DEBUG (--clidebug) can only be used with the raw output (for security reasons). Exiting.")
        sys.exit(1)
    else:
        aka_log.log.warning(f"CLIDEBUG has been enabled, beside the loglines, you will also see debug information from the underlying CLI")

    # Check CLI Environment
    UlsTools.uls_check_sys(root_path=root_path, uls_input=uls_args.input)


    # Create & Start monitoring Instance
    my_monitor = UlsMonitoring.UlsMonitoring(stopEvent=stopEvent,
                                             product=uls_args.input,
                                             feed=uls_args.feed,
                                             output=uls_args.output,
                                             prom_enabled=uls_args.prometheus_enabled,
                                             prom_port=uls_args.prometheus_port,
                                             prom_host=uls_args.prometheus_addr,
                                             prom_certfile=uls_args.prometheus_certfile,
                                             prom_keyfile=uls_args.prometheus_keyfile)
    my_monitor.start()

    # Connect to an Input Handler UlsInputCli
    my_input = UlsInputCli.UlsInputCli(product=uls_args.input,
                                       feed=uls_args.feed,
                                       cliformat=uls_args.cliformat,
                                       credentials_file=os.path.expanduser(
                                           uls_args.credentials_file),
                                       credentials_file_section=uls_args.credentials_file_section,
                                       inproxy=uls_args.inproxy,
                                       rawcmd=uls_args.rawcmd,
                                       starttime=uls_args.starttime,
                                       endtime=uls_args.endtime,
                                       root_path=root_path,
                                       cli_debug=uls_args.clidebug)


    # Connect to the selected input UlsOutput
    my_output = UlsOutput.UlsOutput(output_type=uls_args.output,
                                    host=uls_args.host,
                                    port=uls_args.port,
                                    tcpudp_out_format=uls_args.tcpudpformat,
                                    http_out_format=uls_args.httpformat,
                                    http_out_auth_header=uls_args.httpauthheader,
                                    http_out_aggregate_count=uls_args.httpaggregate,
                                    http_url=uls_args.httpurl,
                                    http_insecure=uls_args.httpinsecure,
                                    http_liveness=uls_args.httpliveness,
                                    http_formattype=uls_args.httpformattype,
                                    filehandler=uls_args.filehandler,
                                    filename=uls_args.filename,
                                    filebackupcount=uls_args.filebackupcount,
                                    filemaxbytes=uls_args.filemaxbytes,
                                    filetime=uls_args.filetime,
                                    fileinterval=uls_args.fileinterval,
                                    fileaction=uls_args.fileaction,
                                    stopEvent=stopEvent)


    # Load a Transformation (if selected) UlsTransformation
    my_transformer = UlsTransformation.UlsTransformation(transformation=uls_args.transformation,
                                                         product=uls_args.input,
                                                         feed=uls_args.feed,
                                                         cliformat=uls_args.cliformat,
                                                         transformationpattern=uls_args.transformationpattern)

    filter_escaped = uls_args.filter.replace('"', '\\"') if uls_args.filter else None
    # Prepare the Filter
    if uls_args.filter:
        try:
            aka_log.log.info(f"FILTER pattern has been specified: "
                             f"{filter_escaped} - will only output matches")
            filter_pattern = re.compile(uls_args.filter.encode())
        except Exception as my_error:
            aka_log.log.critical(f"Error in filter pattern {filter_escaped}"
                                 f" (exiting). Error: {my_error}")
            sys.exit(1)
    else:
        filter_pattern = None


    # Now let's handle the data and send input to output

    # Initiate the Input handler
    my_input.proc_create()

    # Append extra vars to the output
    #my_output.ingest_vars_into_output_format(api_hostname=my_input.get_edgerc_hostname())
    my_output.ingest_vars_into_output_format(placeholder='{api_hostname}', replacement=my_input.get_edgerc_hostname())
    my_output.ingest_vars_into_output_format(placeholder='{uls_input}', replacement=uls_args.input)
    my_output.ingest_vars_into_output_format(placeholder='{uls_feed}', replacement=uls_args.feed)
    my_output.ingest_os_vars_into_output_format()


    # Connect the output handler
    my_output.connect()


    # Send CallHome Request, if not opted_out
    UlsTools.callhome(nocallhome_state=uls_args.nocallhome, position="uls_start", input=uls_args.input, feed=uls_args.feed, output=uls_args.output)

    # New ULS/1.5: the input module is ingesting messages
    # into a thread safe queue. The function call will immediately
    # return
    event_q = queue.Queue(uls_args.input_queue_size)
    my_input.ingest(stopEvent, event_q, my_monitor)



    # Now we are back to the main thread to process the message
    while not stopEvent.is_set():
        try:
            input_data = event_q.get(block=True, timeout=0.05)
            if uls_args.debugloglines:
                escaped_data = input_data.rstrip().decode('utf-8').replace('"', '\\"')
                aka_log.log.debug(f"<IN> {escaped_data}")
            for log_line in input_data.splitlines():

                log_line_escaped = log_line.decode('utf-8').replace('"', '\\"')
                # Write checkpoint to the checkpoint file (if autoresume is enabled) (not after transformation or filter)
                if uls_args.autoresume and int(my_monitor.get_message_count()) >= autoresume_lastwrite + uls_args.autoresumewriteafter:
                    aka_log.log.info(f"WRITING AUTORESUME CHECKPOINT - curr_message_count={int(my_monitor.get_message_count())} - last_write = {autoresume_lastwrite}")
                    UlsTools.write_autoresume_ckpt(uls_args.input,
                                                   uls_args.feed,
                                                   autoresume_file,
                                                   log_line,
                                                   current_count=int(my_monitor.get_message_count()))
                    autoresume_lastwrite = int(my_monitor.get_message_count())

                # Filter Enhancement
                if uls_args.filter and not filter_pattern.match(log_line):
                    aka_log.log.info(f"SKIPPED LINE due to FILTER rule {filter_escaped}")
                    aka_log.log.debug(f"SKIPPED the following LOG_LINE "
                                      f"due to FILTER match: {log_line_escaped}")
                    continue

                # Transformation Enhancement
                if uls_args.transformation:
                    log_line = my_transformer.transform(log_line)
                    log_line_escaped = log_line.decode('utf-8').replace('"', '\\"')
                    aka_log.log.debug(f"Transformed Logline via "
                                      f"({uls_args.transformation}): {log_line_escaped}")

                # Attach Linebreak
                #out_data = log_line + uls_config.output_line_breaker.encode()

                # Send the data (through a loop for retransmission)
                resend_counter = 1
                resend_status = False

                while not resend_status and\
                        resend_counter < uls_config.main_resend_attempts:
                    aka_log.log.debug(f"MSG[{my_monitor.get_message_count()}]"
                                      f" Delivery (output) attempt  "
                                      f"{resend_counter} of {uls_config.main_resend_attempts}")
                    # Send the data
                    resend_status = my_output.send_data(log_line)
                    my_monitor.increase_message_count(len(log_line))
                    if uls_args.debugloglines:
                        aka_log.log.debug(f"<OUT> {log_line_escaped}")
                    resend_counter = resend_counter + 1

                if resend_counter == uls_config.main_resend_attempts and\
                        uls_config.main_resend_exit_on_fail:
                    aka_log.log.critical(f"MSG[{my_monitor.get_message_count()}] "
                                        f"ULS was not able to deliver the log message "
                                        f"{log_line_escaped} after {resend_counter} attempts - Exiting!")
                    sys.exit(1)
                elif resend_counter == uls_config.main_resend_attempts and \
                        not uls_config.main_resend_exit_on_fail:
                    aka_log.log.warning(
                        f"MSG[{my_monitor.get_message_count()}] "
                        f"ULS was not able to deliver the log message "
                        f"{log_line_escaped} after {resend_counter} attempts - (continuing anyway as my config says)")
        except queue.Empty:
            # No data available, we get a chance to capture the StopEvent
            pass
        except KeyboardInterrupt:
            control_break_handler()
        except Exception as my_error:
            aka_log.log.critical(f"General error in ULS main loop: {my_error}")

    my_output.tear_down()

    if stopEvent.is_set():
        sys.exit(100)


if __name__ == "__main__":
    main()

# EOF
