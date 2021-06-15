# Copyright 2021 Akamai Technologies, Inc. All Rights Reserved
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

import config.global_config as uls_config


def init():
    # Argument Parsing
    parser = argparse.ArgumentParser(description=f"{uls_config.__tool_name_long__}",
                                     formatter_class=argparse.RawTextHelpFormatter)
    # Common params
    parser.add_argument('-l', '--loglevel',
                        action='store',
                        type=str.upper,
                        default=(os.environ.get('ULS_LOGLEVEL') or uls_config.log_level_default),
                        choices=uls_config.log_levels_available,
                        help=f'Adjust the loglevel Default: {uls_config.log_level_default}')

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
                             default=(os.environ.get('ULS_EDGERC') or '~/.edgerc'),
                             help="Location of the credentials file (default is ~/.edgerc)")
    # EDGERC-SECTION
    input_group.add_argument('--section',
                             action='store',
                             type=str,
                             dest="credentials_file_section",
                             default=(os.environ.get('ULS_SECTION') or 'default'),
                             help="Credentials file Section's name to use ('default' if not specified).")

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

    # Output HOST
    output_group.add_argument('--host',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_OUTPUT_HOST') or None),
                              help="Host for TCP/UDP")

    # OUTPUT PORT
    output_group.add_argument('--port',
                              action='store',
                              type=int,
                              default=int(os.environ.get('ULS_OUTPUT_PORT') or '0'),
                              help="Port for TCP/UDP")

    # HTTP URL
    output_group.add_argument('--httpurl',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_HTTP_URL') or None),
                              help=f'Full http(s) target url i.e. '
                                   f'https://my.splunk.host:9091/services/collector/event"')

    # HTTP AUTH HEADER
    output_group.add_argument('--httpauthheader',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_HTTP_AUTH_HEADER') or None),
                              help='HTTP Header for authorization. Example: '
                                   '\'{"Authorization": "Splunk xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"}\'')

    # Disable HTTP TLS verification
    output_group.add_argument('--httpinsecure',
                              action='store',
                              type=bool,
                              default=(os.environ.get('ULS_HTTP_INSECURE') or False),
                              nargs='?',
                              const=True,
                              help=f'Disable TLS CA Certificate verification. Default: False')

    # HTTP FORMAT DEFINITION
    output_group.add_argument('--httpformat',
                              action='store',
                              type=str,
                              default=(os.environ.get('ULS_HTTP_FORMAT') or '{"event": %s}'),
                              help='HTTP Message format expected by http receiver '
                                   '(%%s defines the data string). Default \'{\"event\": %%s}\'')

    return parser.parse_args()

# EOF
