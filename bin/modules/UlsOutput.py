#!/usr/bin/env python3

import socket
import requests
import ast
import sys
import time
import threading

# ULS specific modules
import modules.aka_log as aka_log
import config.global_config as uls_config

stopEvent = threading.Event()


class UlsOutput:

    def __init__(self):
        # Variables (load from uls_config)
        self.reconnect_retries = uls_config.output_reconnect_retries    # Number of reconnect attempts before giving up
        self.udp_send_buffer = uls_config.output_udp_send_buffer        # UDP Send buffer in bytes
        self.udp_timeout = uls_config.output_udp_timeout                # UDP SEND / CONNECT Timeout (seconds)
        self.tcp_send_buffer = uls_config.output_tcp_send_buffer        # TCP Send buffer in bytes
        self.tcp_timeout = uls_config.output_tcp_timeout                # TCP SEND / CONNECT Timeout (seconds)
        self.http_header = uls_config.output_http_header                # Additional Headers

        # Defaults (may vary later)
        self.name = "UlsOutput"                 # Class Human readable name
        self.http_verify_tls = False            # whether to verify the Certificate CA (True) or not (False)
        self.connected = False                  # Internal Connection tracker - do not touch
        self.output_type = None
        self.http_out_format = None
        self.http_url = None
        self.httpSession = None
        self.port = None
        self.host = None
        self.clientSocket = None

    def connect(self, output_type: str, host: str, port: int,
                http_out_format=None,
                http_out_auth_header=None,
                http_url=None,
                http_insecure=False):
        """
        Connecting the tcp output socket. in addition we've added some error/reconnection handling
        :param output_type: The desired output format (TCP/ UDP / HTTP)
        :param host: hostname or ip address (TCP/UDP)
        :param port: tcp port number (TCP/UDP)
        :param http_url: URL (scheme://host:port/path) (HTTP)
        :param http_out_format: HTTP Output format ((HTTP)
        :param http_out_auth_header: HTTP Authentication header (HTTP)
        :param http_insecure: (bool) Disable TLS verification (HTTP)
        :return:
        """

        reconnect_counter = 1
        while not stopEvent.is_set() and self.connected is False and reconnect_counter <= self.reconnect_retries:
            # Check & set output type
            if output_type in ['TCP', 'HTTP', 'UDP']:
                self.output_type = output_type
                aka_log.log.debug(f"{self.name} Selected Output Type: {self.output_type} ")
            else:
                aka_log.log.critical(f"{self.name} target was not defined {output_type} ")
                sys.exit(1)
            try:
                # TCP Connector
                if self.output_type == "TCP":
                    # add a check if required vars are set
                    aka_log.log.debug(f"{self.name} attempting to connect via TCP to {host}:{port} ")
                    self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # check
                    self.clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.tcp_send_buffer)
                    self.clientSocket.connect((host, port))
                    self.clientSocket.settimeout(self.tcp_timeout)
                    reconnect_counter = 1
                    self.connected = True
                    aka_log.log.info(f"{self.name} successful connected to tcp://{host}:{port} ")

                # UDP Connector
                if self.output_type == "UDP":
                    aka_log.log.debug(f"{self.name} attempting to connect via UDP to {host}:{port} ")
                    self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    self.host = host
                    self.port = port
                    self.clientSocket.settimeout(self.udp_timeout)
                    self.clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.udp_send_buffer)
                    reconnect_counter = 1
                    self.connected = True
                    aka_log.log.info(f"{self.name} successful connected to udp://{host}:{port} ")

                # HTTP Connector
                if self.output_type == "HTTP":
                    self.httpSession = requests.session()
                    # Prepare & set the headers
                    if http_out_auth_header:
                        headers = self.http_header | ast.literal_eval(http_out_auth_header)
                    else:
                        headers = self.http_header
                    aka_log.log.debug(f"{self.name} adding http headers: {headers}")
                    self.httpSession.headers.update(headers)
                    # Output Format
                    self.http_out_format = http_out_format
                    aka_log.log.debug(f"{self.name} setting http output format: {self.http_out_format}")
                    # TLS Verification
                    if http_insecure:
                        # DISABLE insecure warnings (if verify=FALSE)
                        requests.packages.urllib3.disable_warnings()
                        self.http_verify_tls = False    # Use the inverted boolean expression ;)
                        aka_log.log.debug(
                            f"{self.name} TLS CA Certificate verification has been disabled - this is insecure !!")
                    elif not http_insecure:
                        self.http_verify_tls = True
                        aka_log.log.debug(
                            f"{self.name} TLS CA Certificate verification is turned on.")
                    else:
                        aka_log.log.critical(f'{self.name} HTTP insecure was not set to a boolean value (True|False) '
                                             f'- we got "{http_insecure}" instead')
                        sys.exit(1)
                    # Check the URL
                    if not http_url:
                        aka_log.log.critical(f'{self.name} HTTP output selected but no URL given. '
                                             f'Use --httpurl instead of --host / --port')
                        sys.exit(1)
                    else:
                        aka_log.log.debug(f"{self.name} attempting to connect via HTTP to {http_url} ")

                    # Let'S do an options request
                    self.http_url = http_url
                    resp = self.httpSession.options(url=self.http_url, data='{"event":"connection test"}',
                                                    verify=self.http_verify_tls)

                    if resp.status_code == 200:
                        reconnect_counter = 1
                        self.connected = True
                        aka_log.log.info(f"{self.name} successful connected to {self.http_url} ")
                    else:
                        aka_log.log.error(f"{self.name} error connecting to {self.http_url}. "
                                          f"StatusCode: {resp.status_code} Reason: {resp.text} [{reconnect_counter}]")
                        time.sleep(uls_config.output_reconnect_delay)
                        self.connected = False
                        reconnect_counter = 1

            except Exception as con_error:
                aka_log.log.debug(f"{self.name} issue: {con_error}")
                if not self.output_type == 'HTTP':
                    aka_log.log.error(f"{self.name} error connecting to {host}:{port} [{reconnect_counter}]")
                else:
                    aka_log.log.error(f"{self.name} error connecting to {self.http_url} [{reconnect_counter}]")
                reconnect_counter += 1
                self.connected = False
                time.sleep(uls_config.output_reconnect_delay)

            if self.connected is False and reconnect_counter > self.reconnect_retries:
                if not self.output_type == 'HTTP':
                    aka_log.log.critical(f"{self.name} not able to connect to {host}:{port} - "
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
        :return:
        """
        try:
            if self.output_type == "TCP":
                self.clientSocket.sendall(data)

            elif self.output_type == "UDP":
                self.clientSocket.sendto(data, (self.host, self.port))

            elif self.output_type == "HTTP":
                response = self.httpSession.post(url=self.http_url,
                                                 data=self.http_out_format % (data.decode()),
                                                 verify=self.http_verify_tls)
                aka_log.log.debug(f"{self.name} DATA Send response {response.status_code},"
                                  f" {response.text} ")
            else:
                aka_log.log.critical(f"{self.name} target was not defined {self.output_type} ")
                sys.exit(1)
        except Exception as my_error:
            aka_log.log.error(f"{self.name} Issue sending data {my_error}")
            self.connected = False

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
# EOF
