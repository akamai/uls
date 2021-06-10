#!/usr/bin/env python3

import subprocess
import sys
import time
import shlex
import modules.aka_log as aka_log
import config.global_config as uls_config
import platform


def uls_version():
    """
    Collect ULS Version information and display it on STDOUT
    """
    def _get_cli_version(cli_bin):
        try:
            version_proc = subprocess.Popen([uls_config.bin_python, cli_bin, "version"],
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

    # generate the stdout
    print(f"{uls_config.__tool_name_long__} Version information\n"
          f"ULS Version\t\t{uls_config.__version__}\n\n"
          f"EAA Version\t\t{_get_cli_version(uls_config.bin_eaa_cli)}\n"
          f"ETP Version\t\t{_get_cli_version(uls_config.bin_etp_cli)}\n"
          f"MFA Version\t\t{_get_cli_version(uls_config.bin_mfa_cli)}\n\n"
          f"OS Plattform\t\t{platform.platform()}\n"
          f"OS Version\t\t{platform.release()}\n"
          f"Python Version\t\t{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n"
          )
    sys.exit(0)


class UlsInputCli:
    def __init__(self):

        self.run_delay = uls_config.input_run_delay                 # Time in seconds to wait for the first health check
        self.rerun_retries = uls_config.input_rerun_retries         # Number of rerun attempts before giving up
        self.rerun_delay = uls_config.input_rerun_delay             # Time in seconds between rerun attempts
        self.bin_python = uls_config.bin_python                     # The python binary

        # Defaults (may vary later)
        self.name = "UlsInputCli"       # Class Human readable name
        self.running = False            # Internal Running tracker - do not touch
        self.proc = None
        self.proc_output = None

    def _feed_selector(self, feed, product_feeds):
        if feed in product_feeds:
            # feed matches the given list
            aka_log.log.debug(f'{self.name} - selected feed: {feed}')
        elif not feed:
            # Set default (first of feeds)
            feed = product_feeds[0]
            aka_log.log.debug(f'{self.name} - using default feed: {feed}')
        else:
            aka_log.log.critical(
                f"{self.name} - Feed ({feed}) not available - Available: {product_feeds}")
            sys.exit(1)
        return feed

    def _format_selector(self, cliformat):
        if cliformat in uls_config.input_format_choices:

            return cliformat
        elif not cliformat:
            cliformat = 'JSON'
            aka_log.log.debug(f'{self.name} - using default format: {cliformat}')
        else:
            aka_log.log.critical(
                f"{self.name} - FORMAT ({cliformat}) not available")
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

    def _uls_useragent(self, product, feed):
        my_useragent = f'ULS/{uls_config.__version__}_{product}-{feed}'
        return ["--user-agent-prefix", my_useragent]

    def proc_create(self, product=None,
                    feed=None,
                    cliformat=None,
                    credentials_file="~/.edgerc",
                    credentials_file_section="default",
                    rawcmd=None,
                    inproxy=None):

        rerun_counter = 1

        while self.running is False and rerun_counter <= self.rerun_retries:
            edgegrid_auth = self._prep_edgegridauth(credentials_file, credentials_file_section)
            aka_log.log.debug(f'{self.name} - selected product: {product}')

            # EAA config
            if product == "EAA":
                product_path = uls_config.bin_eaa_cli
                product_feeds = uls_config.eaa_cli_feeds
                if not rawcmd:
                    feed = self._feed_selector(feed, product_feeds)
                    cli_command = [self.bin_python, product_path, 'log', feed.lower(), '-f']
                    cli_command[2:2] = self._uls_useragent(product, feed)
                    cli_command[2:2] = edgegrid_auth
                    cli_command[2:2] = self._prep_proxy(inproxy)
                    if self._format_selector(cliformat) == "JSON":
                        cli_command.append('-j')
                else:
                    cli_command = [self.bin_python, product_path] + \
                                  self._uls_useragent(product, feed) +\
                                  shlex.split(rawcmd)

            # ETP config
            elif product == "ETP":
                product_path = uls_config.bin_etp_cli
                product_feeds = uls_config.etp_cli_feeds
                if not rawcmd:
                    feed = self._feed_selector(feed, product_feeds)
                    cli_command = [self.bin_python, product_path, 'event', feed.lower(), '-f']
                    cli_command[2:2] = self._uls_useragent(product, feed)
                    cli_command[2:2] = edgegrid_auth
                    cli_command[2:2] = self._prep_proxy(inproxy)
                else:
                    cli_command = [self.bin_python, product_path] +\
                                  self._uls_useragent(product, feed) +\
                                  shlex.split(rawcmd)

            # MFA config
            elif product == "MFA":
                product_path = uls_config.bin_mfa_cli
                product_feeds = uls_config.mfa_cli_feeds
                if not rawcmd:
                    feed = self._feed_selector(feed, product_feeds)
                    cli_command = [self.bin_python, product_path, 'event', feed.lower(), '-f']
                    cli_command[2:2] = self._uls_useragent(product, feed)
                    cli_command[2:2] = edgegrid_auth
                    cli_command[2:2] = self._prep_proxy(inproxy)
                else:
                    cli_command = [self.bin_python, product_path] +\
                                  self._uls_useragent(product, feed) +\
                                  shlex.split(rawcmd)

            # Everything else (undefined)
            else:
                aka_log.log.critical(f" {self.name} - No valid product selected (--input={product}).")
                sys.exit(1)
            try:
                aka_log.log.debug(f'{self.name} - CLI Command:  {cli_command}')
                cli_proc = subprocess.Popen(cli_command,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)

                aka_log.log.debug(f"{self.name} - started PID[{cli_proc.pid}]: {cli_command}")
                self.proc = cli_proc
                self.proc_output = cli_proc.stdout
                time.sleep(1)

                if not self.check_proc():
                    raise NameError(f"process [{cli_proc.pid}] "
                                    f"exited rc={cli_proc.returncode}: {cli_proc.stderr.read()}")
                self.running = True

            except Exception as my_error:
                time.sleep(self.rerun_delay)
                self.running = False
                rerun_counter += 1
                aka_log.log.error(f'{self.name} - {my_error} -> {self.proc.stderr.read()}')

            if self.running is False and rerun_counter > self.rerun_retries:
                aka_log.log.critical(f'Not able to start the CLI for {product}. See above errors. '
                                     f'Giving up after {rerun_counter - 1} retries.')
                sys.exit(1)

    def check_proc(self):
        try:
            if self.proc.poll() is None:
                return True
            else:
                self.running = False
                aka_log.log.error(f'{self.name} - CLI process [{self.proc.pid}]'
                                  f' was found stale -> {self.proc.stderr.read()}')
                return False
        except:
            return False

# EOF
