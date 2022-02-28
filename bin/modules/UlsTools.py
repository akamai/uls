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
import json
import subprocess
import sys
import platform
import os.path
import configparser
import pathlib
import datetime
import time

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
          f"TimeZone (UTC OFST) \t{check_timezone()} ({-time.timezone / 3600})\n"
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

def check_timezone():
    now = datetime.datetime.now()
    from pytz import reference
    localtime = reference.LocalTimezone()
    return localtime.tzname(now)

def root_path():
    """
    Function to return the root path of the repo
    :return: Root path (git root)
    """
    return pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve()


def check_autoresume(input, feed, checkpoint_dir=uls_config.autoresume_checkpoint_path):
    # Check if we're in a supported stream / feed
    if input not in uls_config.autoresume_supported_inputs or feed == "CONHEALTH":
        aka_log.log.critical(f"Input {input} or feed {feed} currently not supported by AUTORESUME - Exiting.")
        sys.exit(1)

    checkpoint_file = "uls_" + input.lower() + "_" + feed.lower() + ".ckpt"
    checkpoint_full = str(os.path.abspath(checkpoint_dir)) + "/" + checkpoint_file

    if os.path.isfile(checkpoint_full):
        aka_log.log.debug(f"Autoresume Checkpoint found: {checkpoint_full}")
        if os.stat(checkpoint_full).st_size == 0:
            aka_log.log.warning(f"Checkpoint \'{checkpoint_full}\' seems to be empty.")
            creation_time = None
            checkpoint = None
        else:
            try:
                with open (checkpoint_full, "r") as ckpt_f:
                    data = json.load(ckpt_f)
                    if data['creation_time'] and data['checkpoint']:
                        aka_log.log.debug(f"Autoresume Checkpoint successfully loaded. Checkpoint Time: {data['checkpoint']}, Creation_time: {data['creation_time']}")
                        creation_time = data['creation_time']
                        # Convert the Checkpoint to "epoch Timestamp", depending on the input
                        if data['input'] == "ETP":
                            mytime = data['checkpoint'].split("Z")[0]
                        elif data['input'] == "EAA":
                            mytime = data['checkpoint'].split("+")[0]
                        else:
                            aka_log.log.critical(
                                f"Unhandeled input data in checkpointfile  \'{checkpoint_full}\' --> {input} / {feed} - Exiting.")
                            sys.exit(1)
                        checkpoint = int(datetime.datetime(year=int(mytime.split("T")[0].split("-")[0]),
                                            month=int(mytime.split("T")[0].split("-")[1]),
                                            day=int(mytime.split("T")[0].split("-")[2]),
                                            hour=int(mytime.split("T")[1].split(":")[0]),
                                            minute=int(mytime.split("T")[1].split(":")[1]),
                                            second=int(mytime.split("T")[1].split(":")[2]),
                                            ).timestamp())
                        aka_log.log.debug(f"Checkpoint timestamp {data['checkpoint']} converted to epoch time {checkpoint}")
                    else:
                        aka_log.log.critical(f"Inconsitent data in checkpointfile  \'{checkpoint_full}\' --> {data} - Exiting.")
                        sys.exit(1)
            except Exception as readerror:
                aka_log.log.critical(f"Error reading data from \'{checkpoint_full}\': {readerror} - Exiting.")
                sys.exit(1)
    else:
        aka_log.log.info(f"No autoresume Checkpoint found - trying to create {checkpoint_full}")
        creation_time = None
        checkpoint = None
        try:
            pathlib.Path(checkpoint_full).touch()
        except Exception as toucherr:
            aka_log.log.critical(f"Error creating {checkpoint_full}: {toucherr} Please check directory / file permissions. - Exiting")
            sys.exit(1)
        aka_log.log.info(
            f"Checkpoint file {checkpoint_full} successfully created")

    return {'filename': checkpoint_full, 'creation_time': creation_time, 'checkpoint': checkpoint}


def write_autoresume_ckpt(input, feed, autoresume_file, logline):
    aka_log.log.info(f"AUTORESUME - IT's time to write a new checkpoint")

    # Adopt the field to the stream / feed
    checkpoint_line = logline.decode()
    if input == "ETP" and (feed == "THREAT" or feed =="PROXY" or feed == "AUP"):
        checkpoint_timestamp = json.loads(checkpoint_line)['event']['detectionTime']
    elif input == "ETP" and feed == "DNS":
        checkpoint_timestamp = json.loads(checkpoint_line)['query']['time']
    elif input == "EAA" and feed == "ACCESS":
        checkpoint_timestamp = json.loads(checkpoint_line)['datetime']
    else:
        aka_log.log.critical(
            f"AUTORESUME - Unhandled Input / Feed detected:  '{input} / {feed}' (this should never happen !!)- Exiting")
        sys.exit(1)

    # Write out the file
    try:
        autoresume_data = {'creation_time': str(datetime.datetime.now()), 'checkpoint': str(checkpoint_timestamp), 'input': input, 'feed': feed}
        with open(autoresume_file, "w") as ckpt_fd:
            json.dump(autoresume_data, ckpt_fd)
        aka_log.log.debug(f"AUTORESUME - Wrote a new checkpoint to {autoresume_file}: {autoresume_data}")
    except Exception as write_error:
        aka_log.log.critical(f"AUTORESUME - Failure writing data to {autoresume_file} - Data: {autoresume_data} - error: {write_error} - Exiting")
        sys.exit(1)
