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

import socket
import ast
import sys
import os
import time
import threading
import requests
import logging
import logging.handlers

# ULS specific modules
import config.global_config as uls_config
import modules.aka_log as aka_log


stopEvent = threading.Event()


class UlsOutput:
    """
    Uls Output Class to handle data streaming to different targets
    """

    def __init__(self, output_type: str,
                 host=None,
                 port=None,
                 http_out_format=None,
                 http_out_auth_header=None,
                 http_url=None,
                 http_insecure=False,
                 filehandler=None,
                 filename=None,
                 filebackupcount=None,
                 filemaxbytes=None,
                 filetime=None,
                 fileinterval=None):
        """
        Initialzing a new UlsOutput handler
        :param output_type: The desired output format (TCP/ UDP / HTTP)
        :param host: hostname or ip address (TCP/UDP)
        :param port: tcp port number (TCP/UDP)
        :param http_url: URL (scheme://host:port/path) (HTTP)
        :param http_out_format: HTTP Output format ((HTTP)
        :param http_out_auth_header: HTTP Authentication header (HTTP)
        :param http_insecure: (bool) Disable TLS verification (HTTP)
        :return:
        """

        # Defaults (may vary later)
        self.name = "UlsOutput"                 # Class Human readable name
        self.http_verify_tls = False            # whether to verify the Certificate CA (True) or not (False)
        self.connected = False                  # Internal Connection tracker - do not touch
        # self.output_type = None
        self.http_out_format = None
        self.http_url = None
        self.httpSession = None
        self.port = None
        self.host = None
        self.clientSocket = None

        # Handover Parameters
        ## Check & set output type
        if output_type in uls_config.output_choices:
            self.output_type = output_type
            aka_log.log.info(f"{self.name} Selected Output Type: {self.output_type} ")
        else:
            aka_log.log.critical(f"{self.name} target was not defined {output_type} ")
            sys.exit(1)

        ## TCP, UDP parameters
        if self.output_type in ['TCP', 'UDP'] and host and port:
            self.host = host
            self.port = port
        elif self.output_type in ['TCP', 'UDP'] and (not host or not port):
            aka_log.log.critical(f"{self.name} - Host or Port has not "
                                 f"been set Host: {host} Port: {port} - exiting")
            sys.exit(1)

        # HTTP parameters
        elif self.output_type in ['HTTP'] and http_url:
            self.http_url = http_url
            # apply other variables if SET
            self.http_out_format = http_out_format
            self.http_out_auth_header = http_out_auth_header
            self.http_insecure = http_insecure
            self.http_timeout = uls_config.output_http_timeout
        elif self.output_type in ['HTTP'] and not http_url:
            aka_log.log.critical(f"{self.name}  http_out_format http_out_auth_"
                                 f"header http_url or http_insecure missing- exiting")
            sys.exit(1)

        # File Parameters
        elif self.output_type in ['FILE']:
            if filename == None:
                aka_log.log.critical(f"{self.name}  file-output was specified, but no file was specified. "
                                     f"Please use --filename <filename> to specify a file")
                sys.exit(1)
            self.filehandler = filehandler
            self.filename = filename
            self.filebackupcount = filebackupcount
            self.filemaxbytes = filemaxbytes
            self.filetime = filetime
            self.fileinterval = fileinterval

        # Variables (load from uls_config)
        self.reconnect_retries = uls_config.output_reconnect_retries    # Number of reconnect attempts before giving up
        ## TCP / UDP
        self.udp_send_buffer = uls_config.output_udp_send_buffer        # UDP Send buffer in bytes
        self.udp_timeout = uls_config.output_udp_timeout                # UDP SEND / CONNECT Timeout (seconds)
        self.tcp_send_buffer = uls_config.output_tcp_send_buffer        # TCP Send buffer in bytes
        self.tcp_timeout = uls_config.output_tcp_timeout                # TCP SEND / CONNECT Timeout (seconds)
        ## HTTP
        self.http_header = uls_config.output_http_header                # Additional Headers
        ## FILE
        self.file_encoding = uls_config.output_file_encoding            # File Encoding

    def connect(self):
        """
        Connect or Re-Connect the Output handler
        :return:
        """

        reconnect_counter = 1
        while not stopEvent.is_set() and self.connected is False \
                and reconnect_counter <= self.reconnect_retries:
            try:

                # TCP Connector
                if self.output_type == "TCP":
                    # add a check if required vars are set
                    aka_log.log.info(f"{self.name} attempting to connect "
                                     f"via TCP to {self.host}:{self.port} ")
                    self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # check
                    self.clientSocket.setsockopt(socket.SOL_SOCKET,
                                                 socket.SO_SNDBUF,
                                                 self.tcp_send_buffer)
                    self.clientSocket.connect((self.host, self.port))
                    self.clientSocket.settimeout(self.tcp_timeout)
                    reconnect_counter = 1
                    self.connected = True
                    aka_log.log.info(f"{self.name} successful connected "
                                     f"to tcp://{self.host}:{self.port} ")

                # UDP Connector
                elif self.output_type == "UDP":
                    aka_log.log.info(f"{self.name} attempting to connect via "
                                     f"UDP to {self.host}:{self.port} ")
                    self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    self.clientSocket.settimeout(self.udp_timeout)
                    self.clientSocket.setsockopt(socket.SOL_SOCKET,
                                                 socket.SO_SNDBUF,
                                                 self.udp_send_buffer)
                    reconnect_counter = 1
                    self.connected = True
                    aka_log.log.info(f"{self.name} successful connected "
                                     f"to udp://{self.host}:{self.port} ")

                # HTTP Connector
                elif self.output_type == "HTTP":
                    self.httpSession = requests.session()
                    # Prepare & set the headers
                    if self.http_out_auth_header:
                        headers = self.http_header | ast.literal_eval(self.http_out_auth_header)
                    else:
                        headers = self.http_header
                    aka_log.log.info(f"{self.name} adding http headers: {headers}")
                    self.httpSession.headers.update(headers)
                    # Output Format
                    aka_log.log.info(f"{self.name} setting http output "
                                     f"format: {self.http_out_format}")
                    # TLS Verification
                    if self.http_insecure:
                        # DISABLE insecure warnings (if verify=FALSE)
                        requests.packages.urllib3.disable_warnings()
                        self.http_verify_tls = False    # Use the inverted boolean expression ;)
                        aka_log.log.warning(
                            f"{self.name} TLS CA Certificate verification "
                            f"has been disabled - this is insecure !!")
                    elif not self.http_insecure:
                        self.http_verify_tls = True
                        aka_log.log.info(
                            f"{self.name} TLS CA Certificate verification is turned on.")
                    else:
                        aka_log.log.critical(f'{self.name} HTTP insecure was not set '
                                             f'to a boolean value (True|False) '
                                             f'- we got "{self.http_insecure}" instead')
                        sys.exit(1)
                    # Check the URL
                    if not self.http_url:
                        aka_log.log.critical(f'{self.name} HTTP output selected but no URL given. '
                                             f'Use --httpurl instead of --host / --port')
                        sys.exit(1)
                    else:
                        aka_log.log.info(f"{self.name} attempting to connect via "
                                         f"HTTP(S) to {self.http_url} ")

                    # Let'S do an options request
                    resp = self.httpSession.options(url=self.http_url,
                                                    data='{"event":"connection test"}',
                                                    verify=self.http_verify_tls, timeout=self.http_timeout)

                    if resp.status_code == 200:
                        reconnect_counter = 1
                        self.connected = True
                        aka_log.log.info(f"{self.name} successful connected to {self.http_url} ")
                    else:
                        aka_log.log.error(f"{self.name} error connecting to {self.http_url}. "
                                          f"StatusCode: {resp.status_code} Reason: "
                                          f"{resp.text} [{reconnect_counter}]")
                        time.sleep(uls_config.output_reconnect_delay)
                        self.connected = False
                        reconnect_counter = 1

                # RAW OUTPUT
                elif self.output_type == "RAW":
                    aka_log.log.info(f"{self.name} Preparing RAW OUTPUT ... (phew ... done ;D) ")
                    self.connected = True
                    reconnect_counter = 1

                # FILE OUTPUT
                elif self.output_type == "FILE":

                    aka_log.log.info(f"{self.name} preparing FILE output "
                                     f"handler: {self.filehandler} , filename: {self.filename} "
                                     f"encoding: {self.file_encoding} , maxbytes(SIZE): {self.filemaxbytes}"
                                     f"filetime(TIME): {self.filetime} , interval(TIME): {self.fileinterval}")

                    # Check if the specified directory exists
                    if not (os.path.exists(os.path.dirname(self.filename))):
                        aka_log.log.critical(f"{self.name} - The specified directory "
                                             f"{os.path.dirname(self.filename)} does not exist "
                                             f"or privileges are missing - exiting.")
                        sys.exit(1)
                    self.my_file_writer = logging.getLogger('uls_file_writer')

                    if self.filehandler in ['SIZE']:
                        if not self.filemaxbytes:
                            aka_log.log.critical(f"{self.name} - MaxBytes have not been "
                                                 f"specified and somehow the default "
                                                 f"was not used - exiting.")
                            sys.exit(1)
                        file_handler = logging.handlers.RotatingFileHandler(filename=self.filename, mode='a', maxBytes=self.filemaxbytes, backupCount=self.filebackupcount, encoding=self.file_encoding, delay=False)

                    elif self.filehandler in ['TIME']:
                        if not self.fileinterval or not self.filetime:
                            aka_log.log.critical(f"{self.name} - Filetime or FileInterval have not been "
                                                 f"specified and somehow the default "
                                                 f"was not used - exiting.")
                            sys.exit(1)
                        file_handler = logging.handlers.TimedRotatingFileHandler(filename=self.filename, when=self.filetime.lower(), interval=self.fileinterval, backupCount=self.filebackupcount, encoding=self.file_encoding, delay=False, utc=uls_config.output_file_default_time_use_utc, atTime=None)

                    else:

                        aka_log.log.critical(f"{self.name} - No valid filehandler has been specified Valid choices: {uls_config.output_file_handler_choices}. Given value: {self.filehandler} - exiting.")
                        sys.exit(1)

                    self.my_file_writer.addHandler(file_handler)
                    self.my_file_writer.setLevel(logging.INFO)


                    aka_log.log.info(f"{self.name} - File output ready")
                    self.connected = True
                    reconnect_counter = 1


                else:
                    aka_log.log.critical(f"{self.name} - No Valid OUTPUT specified !! - exiting")
                    sys.exit(1)


            except Exception as con_error:
                aka_log.log.warning(f"{self.name} issue: {con_error}")
                if not self.output_type == 'HTTP':
                    aka_log.log.error(f"{self.name} error connecting to "
                                      f"{self.host}:{self.port} [{reconnect_counter}]")
                else:
                    aka_log.log.error(f"{self.name} error connecting to "
                                      f"{self.http_url} [{reconnect_counter}]")
                reconnect_counter += 1
                self.connected = False
                time.sleep(uls_config.output_reconnect_delay)

            if self.connected is False and reconnect_counter > self.reconnect_retries:
                if not self.output_type == 'HTTP':
                    aka_log.log.critical(f"{self.name} not able to connect to "
                                         f"{self.host}:{self.port} - "
                                         f"giving up after {reconnect_counter - 1} retries.")
                else:
                    aka_log.log.critical(f"{self.name} not able to connect to {self.http_url} - "
                                         f"giving up after {reconnect_counter - 1} retries.")
                sys.exit(1)

    def send_data(self, data):
        """
        Transfer binary data towards the established TCP socket.
        We also try to handle issues across the connection (potential data loss?)
        :param data: binary
        :return: True on successful send, False on error
        """
        try:
            aka_log.log.info(f"{self.name} Trying to send data via {self.output_type}")

            if self.output_type == "TCP":
                self.clientSocket.sendall(data)

            elif self.output_type == "UDP":
                self.clientSocket.sendto(data, (self.host, self.port))

            elif self.output_type == "HTTP":
                response = self.httpSession.post(url=self.http_url,
                                                 data=self.http_out_format % (data.decode()),
                                                 verify=self.http_verify_tls,
                                                 timeout=self.http_timeout)
                aka_log.log.debug(f"{self.name} DATA Send response {response.status_code},"
                                  f" {response.text} ")

            elif self.output_type == "RAW":
                sys.stdout.write(data.decode())
                sys.stdout.flush()


            elif self.output_type == "FILE":
                self.my_file_writer.info(f"{data.decode().rstrip()}")

            else:
                aka_log.log.critical(f"{self.name} target was not defined {self.output_type} ")
                sys.exit(1)

            aka_log.log.info(f"{self.name} Data successfully sent via {self.output_type}")
            return True

        except Exception as my_error:
            aka_log.log.error(f"{self.name} Issue sending data {my_error}")
            self.connected = False
            self.connect()
            return False

    def tear_down(self):
        """
        Tear down all resources
        """
        if self.output_type == "TCP" or self.output_type == "UDP":
            aka_log.log.debug(f"{self.name} closing socket {self.clientSocket}")
            if self.clientSocket:
                self.clientSocket.close()
        if self.output_type == "HTTP":
            aka_log.log.debug(f"{self.name} closing HTTP Session {self.httpSession}")
            if self.httpSession:
                self.httpSession.close()
        self.connected = False

# EOF
