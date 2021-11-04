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

import subprocess
import sys
import platform
import os.path
import configparser
import pathlib

# ULS modules
import modules.aka_log as aka_log
import config.global_config as uls_config


def uls_check_sys(root_path):
    """
    Collect ULS requirements information and request input if failing
    """
    def _check_cli_installed(cli_bin):
        try:
            if not os.path.isfile(cli_bin):
                aka_log.log.warning(f"Uhoh - seems like {cli_bin} is not installed. "
                                    f"Please follow docs/COMMAND_LINE_USAGE.md "
                                    f"to setup the required environment cli tools")
                skip_verification = input("Continue anyway ? (y|N)")
                if skip_verification.lower() == "y" or skip_verification.lower() == "yes":
                    print(f"Continuing without {cli_bin} - please be do not use any stream this cli provides")
                else:
                    aka_log.log.critical(f"Missing {cli_bin} - exiting")
                    sys.exit(1)
            else:
                return True
        except Exception as my_error:
            aka_log.log.critical(f"Error checking the cli'tools ")

    _check_cli_installed(root_path + "/" + uls_config.bin_eaa_cli)
    _check_cli_installed(root_path + "/" + uls_config.bin_etp_cli)
    _check_cli_installed(root_path + "/" + uls_config.bin_mfa_cli)


def uls_version(root_path):
    """
    Collect ULS Version information and display it on STDOUT
    """

    my_edgerc_mock_file = root_path + "/" + uls_config.edgerc_mock_file
    def _get_cli_version(cli_bin, edgerc_mock_file):
        try:
            version_proc = subprocess.Popen([uls_config.bin_python, cli_bin, "--edgerc", edgerc_mock_file, "version"],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
            my_cli_version = version_proc.communicate()[0].decode().strip('\n')
            version_proc.terminate()
            if my_cli_version:
                return my_cli_version
            else:
                return "n/a"
        except Exception as my_err:
            return f"n/a -> ({my_err})"

    # Create a mocked edgerc file (fix bug no output on missing edgerc)
    if os.path.isfile(my_edgerc_mock_file):
        os.remove(my_edgerc_mock_file)

    with open(my_edgerc_mock_file, 'x') as mocked_edgerc_file:
        mocked_edgerc_file.write("[default]\n")

    # generate the stdout
    print(f"{uls_config.__tool_name_long__} Version information\n"
          f"ULS Version\t\t{uls_config.__version__}\n\n"
          f"EAA Version\t\t{_get_cli_version(root_path + '/' + uls_config.bin_eaa_cli, my_edgerc_mock_file)}\n"
          f"ETP Version\t\t{_get_cli_version(root_path + '/' + uls_config.bin_etp_cli, my_edgerc_mock_file)}\n"
          f"MFA Version\t\t{_get_cli_version(root_path + '/' + uls_config.bin_mfa_cli, my_edgerc_mock_file)}\n\n"
          f"OS Plattform\t\t{platform.platform()}\n"
          f"OS Version\t\t{platform.release()}\n"
          f"Python Version\t\t{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n"
          f"Docker Status\t\t{check_docker()}\n"
          f"RootPath \t\t{root_path}\n"
          )

    # Delete the mocked edgerc file
    os.remove(my_edgerc_mock_file)

    sys.exit(0)


def uls_check_edgerc(configfile, configsection, configvalues):
    """
    Verify the given "edgerc" file to contain all required variables (for the desired stream) within the given section
    see https://github.com/akamai/uls/blob/main/docs/AKAMAI_API_CREDENTIALS.md for more information
    :param configfile: The path to the config file
    :param configsection: The section within the config file [default]
    :param configvalues: A list of desiresd config values ["val1", "val2", ...]
    :return:
    """
    config = configparser.ConfigParser()
    # Load config file
    if not config.read(configfile):
        aka_log.log.critical(f"Config file '{os.path.expanduser(configfile)}' could not be loaded. - Exiting.")
        sys.exit(1)
    else:
        aka_log.log.debug(f"Config file '{os.path.expanduser(configfile)}' was found and is readable.")

    # Check config section
    if configsection not in config:
        aka_log.log.critical(f"Section '{configsection}' not found. Available sections: '{config.sections()}'. - Exiting")
        sys.exit(1)
    else:
        aka_log.log.debug(f"Section '{configsection}' found.")

    # check for specified values
    for configvalue in configvalues:
        if not configvalue in config[configsection]:
            aka_log.log.critical(f"Required configuration value '{configvalue}' not found in section / file. Please see: {uls_config.edgerc_documentation_url} - Exiting")
            sys.exit(1)
        else:
            aka_log.log.debug(f"Required configuration value '{configvalue}' found.")
    return 0


def uls_check_args(input, output):
    missing = None
    if not input:
        missing = "INPUT"
    elif not output:
        missing = "OUTPUT"
    if missing:
        aka_log.log.critical(f"Required argument / ENV var not set: {missing}")
        aka_log.log.critical(f"Please run `bin/uls.py --help` for additional information")
        sys.exit(1)
    else:
        return 0

def check_docker():
    return os.path.isfile('/.dockerenv')


def runpath():
    """
    Function to return the root path of the repo
    :return: Root path (git root)
    """
    return pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve()