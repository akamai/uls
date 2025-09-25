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

import subprocess
import sys
import time
import shlex
import os
import threading
import queue

# ULS modules
import uls_config.global_config as uls_config
import modules.aka_log as aka_log
import modules.UlsTools as UlsTools


class UlsInputCli:
    """
    Uls Input Class to handle CLI commands from external CLI (ext directory)
    """

    def __init__(self,
                 product=None,
                 feed=None,
                 cliformat=None,
                 credentials_file="~/.edgerc",
                 credentials_file_section="default",
                 rawcmd=None,
                 inproxy=None,
                 starttime: int=None,
                 endtime: int=None,
                 root_path: str=None,
                 cli_debug: bool=False,
                 stopEvent=None):
        """
        Initialzing a new UlsInput handler
        :param product: Input product
        :param feed: Input feed
        :param cliformat: Format within the CLI
        :param credentials_file: Akamai Credentials file (path)
        :param credentials_file_section: (Akamai Section within the credentials file)
        :param rawcmd: RawCMD ["cmd", "cmd", ...]
        :param inproxy: Proxy config
        :param starttime: Start time in epoch seconds
        :param endtime: End time in epoch seconds
        :param root_path: Root path of the git repo (to avoid runtime issues)
        """""

        # Defaults (may vary later)
        self.name = "UlsInputCli"       # Class Human readable name
        self.running = False            # Internal Running tracker - do not touch
        self.proc = None
        self.proc_output = None
        self.rerun_counter = 1
        self.cli_proc = None
        self.run_once = False
        self.cycle_counter = 0

        # Handover Parameters
        self.product = product
        self.feed = feed
        self.cliformat = cliformat
        self.credentials_file = credentials_file
        self.credentials_file_section = credentials_file_section
        self.rawcmd = rawcmd
        self.inproxy = inproxy
        self.starttime = starttime
        self.endtime = endtime
        self.root_path = root_path
        self.cli_debug = cli_debug

        # Variables (load from uls_config)
        self.run_delay = uls_config.input_run_delay              # Time in seconds to wait for the first health check
        self.rerun_retries = uls_config.input_rerun_retries      # Number of rerun attempts before giving up
        self.rerun_delay = uls_config.input_rerun_delay          # Time in seconds between rerun attempts
        self.bin_python = uls_config.bin_python                  # The python binary
        self.disable_stderr = uls_config.input_disable_stderr    #Specify if STDERR should be disabled at all after $disable_stderr_after cycles
        self.disable_stderr_after = uls_config.input_disable_stderr_after   # Disable StdErr Output after # cycles

        # Generic vars
        self.edgerc_hostname = None

        # StopEvent
        self.stopEvent = stopEvent

    def _feed_selector(self, feed, product_feeds):
        if feed in product_feeds:
            # feed matches the given list
            aka_log.log.info(f'{self.name} - selected feed: {feed}')
        elif not feed or feed == "DEFAULT":
            # Set default (first of feeds)
            feed = product_feeds[0]
            aka_log.log.warning(f'{self.name} - using default feed: {feed}')
        else:
            aka_log.log.critical(
                f"{self.name} - Feed ({feed}) not available - Available: {product_feeds}")
            self.stopEvent.set()
            sys.exit(1)
        return feed

    def _format_selector(self, cliformat):
        if cliformat in uls_config.input_format_choices:

            return cliformat
        elif not cliformat:
            cliformat = 'JSON'
            aka_log.log.info(f'{self.name} - using default format: {cliformat}')
        else:
            aka_log.log.critical(
                f"{self.name} - FORMAT ({cliformat}) not available")
            self.stopEvent.set()
            sys.exit(1)
        return cliformat

    def _prep_proxy(self, proxy):
        if proxy:
            return ['--proxy', proxy]
        else:
            return ""

    def _prep_edgegridauth(self, credentials_file, credentials_file_section):
        edgegrid_auth = ['--edgerc', credentials_file, '--section', credentials_file_section]
        return edgegrid_auth


    def _prep_start_endtime(self, cli_param, time):
        if time:
            aka_log.log.info(f"{self.name} - Found {cli_param} timestamp: {time}")
            my_return = [str(cli_param), str(time)]
            return my_return


    def _uls_useragent(self, product, feed):
        install_id = UlsTools.get_install_id()['install_id']
        if install_id:
            header_install_id = f"-{install_id}"
        if UlsTools.check_container():
            my_useragent = f'ULS/{uls_config.__version__}_{product}-{feed}{header_install_id}-DKR'
        else:
            my_useragent = f'ULS/{uls_config.__version__}_{product}-{feed}{header_install_id}'
        return ["--user-agent-prefix", my_useragent]

    def _cli_debug_cmd(self, debug_cmd: list):
        """Craft the CLI Debug command, if required"""
        if self.cli_debug:
            aka_log.log.debug(f"{self.name} - Enabling the CLI DEBUG MODE")
            return debug_cmd
        else:
            return None

    def _gen_cli_cmd(self,
                     cli_bin: str=None,
                     cli_feeds: list=None,
                     eventtrigger: str=None,
                     cli_debug: list=None,
                     edgerc_file: list=None,
                     proxy: list=None,
                     starttime: list=None,
                     endtime: list=None,
                     skip_feed: bool=False,
                     follow_sign: str="-f",
                     feed_override: list=None,
                     outformat: list=None
                     ):
            """ Craft the CLI Command"""
            product_path = self.root_path + "/" + cli_bin

            # If there needs to be an adoption of the feed name (feed != the real feed)
            if not feed_override:
                tmp_feed = self._feed_selector(self.feed, cli_feeds).lower()
                feed = [tmp_feed]

            else:
                feed = feed_override

            # Craft the base command
            my_cli_cmd = [self.bin_python, '-u', product_path]

            if not self.rawcmd:
                # Add CLI DEBUGGING if required
                if cli_debug:
                    my_cli_cmd = my_cli_cmd + cli_debug

                # add the useragent
                my_cli_cmd = my_cli_cmd + self._uls_useragent(self.product, "_".join(feed))
                #my_cli_cmd = my_cli_cmd + self._uls_useragent(self.product, [feed])

                # Add the edgerc, if provided
                if edgerc_file:
                    my_cli_cmd = my_cli_cmd + edgerc_file

                if proxy:
                    my_cli_cmd = my_cli_cmd + proxy

                # Generating the rest of the command
                if not skip_feed:
                    my_cli_cmd = my_cli_cmd + [eventtrigger] + feed

                if outformat:
                    my_cli_cmd = my_cli_cmd + outformat

                elif skip_feed:
                    my_cli_cmd = my_cli_cmd + [eventtrigger]

                if starttime:
                    my_cli_cmd = my_cli_cmd + starttime

                if endtime:
                    my_cli_cmd = my_cli_cmd + endtime
                else:
                    my_cli_cmd = my_cli_cmd + [follow_sign]

            elif self.rawcmd:
                my_cli_cmd = my_cli_cmd + self._uls_useragent(self.product, "rawcmd")
                my_cli_cmd = my_cli_cmd + shlex.split(self.rawcmd)

            #print(my_cli_cmd)
            #sys.exit(1)
            return my_cli_cmd


    def proc_create(self):

        while self.running is False and self.rerun_counter <= self.rerun_retries and not self.run_once:
            edgegrid_auth = self._prep_edgegridauth(self.credentials_file,
                                                    self.credentials_file_section)


            aka_log.log.info(f'{self.name} - selected product: {self.product}')


            # Enterprise Application Access
            if self.product == "EAA":
                my_feed = self._feed_selector(self.feed, uls_config.eaa_cli_feeds)
                feed_format = None
                if self.cliformat == "JSON":
                    feed_format = ["--json"]


                # Connection health
                if my_feed == "CONHEALTH":
                    self.edgerc_hostname = UlsTools.uls_check_edgerc(
                        self.credentials_file,
                        self.credentials_file_section,
                        uls_config.edgerc_openapi
                    )

                    cli_command = self._gen_cli_cmd(
                        cli_bin=uls_config.bin_eaa_cli,
                        cli_feeds=uls_config.eaa_cli_feeds,
                        eventtrigger="connector",
                        cli_debug=self._cli_debug_cmd(["--debug"]),
                        edgerc_file=edgegrid_auth,
                        proxy=self._prep_proxy(self.inproxy),
                        starttime=self._prep_start_endtime('--start', self.starttime),
                        endtime=self._prep_start_endtime('--end', self.endtime),
                        feed_override=["list", "--perf"],
                        follow_sign="--tail",
                        outformat=feed_format
                    )

                # Device Inventory
                elif my_feed == "DEVINV":
                    self.edgerc_hostname = UlsTools.uls_check_edgerc(
                        self.credentials_file,
                        self.credentials_file_section,
                        uls_config.edgerc_openapi
                    )

                    cli_command = self._gen_cli_cmd(
                        cli_bin=uls_config.bin_eaa_cli,
                        cli_feeds=uls_config.eaa_cli_feeds,
                        eventtrigger="dp",
                        cli_debug=self._cli_debug_cmd(["--debug"]),
                        edgerc_file=edgegrid_auth,
                        proxy=self._prep_proxy(self.inproxy),
                        starttime=self._prep_start_endtime('--start', self.starttime),
                        endtime=self._prep_start_endtime('--end', self.endtime),
                        feed_override=["inventory"],
                        follow_sign="--tail"
                    )

                # Directory Health
                elif my_feed == "DIRHEALTH":
                    self.edgerc_hostname = UlsTools.uls_check_edgerc(
                        self.credentials_file,
                        self.credentials_file_section,
                        uls_config.edgerc_openapi
                    )

                    cli_command = self._gen_cli_cmd(
                        cli_bin=uls_config.bin_eaa_cli,
                        cli_feeds=uls_config.eaa_cli_feeds,
                        eventtrigger="dir",
                        cli_debug=self._cli_debug_cmd(["--debug"]),
                        edgerc_file=edgegrid_auth,
                        proxy=self._prep_proxy(self.inproxy),
                        starttime=self._prep_start_endtime('--start', self.starttime),
                        endtime=self._prep_start_endtime('--end', self.endtime),
                        feed_override=["list"],
                        follow_sign="--tail",
                        outformat=feed_format
                    )

                # All olhter (standard) feeds
                else:
                    self.edgerc_hostname = UlsTools.uls_check_edgerc(
                        self.credentials_file,
                        self.credentials_file_section,
                        uls_config.edgerc_eaa_legacy
                    )

                    cli_command = self._gen_cli_cmd(
                        cli_bin=uls_config.bin_eaa_cli,
                        cli_feeds=uls_config.eaa_cli_feeds,
                        eventtrigger="log",
                        cli_debug=self._cli_debug_cmd(["--debug"]),
                        edgerc_file=edgegrid_auth,
                        proxy=self._prep_proxy(self.inproxy),
                        starttime=self._prep_start_endtime('--start', self.starttime),
                        endtime=self._prep_start_endtime('--end', self.endtime),
                        outformat=feed_format
                    )

            # Enterprise Threat Protector / Secure Internet Access)
            elif self.product == "ETP" or self.product == "SIA":
                my_feed = self._feed_selector(self.feed, uls_config.etp_cli_feeds)

                self.edgerc_hostname = UlsTools.uls_check_edgerc(
                    self.credentials_file,
                    self.credentials_file_section,
                    uls_config.edgerc_openapi + ["etp_config_id"])

                # Only JSON format support
                if not self.cliformat == "JSON":
                    aka_log.log.warning(f"{self.name} - Selected LOG Format ({self.cliformat}) "
                                        f"not available for {self.product}, continuing with JSON.")
                    self.cliformat = "JSON"

                # Trigger DNS WARNING MESSAGE
                if my_feed == "DNS":
                    aka_log.log.warning(f"SIA-DNS FEED Improvement: Akamai SIA team has provided a smoother way of delivering huge log streams such as the DNS one to SIEM. Please have a look here: https://github.com/akamai/uls/blob/main/docs/FAQ.md#is-there-an-alternative-to-stream-high-volume-sia--etp-logs-")
                    time.sleep(3)

                cli_command = self._gen_cli_cmd(
                    cli_bin=uls_config.bin_etp_cli,
                    cli_feeds=uls_config.etp_cli_feeds,
                    eventtrigger="event",
                    cli_debug=self._cli_debug_cmd(["--debug"]),
                    edgerc_file=edgegrid_auth,
                    proxy=self._prep_proxy(self.inproxy),
                    starttime=self._prep_start_endtime('--start', self.starttime),
                    endtime=self._prep_start_endtime('--end', self.endtime),
                )

            # Akamai MFA
            elif self.product == "MFA":
                # Check the EDGERC for the product
                self.edgerc_hostname = UlsTools.uls_check_edgerc(
                    self.credentials_file,
                    self.credentials_file_section,
                    uls_config.edgerc_mfa
                )

                # Only JSON format support
                if not self.cliformat == "JSON":
                    aka_log.log.warning(f"{self.name} - Selected LOG Format ({self.cliformat}) "
                                        f"not available for {self.product}, continuing with JSON.")
                    self.cliformat = "JSON"

                cli_command = self._gen_cli_cmd(
                    cli_bin=uls_config.bin_mfa_cli,
                    cli_feeds=uls_config.mfa_cli_feeds,
                    eventtrigger="event",
                    cli_debug=self._cli_debug_cmd(["--debug"]),
                    edgerc_file=edgegrid_auth,
                    proxy=self._prep_proxy(self.inproxy),
                    starttime=self._prep_start_endtime('--start', self.starttime),
                    endtime=self._prep_start_endtime('--end', self.endtime),
                    skip_feed=True
                )

            # Guardicore config
            elif self.product == "GC":
                # Check the EDGERC for the product
                self.edgerc_hostname = UlsTools.uls_check_edgerc(
                    self.credentials_file,
                    self.credentials_file_section,
                    uls_config.edgerc_gc
                )

                # Only JSON format support
                if not self.cliformat == "JSON":
                    aka_log.log.warning(f"{self.name} - Selected LOG Format ({self.cliformat}) "
                                        f"not available for {self.product}, continuing with JSON.")
                    self.cliformat = "JSON"

                cli_command = self._gen_cli_cmd(
                    cli_bin=uls_config.bin_gc_cli,
                    cli_feeds=uls_config.gc_cli_feeds,
                    eventtrigger="events",
                    cli_debug=self._cli_debug_cmd(["-l", "debug"]),
                    edgerc_file=edgegrid_auth,
                    proxy=self._prep_proxy(self.inproxy),
                    starttime=self._prep_start_endtime('--start', self.starttime),
                    endtime=self._prep_start_endtime('--end', self.endtime),
                )

            # LINODE config
            elif self.product == "LINODE":

                # Check the EDGERC for the product
                self.edgerc_hostname = UlsTools.uls_check_edgerc(
                    self.credentials_file,
                    self.credentials_file_section,
                    uls_config.edgerc_linode)

                # Only JSON format support
                if not self.cliformat == "JSON":
                    aka_log.log.warning(f"{self.name} - Selected LOG Format ({self.cliformat}) "
                                        f"not available for {self.product}, continuing with JSON.")
                    self.cliformat = "JSON"

                my_feed = self._feed_selector(self.feed, uls_config.linode_cli_feeds)
                if my_feed == "AUDIT":
                    cli_command = self._gen_cli_cmd(
                        cli_bin = uls_config.bin_linode_cli,
                        cli_feeds=uls_config.linode_cli_feeds,
                        eventtrigger="events",
                        cli_debug=self._cli_debug_cmd(["-l", "debug"]),
                        edgerc_file=edgegrid_auth,
                        proxy=self._prep_proxy(self.inproxy),
                        starttime=self._prep_start_endtime('--start', self.starttime),
                        endtime=self._prep_start_endtime('--end', self.endtime),
                    )

                elif my_feed == "UTILIZATION":
                    cli_command = self._gen_cli_cmd(
                        cli_bin=uls_config.bin_linode_cli,
                        cli_feeds=uls_config.linode_cli_feeds,
                        eventtrigger="utilization",
                        cli_debug=self._cli_debug_cmd(["-l", "debug"]),
                        edgerc_file=edgegrid_auth,
                        proxy=self._prep_proxy(self.inproxy),
                        starttime=self._prep_start_endtime('--start', self.starttime),
                        endtime=self._prep_start_endtime('--end', self.endtime),
                        skip_feed=True
                    )

            # Akamai Control Center config
            elif self.product == "ACC":

                # Check the EDGERC for the product
                self.edgerc_hostname = UlsTools.uls_check_edgerc(
                    self.credentials_file,
                    self.credentials_file_section,
                    uls_config.edgerc_openapi
                )

                # Only JSON format support
                if not self.cliformat == "JSON":
                    aka_log.log.warning(f"{self.name} - Selected LOG Format ({self.cliformat}) "
                                        f"not available for {self.product}, continuing with JSON.")
                    self.cliformat = "JSON"

                my_feed = self._feed_selector(self.feed, uls_config.acc_logs_feeds)
                if my_feed == "EVENTS":
                    cli_command = self._gen_cli_cmd(
                        cli_bin=uls_config.bin_acc_logs,
                        cli_feeds=uls_config.acc_logs_feeds,
                        eventtrigger="events",
                        cli_debug=self._cli_debug_cmd(["-l", "debug"]),
                        edgerc_file=edgegrid_auth,
                        proxy=self._prep_proxy(self.inproxy),
                        starttime=self._prep_start_endtime('--start', self.starttime),
                        endtime=self._prep_start_endtime('--end', self.endtime),
                        feed_override=["getevents"]
                    )

            # Mocked output
            elif self.product == "MOCK":
                print ("Not yet there")


            # Everything else (undefined)
            else:
                aka_log.log.critical(f" {self.name} - No valid product selected "
                                     f"(--input={self.product}).")
                self.stopEvent.set()
                sys.exit(1)

            try:
                # Lets start the selection
                self.cycle_counter = 0
                while "" in cli_command:
                    cli_command.remove("")
                aka_log.log.info(f'{self.name} - CLI Command:  {" ".join(cli_command)}')
                os.environ["PYTHONUNBUFFERED"] = "1"
                if not self.cli_debug:
                    self.cli_proc = subprocess.Popen(cli_command,
                                                     stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE)
                elif self.cli_debug:
                    self.cli_proc = subprocess.Popen(cli_command,
                                                     stdout=subprocess.PIPE,
                                                     stderr=sys.stdout.buffer)

                aka_log.log.info(f"{self.name} - started PID[{self.cli_proc.pid}]: "
                                 f"{' '.join(cli_command)}")
                self.proc = self.cli_proc
                self.proc_output = self.cli_proc.stdout



                # Non-blocking on windows causes trouble so we're avoiding it
                # 2022-07-08: Disabled completely see EME-588
                # if not os.name == 'nt':
                #     os.set_blocking(self.proc_output.fileno(), False)

                if not self.endtime:
                    time.sleep(1)
                else:
                    self.run_once = True
                #if self.endtime:
                #    self.run_once = True

                if not self.check_proc():
                    #self.rerun_counter += 1
                    raise NameError(f"process [{self.cli_proc.pid}] "
                                    f"exited RC={self.cli_proc.returncode}, REASON: "
                                    f"{self.cli_proc.stderr.read().decode()}")

                # Handover the app into running state (disable stderr as it caused issues)
                # and reset rerun counter to 1
                self.running = True
                self.rerun_counter = 1
                if self.endtime:
                    self.run_once = True


                #self.cli_proc.stderr = subprocess.DEVNULL

            except Exception as my_error:
                time.sleep(self.rerun_delay)
                self.running = False
                self.rerun_counter += 1
                aka_log.log.error(f'{self.name} - {my_error} - '
                                  f'{self.cli_proc.stderr.read().decode()}')

            if self.running is False and self.rerun_counter > self.rerun_retries:
                aka_log.log.critical(f'{self.name} - Not able to start the CLI for '
                                     f'{self.product}. See above errors. '
                                     f'Giving up after {self.rerun_counter - 2} retries. Exiting NOW')
                self.stopEvent.set()
                sys.exit(1)

    def check_proc(self):
        try:
            if self.proc.poll() is None:
                if self.cycle_counter == self.disable_stderr_after and self.disable_stderr:
                    aka_log.log.info(f"{self.name} - Disabling STDERR output from now on, after {self.cycle_counter} successful cycles")
                    self.cli_proc.stderr = subprocess.DEVNULL
                aka_log.log.debug(f'{self.name} - Successful cycles for proc[{self.proc.pid}]: {self.cycle_counter}')
                self.cycle_counter = self.cycle_counter + 1
                return True
            else:
                self.running = False
                self.rerun_counter += 1
                if self.run_once:
                    aka_log.log.critical(f"{self.name} - '--endtime' was specified - so stopping now")
                    self.stopEvent.set()
                    sys.exit(1)
                elif (self.cycle_counter <= self.disable_stderr_after and self.disable_stderr) or not self.disable_stderr:
                    aka_log.log.error(f'{self.name} - CLI process [{self.proc.pid}]'
                                      f' was found stale - Reason:  "{self.proc.stderr.read().decode()}" ')
                else:
                    aka_log.log.error(f'{self.name} - CLI process [{self.proc.pid}], sadly stderr has been disabled')
                self.proc_create()
                return False

        except Exception as my_error:
            if self.run_once:
                aka_log.log.critical(f"{self.name} - '--endtime' was specified - so stopping now")
                self.stopEvent.set()
                sys.exit(0)
            else:
                aka_log.log.error(f'{self.name} - Soemthing really '
                                     f'strange happened - message: {my_error}')

            self.proc_create()
            return False

    def ingest(self, stopEvent, event_q, monitor):
        """
        Ingest CLI incoming data asynchronously
        The function will return immediately
        Args:
            stopEvent (_type_): Stop Event that will stop the current thread
            event_q (_type_): The queue where to put the message
            monitor (): Monitor
        """
        self.stopEvent = stopEvent
        self.event_queue = event_q
        self.monitor = monitor
        self.ingest_thread = threading.Thread(target=self.ingest_loop)
        self.ingest_thread.setName("ingest_loop")
        self.ingest_thread.start()

    def ingest_loop(self):

        # When reading CLI output, if no data, pause 10ms before retrying
        # if still no data, then it will backoff exponentially till 60s
        wait_default = uls_config.main_wait_default
        wait_max = uls_config.main_wait_max
        wait = wait_default

        while not self.stopEvent.is_set():
            try:

                # Ensure the Input handler is still running (rebump if stale)
                self.check_proc()

                input_data = self.proc_output.readline()
                if input_data:
                    self.event_queue.put(input_data, timeout=0.05)
                    self.monitor.increase_message_ingested()
                    wait = wait_default  # back to 10ms wait in case of bursty content
                else:
                    aka_log.log.debug(f"ingest_loop, wait {wait} seconds [{self.monitor.get_stats()}]")
                    self.stopEvent.wait(wait)
                    wait = min(wait * 2, wait_max)  # double the wait till a max of 60s
            except queue.Full:
                aka_log.log.fatal("Capacity exceeded, too many incoming data vs. slow output")
                self.stopEvent.set()
            except Exception:
                aka_log.log.exception("Error in ingest_loop")

    def get_edgerc_hostname(self):
        if self.edgerc_hostname:
            return self.edgerc_hostname
        else:
            return "no_hostname_available"



    # EOF
