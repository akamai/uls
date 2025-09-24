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

import argparse
import os
# from distutils.util import strtobool

import uls_config.global_config as uls_config

def strtobool(value):
    """
    We could do
    from distutils.util import strtobool
    Yet, it won't be a good long term solution:
    https://docs.python.org/3.10/library/distutils.html
    """
    if isinstance(value, bool):
        return value
    value = value.lower()
    if value in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif value in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid input value %r" % (value,))


def init():
    # Argument Parsing
    parser = argparse.ArgumentParser(description=f"{uls_config.__tool_name_long__}",
                                     formatter_class=argparse.RawTextHelpFormatter)
    # Loglevel
    parser.add_argument('-l', '--loglevel',
                        action='store',
                        type=str.upper,
                        default=(os.environ.get('ULS_LOGLEVEL') or uls_config.log_level_default),
                        choices=uls_config.log_levels_available,
                        help=f'Adjust the loglevel Default: {uls_config.log_level_default}'
                             f"\nENV-VAR: 'ULS_LOGLEVEL'"
                        )

    parser.add_argument('--clidebug',
                        action='store',
                        type=bool,
                        nargs='?',
                        default=(os.environ.get('ULS_CLIDEBUG') or uls_config.cli_debug_default),
                        const=True,
                        dest='clidebug',
                        help=f'Turn on/off the CLI DEBUG output. This will work with RAW OUTPUT only ! Default: {uls_config.cli_debug_default}'
                             f"\nENV-VAR: 'ULS_CLIDEBUG'"
                        )

    parser.add_argument('--json-log',
                        action='store',
                        dest='jsonlog',
                        type=bool,
                        nargs='?',
                        default=(os.environ.get('ULS_JSONLOG') or uls_config.log_jsonlog),
                        const=True,
                        help=f"Should ULS write its own logdata in JSON format  instead of plain text output ? (Default: {uls_config.log_jsonlog})"
                             f"\nENV-VAR: 'ULS_JSONLOG'"
                        )

    parser.add_argument('--ulslogformat',
                        action='store',
                        dest='logformat',
                        type=str,
                        default=(os.environ.get('ULS_LOGFORMAT') or False),
                        help=f"Custom logging format (ULS internal logs) see additional features documentation for more information -  (Default: False)"
                             f"\nENV-VAR: 'ULS_LOGFORMAT'"
                        )

    parser.add_argument('--ulslogdatefmt',
                        action='store',
                        dest='logdatefmt',
                        type=str,
                        default=(os.environ.get('ULS_LOG_DATEFORMAT') or uls_config.log_datefmt),
                        help=f"Adjust the logging date/time format to your needs, (Default: {uls_config.log_datefmt.replace('%', '%%')})"
                             f"\nENV-VAR: 'ULS_LOG_DATEFORMAT'"
                        )
                        # Added double %% to have argsparser display proper string as it tries do to % replacement :D

    # put loglines into debug log
    parser.add_argument('--debugloglines',
                        action='store',
                        type=bool,
                        nargs='?',
                        default=(os.environ.get('ULS_DEBUGLOGLINES') or uls_config.log_debugloglines_default),
                        const=True,
                        help=f"Should the log_lines appear in debug log? (Default: {uls_config.log_debugloglines_default})"
                             f"\nENV-VAR: 'ULS_DEBUGLOGLINES'"
                        )

    # Version Information
    parser.add_argument('-v', '--version',
                        action='store',
                        type=bool,
                        default=False,
                        nargs='?',
                        const=True,
                        help=f'Display {uls_config.__tool_name_short__} version and operational information'
                        )

    parser.add_argument('--nocallhome',
                        action='store',
                        type=bool,
                        default=os.environ.get('ULS_NOCALLHOME') or not uls_config.callhome_enabled,
                        nargs='?',
                        const=True,
                        help=f"Disable the ULS CallHome feature that helps the ULS developers to continue improving ULS. Default: {not uls_config.callhome_enabled}"
                             f"\nENV-VAR: 'ULS_NOCALLHOME'"
                        )


    # ----------------------
    # Input GROUP
    input_group = parser.add_argument_group(title="Input",
                                            description="Define INPUT Settings (AKAMAI API)")

    # INPUT_SELECTOR
    input_group.add_argument('-i', '--input',
                             action='store',
                             type=str.upper,
                             default=(os.environ.get('ULS_INPUT') or None),
                             choices=uls_config.input_choices,
                             help="Select the Input Source (The Akamai product). Default: None"
                                  f"\nENV-VAR: 'ULS_INPUT'"
                             )
    # INPUT_FEED
    input_group.add_argument('-f', '--feed',
                             action='store',
                             type=str.upper,
                             default=(os.environ.get('ULS_FEED') or 'DEFAULT'),
                             help="Select data feed [CLI-DEFAULT]"
                                  f"\nENV-VAR: 'ULS_FEED'"
                             )
    # INPUT FORMAT
    input_group.add_argument('--format',
                             action='store',
                             dest="cliformat",
                             type=str.upper,
                             default=(os.environ.get('ULS_FORMAT') or "JSON"),
                             choices=uls_config.input_format_choices,
                             help="Select log output format Default: JSON"
                                  f"\nENV-VAR: 'ULS_FORMAT'"
                             )
    # INPUT PROXY
    input_group.add_argument('--inproxy', '--inputproxy',
                             dest='inproxy',
                             type=str,
                             default=(os.environ.get('ULS_INPUT_PROXY') or None),
                             help="Use a proxy Server for the INPUT requests (fetching data from AKAMAI API'S)"
                                  f"\nENV-VAR: 'ULS_INPUT_PROXY'"
                             )
                             #help=argparse.SUPPRESS)

    # RAWCMD
    input_group.add_argument('--rawcmd',
                             action='store',
                             type=str,
                             default=(os.environ.get('ULS_RAWCMD') or None),
                             help="Overwrite the cli command with your parameters. (python3 akamai-cli $rawcmd)"
                                  f"\nENV-VAR: 'ULS_RAWCMD'"
                             )
    # EDGERC
    input_group.add_argument('--edgerc',
                             action='store',
                             type=str,
                             dest="credentials_file",
                             default=(os.environ.get('ULS_EDGERC') or "~/.edgerc"),
                             help="Location of the credentials file (default is ~/.edgerc)"
                                   f"\nENV-VAR: 'ULS_EDGERC'"
                             )
    # EDGERC-SECTION
    input_group.add_argument('--section',
                             action='store',
                             type=str,
                             dest="credentials_file_section",
                             default=(os.environ.get('ULS_SECTION') or 'default'),
                             help="Credentials file Section's name to use ('default' if not specified)."
                                  f"\nENV-VAR: 'ULS_SECTION'"
                             )

    # Log Starttime
    input_group.add_argument('--starttime',
                             action='store',
                             type=int,
                             dest="starttime",
                             default=(os.environ.get('ULS_STARTTIME') or None),
                             help="Start time (EPOCH SECONDS) from when to start getting logs ('default': cli_default (now), example: '1631556101')"
                                  f"\nENV-VAR: 'ULS_STARTTIME'"
                             )
    # Log Endtime
    input_group.add_argument('--endtime',
                             action='store',
                             type=int,
                             dest="endtime",
                             default=(os.environ.get('ULS_ENDTIME') or None),
                             help="End time (EPOCH SECONDS) until when to stop getting logs ('default': cli_default (never), example: '1631556101')"
                                  f"\nENV-VAR: 'ULS_ENDTIME'"
                             )

    # INPUT QUEUE SIZE
    input_group.add_argument('--inputqueuesize',
                             action='store',
                             type=int,
                             dest="input_queue_size",
                             default=(os.environ.get('ULS_INPUT_QUEUESIZE') or uls_config.input_queue_size ),
                             help=f"Maximum threshold of the input queue. (Default: {uls_config.input_queue_size})"
                                  f"\nENV-VAR: 'ULS_INPUT_QUEUESIZE'"
                             )

    # ----------------------
    # Output GROUP
    output_group = parser.add_argument_group(title="Output",
                                             description="Define OUTPUT Settings (SIEM)")

    # OUTPUT Selector
    output_group.add_argument('-o', '--output',
                              action='store',
                              type=str.upper,
                              default=(os.environ.get('ULS_OUTPUT') or None),
                              choices=uls_config.output_choices,
                              help="Select the Output Destination Default: None"
                              f"\nENV-VAR: 'ULS_OUTPUT'"
                              )

    # TCP / UPD
    ## Output HOST
    output_group.add_argument('--host',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_OUTPUT_HOST') or None),
                              help="Host for TCP/UDP"
                              f"\nENV-VAR: 'ULS_OUTPUT_HOST'"
                              )

    ## OUTPUT PORT
    output_group.add_argument('--port',
                              action='store',
                              type=int,
                              default=int(os.environ.get('ULS_OUTPUT_PORT') or '0' ),
                              help="Port for TCP/UDP"
                                   f"\nENV-VAR: 'ULS_OUTPUT_PORT'"
                              )

    ## TCP/UDP FORMAT DEFINITION
    output_group.add_argument('--tcpudpformat',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_TCPUDP_FORMAT') or '%s'),
                              help='TCP UDP Message format expected by the receiver '
                                   '(%%s defines the data string). Default \'%%s\''
                                   f"\nENV-VAR: 'ULS_TCPUDP_FORMAT'"
                              )


    # HTTP
    ## HTTP URL
    output_group.add_argument('--httpurl',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_HTTP_URL') or None),
                              help=f'Full http(s) target url i.e. '
                                   f'https://my.splunk.host:9091/services/collector/event"'
                                   f"\nENV-VAR: 'ULS_HTTP_URL'"
                              )

    ## HTTP AUTH HEADER
    output_group.add_argument('--httpauthheader',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_HTTP_AUTH_HEADER') or None),
                              help='HTTP Header for authorization. Example: '
                                   '\'{"Authorization": "Splunk xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"}\''
                                   f"\nENV-VAR: 'ULS_HTTP_AUTH_HEADER'"
                              )

    ## Disable HTTP TLS verification
    output_group.add_argument('--httpinsecure',
                              action='store',
                              type=bool,
                              default=(os.environ.get('ULS_HTTP_INSECURE') or False),
                              nargs='?',
                              const=True,
                              help=f'Disable TLS CA Certificate verification. Default: False'
                                   f"\nENV-VAR: 'ULS_HTTP_INSECURE'"
                              )

    ## HTTP FORMAT DEFINITION
    output_group.add_argument('--httpformat',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_HTTP_FORMAT') or '{"event": %s}'),
                              help='HTTP Message format expected by http receiver '
                                   '(%%s defines the data string). Default \'{\"event\": %%s}\''
                                    f"\nENV-VAR: 'ULS_HTTP_FORMAT'"
                              )
    ## HTTP AGGREGATE
    output_group.add_argument('--httpaggregate',
                              action='store',
                              type=int,
                              default=(os.environ.get('ULS_HTTP_AGGREGATE') or uls_config.output_http_aggregate_count),
                              help=f"Number of events to aggregate for one output request "
                                   f"the %%s in the httpformat will be replaced by a LIST of events. "
                                   f"Example: %%s = [{{'event1': 'data1'}},{{'event2': 'data2'}},...] - "
                                   f"Default: {uls_config.output_http_aggregate_count}"
                                   f"\nENV-VAR: 'ULS_HTTP_AGGREGATE'"
                              )

    ## HTTP LIVENESS CHECK
    output_group.add_argument('--httpliveness',
                              action='store',
                              type=lambda x: bool(strtobool(x)),
                              default=(os.environ.get('ULS_HTTP_LIVENESS_CHECK') or uls_config.output_http_liveness_check),
                              help=f"ULS to send a OPTIONS request to the HTTP Server "
                                   f"to ensure its liveness. ULS will fail if server is not "
                                   f"responding with HTTP/200 or HTTP/204. Set to False to "
                                   f"disable. Default: {uls_config.output_http_liveness_check}"
                                   f"\nENV-VAR: 'ULS_HTTP_LIVENESS_CHECK'"
                              )

    ## HTTP FORMATTYPE
    output_group.add_argument('--httpformattype',
                              action='store',
                              type=str.lower,
                              default=(os.environ.get('ULS_HTTP_FORMAT_TYPE') or
                                       uls_config.output_http_default_formattype),
                              choices=uls_config.output_http_formattypes,
                              help=f"Specifies the type how the given http format is being wrapped (controls, how the httpformat is being rendered in http output) "
                                   f" Default: {uls_config.output_http_default_formattype}, Valid Choices: {uls_config.output_http_formattypes}"
                                   f"\nENV-VAR: 'ULS_HTTP_FORMAT_TYPE'"
                              )

    ## HTTP COMPRESSION (on or off)
    output_group.add_argument('--httpcompression',
                              action='store',
                              type=lambda x: bool(strtobool(x)),
                              default=(os.environ.get('ULS_HTTP_COMPRESSION') or uls_config.output_http_compression),
                              help=f"ULS to compress the HTTP payload with the 'http_compression_type' "
                                   f"to reduze network overhead. This could increase CPU load slightly."
                                   f"Set to True to enable. \n"
                                   f"Default: {uls_config.output_http_compression}\n"
                                   f"ENV-VAR: 'ULS_HTTP_COMPRESSION'"
                              )
    ## HTTP COMPRESSION TYPE
    output_group.add_argument('--httpcompressiontype',
                              action='store',
                              type=str.upper,
                              default=(os.environ.get('ULS_HTTP_COMPRESSION_TYPE') or uls_config.output_http_default_compression_type),
                              choices=uls_config.output_http_compression_choices,
                              help=f"HTTP compression method to align with the receiving server\n"
                                   f"Choices: {uls_config.output_http_compression_choices}\n"
                                   f"Default: {uls_config.output_http_default_compression_type}\n"
                                   f"ENV-VAR: 'ULS_HTTP_COMPRESSION_TYPE'"
                              )


    # --- FILE STUFF
    ## File Handler
    output_group.add_argument('--filehandler',
                              action='store',
                              type=str.upper,
                              default=(os.environ.get('ULS_FILE_HANDLER') or "SIZE"),
                              choices=uls_config.output_file_handler_choices,
                              help=f"Output file handler - Decides when files are rotated\n"
                                   f"Choices: {uls_config.output_file_handler_choices}\n"
                                   f"Default: None\n"
                                   f"ENV-VAR: 'ULS_FILE_HANDLER'"
                              )
    ## File Name
    output_group.add_argument('--filename',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_FILE_NAME') or
                                       None),
                              help=f"Output file destination (path + filename)"
                                   f" Default: None"
                                   f"\nENV-VAR: 'ULS_FILE_NAME'"
                              )

    ## File Backup count
    output_group.add_argument('--filebackupcount',
                              action='store',
                              type=int,
                              default=(os.environ.get('ULS_FILE_BACKUPCOUNT') or
                                       uls_config.output_file_default_backup_count),
                              help=f"Number of rotated files to keep (backup)"
                                   f" Default: {uls_config.output_file_default_backup_count}"
                                   f"\nENV-VAR: 'ULS_FILE_BACKUPCOUNT'"
                              )

    ## File Max bytes
    output_group.add_argument('--filemaxbytes',
                              action='store',
                              type=int,
                              default=(os.environ.get('ULS_FILE_MAXBYTES') or
                                       uls_config.output_file_default_maxbytes),
                              help=f"Number of rotated files to keep (backup)"
                                   f" Default: {uls_config.output_file_default_maxbytes} bytes"
                                   f"\nENV-VAR: 'ULS_FILE_MAXBYTES'"
                              )

    ## File Time
    output_group.add_argument('--filetime',
                              action='store',
                              type=str.upper,
                              default=(os.environ.get('ULS_FILE_TIME') or
                                       uls_config.output_file_time_default),
                              choices=uls_config.output_file_time_choices,
                              help=f"Specifies the file rotation trigger unit  "
                                   f" Default: {uls_config.output_file_time_default}, Valid Choices: {uls_config.output_file_time_choices}"
                                   f"\nENV-VAR: 'ULS_FILE_TIME'"
                              )

    ## File Time Interval
    output_group.add_argument('--fileinterval',
                              action='store',
                              type=int,
                              default=(os.environ.get('ULS_FILE_INTERVAL') or
                                       uls_config.output_file_time_interval),
                              help=f"Specifies the file rotation interval based on `--filetime` unit value"
                                   f" Default: {uls_config.output_file_time_interval}"
                                   f"\nENV-VAR: 'ULS_FILE_INTERVAL'"
                              )

    ## File Action
    output_group.add_argument('--fileaction',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_FILE_ACTION') or None),
                              help=f"This enables you to specify your own action upon a file rotation. ('%%s' defines the absolute file_name e.g. /path/to/my_file.log.1)."
                                   f" Default: <None>"
                                   f"\nENV-VAR: 'ULS_FILE_ACTION'"
                              )

    # ----------------------
    special_group = parser.add_argument_group(title="Transformation",
                                             description="Define Module Settings (Output manipulation)")

    # Output FILTER
    special_group.add_argument('--filter',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_OUTPUT_FILTER') or None),
                              help="Filter (regex) to reduce number of sent log files (Only send lines that match the --filter argument)."
                                   f"\nENV-VAR: 'ULS_OUTPUT_FILTER'"
                               )

    # Transformation Handler
    special_group.add_argument('--transformation',
                              action='store',
                              dest="transformation",
                              type=str.upper,
                              default=(os.environ.get('ULS_TRANSFORMATION') or None),
                              choices=uls_config.transformation_choices,
                              help="Select a transformation to manipulate the output format (optional)"
                                   f"\nENV-VAR: 'ULS_TRANSFORMATION'"
                               )

    special_group.add_argument('--transformpattern', '--transformationpattern',
                              action='store',
                              dest="transformationpattern",
                              type=str,
                              default=(os.environ.get('ULS_TRANSFORMATION_PATTERN') or None),
                              help="Provide a pattern to transform the output (Required for JMESPATH)"
                                   f"\nENV-VAR: 'ULS_TRANSFORMATION_PATTERN'"
                               )



    #-------------------------
    resume_group = parser.add_argument_group(title="Autoresume",
                                             description="Define Autoresume Settings")
    # Autoresume / Resume Switch
    resume_group.add_argument('--autoresume', '--resume',
                        action='store',
                        type=bool,
                        dest='autoresume',
                        default=(os.environ.get('ULS_AUTORESUME') or False),
                        nargs='?',
                        const=True,
                        help=f'Enable automated resume on based on a checkpoint (do not use alongside --starttime)'
                             f"\nENV-VAR: 'ULS_AUTORESUME'"
                        )

    resume_group.add_argument('--autoresumepath',
                        action='store',
                        type=str,
                        dest='autoresumepath',
                        default=(os.environ.get('ULS_AUTORESUME_PATH') or uls_config.autoresume_checkpoint_path),
                        help=f'Specify the path where checkpoint files should be written to. (Trailing /) [Default: {uls_config.autoresume_checkpoint_path}]'
                             f"\nENV-VAR: 'ULS_AUTORESUME_PATH'"
                        )

    resume_group.add_argument('--autoresumewriteafter',
                              action='store',
                              type=int,
                              dest='autoresumewriteafter',
                              default=(os.environ.get('ULS_AUTORESUME_WRITEAFTER') or uls_config.autoresume_write_after),
                              help=f'Specify after how many loglines a checkpoint should be written [Default: {uls_config.autoresume_write_after}]'
                                   f"\nENV-VAR: 'ULS_AUTORESUME_WRITEAFTER'"
                              )


    #-------------------------
    prometheus_group = parser.add_argument_group(title="Prometheus",
                                             description="Define Prometheus Monitoring Settings")
    # Prometheues switch
    prometheus_group.add_argument('--prometheus',
                        action='store',
                        type=bool,
                        dest='prometheus_enabled',
                        default=(os.environ.get('ULS_PROMETHEUS') or uls_config.prometheus_enabled),
                        nargs='?',
                        const=True,
                        help=f'Enable prometheues monitoring support - Default: {uls_config.prometheus_enabled}'
                                  f"\nENV-VAR: 'ULS_PROMETHEUS'"
                        )

    prometheus_group.add_argument('--promport', '--prometheus-port',
                        action='store',
                        dest='prometheus_port',
                        type=int,
                        default=(os.environ.get('ULS_PROMETHEUS_PORT') or uls_config.prometheus_port),
                        help=f'Prometheues port to listen on [Default: {uls_config.prometheus_port}]'
                             f"\nENV-VAR: 'ULS_PROMETHEUS_PORT'"
                                  )

    prometheus_group.add_argument('--promaddr', '--prometheus-addr',
                                  action='store',
                                  dest='prometheus_addr',
                                  type=str,
                                  default=(os.environ.get('ULS_PROMETHEUS_ADDR') or uls_config.prometheus_addr),
                                  help=f'Prometheues bind address to listen on [Default: {uls_config.prometheus_addr}]'
                                       f"\nENV-VAR: 'ULS_PROMETHEUS_ADDR'"
                                  )

    prometheus_group.add_argument('--promcert', '--prometheus-certfile',
                        action='store',
                        dest='prometheus_certfile',
                        type=str,
                        default=(os.environ.get('ULS_PROMETHEUS_CERTFILE') or uls_config.prometheus_certfile),
                        help=f'Prometheues certificate file (required alongside a keyfile) [Default: {uls_config.prometheus_certfile}]'
                                  f"\nENV-VAR: 'ULS_PROMETHEUS_CERTFILE'"
                        )


    prometheus_group.add_argument('--promkey', '--prometheus-keyfile',
                        action='store',
                        dest='prometheus_keyfile',
                        type=str,
                        default=(os.environ.get('ULS_PROMETHEUS_KEYFILE') or uls_config.prometheus_keyfile),
                        help=f'Prometheues key file (required alongside a certfile) [Default: {uls_config.prometheus_keyfile}]'
                                  f"\nENV-VAR: 'ULS_PROMETHEUS_KEYFILE'"
                        )
    return parser.parse_args()


# EOF
