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
from distutils.util import strtobool

import uls_config.global_config as uls_config


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
                        help=f'Adjust the loglevel Default: {uls_config.log_level_default}')
    # put loglines into debug log
    parser.add_argument('--debugloglines',
                        action='store',
                        type=bool,
                        nargs='?',
                        default=(os.environ.get('ULS_DEBUGLOGLINES') or uls_config.log_debugloglines_default),
                        const=True,
                        help=f"Should the log_lines appear in debug log? (Default: {uls_config.log_debugloglines_default})")

    # Version Information
    parser.add_argument('-v', '--version',
                        action='store',
                        type=bool,
                        default=False,
                        nargs='?',
                        const=True,
                        help=f'Display {uls_config.__tool_name_short__} version and operational information')

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
                             help="Select the Input Source. Default: None", )
    # INPUT_FEED
    input_group.add_argument('-f', '--feed',
                             action='store',
                             type=str.upper,
                             default=(os.environ.get('ULS_FEED') or 'DEFAULT'),
                             help="Select data feed [CLI-DEFAULT]")
    # INPUT FORMAT
    input_group.add_argument('--format',
                             action='store',
                             dest="cliformat",
                             type=str.upper,
                             default=(os.environ.get('ULS_FORMAT') or "JSON"),
                             choices=uls_config.input_format_choices,
                             help="Select log output format Default: JSON")
    # INPUT PROXY
    input_group.add_argument('--inproxy', '--inputproxy',
                             dest='inproxy',
                             type=str,
                             default=(os.environ.get('ULS_INPUT_PROXY') or None),
                             help="Use a proxy Server for the INPUT requests (fetching data from AKAMAI API'S)")
                             #help=argparse.SUPPRESS)

    # RAWCMD
    input_group.add_argument('--rawcmd',
                             action='store',
                             type=str,
                             default=(os.environ.get('ULS_RAWCMD') or None),
                             help="Overwrite the cli command with your parameters. (python3 akamai-cli $rawcmd)")
    # EDGERC
    input_group.add_argument('--edgerc',
                             action='store',
                             type=str,
                             dest="credentials_file",
                             default=(os.environ.get('ULS_EDGERC') or "~/.edgerc"),
                             help="Location of the credentials file (default is ~/.edgerc)")
    # EDGERC-SECTION
    input_group.add_argument('--section',
                             action='store',
                             type=str,
                             dest="credentials_file_section",
                             default=(os.environ.get('ULS_SECTION') or 'default'),
                             help="Credentials file Section's name to use ('default' if not specified).")

    # Log Starttime
    input_group.add_argument('--starttime',
                             action='store',
                             type=int,
                             dest="starttime",
                             default=(os.environ.get('ULS_STARTTIME') or None),
                             help="Start time (EPOCH SECONDS) from when to start getting logs ('default': cli_default (now), example: '1631556101')")
    # Log Endtime
    input_group.add_argument('--endtime',
                             action='store',
                             type=int,
                             dest="endtime",
                             default=(os.environ.get('ULS_ENDTIME') or None),
                             help="End time (EPOCH SECONDS) until when to stop getting logs ('default': cli_default (never), example: '1631556101')")

    # INPUT QUEUE SIZE
    input_group.add_argument('--inputqueuesize',
                             action='store',
                             type=int,
                             dest="input_queue_size",
                             default=(os.environ.get('ULS_INPUT_QUEUESIZE') or uls_config.input_queue_size ),
                             help=f"Maximum threshold of the input queue. (Default: {uls_config.input_queue_size})")

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
                              help="Select the Output Destination Default: None")

    # TCP / UPD
    ## Output HOST
    output_group.add_argument('--host',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_OUTPUT_HOST') or None),
                              help="Host for TCP/UDP")

    ## OUTPUT PORT
    output_group.add_argument('--port',
                              action='store',
                              type=int,
                              default=int(os.environ.get('ULS_OUTPUT_PORT') or '0' ),
                              help="Port for TCP/UDP")

    ## TCP/UDP FORMAT DEFINITION
    output_group.add_argument('--tcpudpformat',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_TCPUDP_FORMAT') or '%s'),
                              help='TCP UDP Message format expected by the receiver '
                                   '(%%s defines the data string). Default \'%%s\'')


    # HTTP
    ## HTTP URL
    output_group.add_argument('--httpurl',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_HTTP_URL') or None),
                              help=f'Full http(s) target url i.e. '
                                   f'https://my.splunk.host:9091/services/collector/event"')

    ## HTTP AUTH HEADER
    output_group.add_argument('--httpauthheader',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_HTTP_AUTH_HEADER') or None),
                              help='HTTP Header for authorization. Example: '
                                   '\'{"Authorization": "Splunk xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"}\'')

    ## Disable HTTP TLS verification
    output_group.add_argument('--httpinsecure',
                              action='store',
                              type=bool,
                              default=(os.environ.get('ULS_HTTP_INSECURE') or False),
                              nargs='?',
                              const=True,
                              help=f'Disable TLS CA Certificate verification. Default: False')

    ## HTTP FORMAT DEFINITION
    output_group.add_argument('--httpformat',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_HTTP_FORMAT') or '{"event": %s}'),
                              help='HTTP Message format expected by http receiver '
                                   '(%%s defines the data string). Default \'{\"event\": %%s}\'')
    ## HTTP AGGREGATE
    output_group.add_argument('--httpaggregate',
                              action='store',
                              type=int,
                              default=(os.environ.get('ULS_HTTP_AGGREGATE') or uls_config.output_http_aggregate_count),
                              help=f"Number of events to aggregate for one output request "
                                   f"the %%s in the httpformat will be replaced by a LIST of events. "
                                   f"Example: %%s = [{{'event1': 'data1'}},{{'event2': 'data2'}},...] - "
                                   f"Default: {uls_config.output_http_aggregate_count}")

    ## HTTP LIVENESS CHECK
    output_group.add_argument('--httpliveness',
                              action='store',
                              type=lambda x: bool(strtobool(x)),
                              default=(os.environ.get('ULS_HTTP_LIVENESS_CHECK') or uls_config.output_http_liveness_check),
                              help=f"ULS to send a OPTIONS request to the HTTP Server "
                                   f"to ensure its liveness. ULS will fail if server is not "
                                   f"responding with HTTP/200 or HTTP/204. Set to False to "
                                   f"disable. Default: {uls_config.output_http_liveness_check}"
    )

    ## HTTP FORMATTYPE
    output_group.add_argument('--httpformattype',
                              action='store',
                              type=str.lower,
                              default=(os.environ.get('ULS_HTTP_FORMAT_TYPE') or
                                       uls_config.output_http_default_formattype),
                              choices=uls_config.output_http_formattypes,
                              help=f"Specifies the type how the given http format is being wrapped (controls, how the httpformat is being rendered in http output) "
                                   f" Default: {uls_config.output_http_default_formattype}, Valid Choices: {uls_config.output_http_formattypes}")

    # FILE STUFF
    ## File Handler
    output_group.add_argument('--filehandler',
                              action='store',
                              type=str.upper,
                              default=(os.environ.get('ULS_FILE_HANDLER') or "SIZE"),
                              choices=uls_config.output_file_handler_choices,
                              help=f"Output file handler - Decides when files are rotated -"
                                   f"Choices: {uls_config.output_file_handler_choices} -"
                                   f" Default: None")
    ## File Name
    output_group.add_argument('--filename',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_FILE_NAME') or
                                       None),
                              help=f"Output file destination (path + filename)"
                                   f" Default: None")

    ## File Backup count
    output_group.add_argument('--filebackupcount',
                              action='store',
                              type=int,
                              default=(os.environ.get('ULS_FILE_BACKUPCOUNT') or
                                       uls_config.output_file_default_backup_count),
                              help=f"Number of rotated files to keep (backup)"
                                   f" Default: {uls_config.output_file_default_backup_count}")

    ## File Max bytes
    output_group.add_argument('--filemaxbytes',
                              action='store',
                              type=int,
                              default=(os.environ.get('ULS_FILE_MAXBYTES') or
                                       uls_config.output_file_default_maxbytes),
                              help=f"Number of rotated files to keep (backup)"
                                   f" Default: {uls_config.output_file_default_maxbytes} bytes")

    ## File Time
    output_group.add_argument('--filetime',
                              action='store',
                              type=str.upper,
                              default=(os.environ.get('ULS_FILE_TIME') or
                                       uls_config.output_file_time_default),
                              choices=uls_config.output_file_time_choices,
                              help=f"Specifies the file rotation trigger unit  "
                                   f" Default: {uls_config.output_file_time_default}, Valid Choices: {uls_config.output_file_time_choices}")

    ## File Time Interval
    output_group.add_argument('--fileinterval',
                              action='store',
                              type=int,
                              default=(os.environ.get('ULS_FILE_INTERVAL') or
                                       uls_config.output_file_time_interval),
                              help=f"Specifies the file rotation interval based on `--filetime` unit value"
                                   f" Default: {uls_config.output_file_time_interval}")

    ## File Action
    output_group.add_argument('--fileaction',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_FILE_ACTION') or None),
                              help=f"This enables you to specify your own action upon a file rotation. ('%%s' defines the absolute file_name e.g. /path/to/my_file.log.1)."
                                   f" Default: <None>")

    # ----------------------
    special_group = parser.add_argument_group(title="Transformation",
                                             description="Define Module Settings (Output manipulation)")

    # Output FILTER
    special_group.add_argument('--filter',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_OUTPUT_FILTER') or None),
                              help="Filter (regex) to reduce number of sent log files (Only send lines that match the --filter argument).")

    # Transformation Handler
    special_group.add_argument('--transformation',
                              action='store',
                              dest="transformation",
                              type=str.upper,
                              default=(os.environ.get('ULS_TRANSFORMATION') or None),
                              choices=uls_config.transformation_choices,
                              help="Select a transformation to manipulate the output format (optional)")

    special_group.add_argument('--transformpattern', '--transformationpattern',
                              action='store',
                              dest="transformationpattern",
                              type=str,
                              default=(os.environ.get('ULS_TRANSFORMATION_PATTERN') or None),
                              help="Provide a pattern to transform the output (Required for JMESPATH)")



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
                        help=f'Enable automated resume on based on a checkpoint (do not use alongside --starttime)')

    resume_group.add_argument('--autoresumepath',
                        action='store',
                        type=str,
                        dest='autoresumepath',
                        default=(os.environ.get('ULS_AUTORESUME_PATH') or uls_config.autoresume_checkpoint_path),
                        help=f'Specify the path where checkpoint files should be written to. (Trailing /) [Default: {uls_config.autoresume_checkpoint_path}]')

    resume_group.add_argument('--autoresumewriteafter',
                              action='store',
                              type=int,
                              dest='autoresumewriteafter',
                              default=(os.environ.get('ULS_AUTORESUME_WRITEAFTER') or uls_config.autoresume_write_after),
                              help=f'Specify after how many loglines a checkpoint should be written [Default: {uls_config.autoresume_write_after}]')

    return parser.parse_args()


# EOF
