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

import ast
import json
import sys
import time

# ULS modules
import config.transformation_config as transform_config
import jmespath
import modules.aka_log as aka_log


class UlsTransformation:
    """
    UlsTransform Class
    """
    def __init__(self, transformation, product, feed, cliformat,
                 transformationpattern=None):
        """
        :param transformation: Specify a supported transformation (MCAS)
        :param product: Provide the selected INPUT (for sanity checks)
        :param feed: Provide the selected FEED (for sanity checks)
        :param cliformat: Provide the selected CLIFORMAT (for sanity checks)
        """
        self.transformation = transformation
        self.product = product
        self.feed = feed
        self.cliformat = cliformat
        self.transformationpattern = transformationpattern

        # Defaults (may vary later)
        self.name = "UlsTransformation"

        if not self.transformation:
            aka_log.log.debug(f'{self.name} - No Transformation loaded')
        else:
            self._preflight_check()

    def _preflight_check(self):
        if self.transformation == "MCAS":
            if self.product in transform_config.mcas_required_input and \
                    self.feed in transform_config.mcas_required_feed and \
                    self.cliformat in transform_config.mcas_required_cliformat:

                aka_log.log.info(f'{self.name} - {transform_config.mcas_name_long} '
                                 f'[{self.transformation}] - Preflight check ok - Transformation loaded')

            else:
                aka_log.log.critical(f'{self.name} - transformation '
                                     f'{transform_config.mcas_name_long} [{self.transformation}] '
                                     f'specified, but wrong input/feed or format defined. '
                                     f'MCAS only supports Input: '
                                     f'{transform_config.mcas_required_input} '
                                     f'Feed: {transform_config.mcas_required_feed} '
                                     f'Cliformat: {transform_config.mcas_required_cliformat} '
                                     f'- (exiting)')
                sys.exit(1)


        elif self.transformation == "JMESPATH":
            if self.cliformat in transform_config.jmespath_required_cliformat and \
                    self.transformationpattern:
                try:
                    import jmespath
                except Exception as my_error:
                    aka_log.log.critical(f"{self.name} - {self.transformation} transformation "
                                        f"R"
                                         f"requires python module 'jmespath' which is not installed."
                                        f"Please run 'pip3 install jmespath' "
                                        f"Error: ({my_error}) - exiting.")
                    sys.exit(1)

                self.transformationpattern_compiled = jmespath.compile(self.transformationpattern)

                aka_log.log.info(f'{self.name} - {transform_config.jmespath_name_long} '
                                 f'[{self.transformation}] - Preflight check ok - Transformation loaded')

            else:
                aka_log.log.critical(f'{self.name} - transformation '
                                     f'{transform_config.jmespath_name_long} [{self.transformation}] '
                                     f'specified, but wrong params given format defined. (Inputformat/pattern)'
                                     f'{transform_config.jmespath_name_short} only supports '
                                     f'Cliformat: {transform_config.jmespath_required_cliformat} '
                                     f'Transformation pattern given: {self.transformationpattern} - (exiting)')
                sys.exit(1)


    def transform(self, log_line):
        """
        :param log_line: The logline to transform
        :return: The transformed logline
        """
        my_output = None
        
        try:
            aka_log.log.info(f'{self.name} - Transformation for '
                             f'{self.product}-{self.feed} --> {self.transformation} starting')

            # MCAS Transformation
            if self.transformation == "MCAS":
                my_output = self._mcas_transformation(log_line)

            # JMESPATH Transformation
            elif self.transformation == "JMESPATH":
                my_output = self._jmespath_transformation(log_line, self.transformationpattern_compiled)

            # Return the data after successful transformation
            aka_log.log.info(f'{self.name} - Transformation for '
                             f'{self.product}-{self.feed} --> '
                             f'{self.transformation} successfully done.')

            aka_log.log.debug(f'{self.name} - Transformed message: {my_output}')

            # Return the data (byte encoded)
            return my_output.encode()

        except Exception as my_error:
            aka_log.log.warning(f"{self.name} - Transformation "
                                f"({self.product}-{self.feed} --> {self.transformation}) "
                                f"somehow crashed/failed: ({my_error})- "
                                f"Discarded message: {log_line}")
            return "".encode()

    def _epochtime(self,
                   timestamp,
                   timestamp_format='%Y-%m-%dT%H:%M:%SZ'
                   ):
        """
        This method will return the epoch_time based on the given timestamp & format
        :param timestamp: The Timestamp in the given format
        :param timestamp_format: Format, the timestamp has been handed over
        :return: integer of epochtime
        """
        return int(time.mktime(time.strptime(timestamp, timestamp_format)))

    def _mcas_transformation(self, log_line):
        """
        This method will transform the given log_line (json format) into MCAS format
        :param log_line: json logline
        :return: MCAS format (agreed with Microsoft)
        """
        try:
            # Setting the defaults
            detection_time = None
            client_ip = None
            destination_ip = None
            domain = None
            user_name = None
            bytes_uploaded = 0
            bytes_downloaded = 0
            bytes_total = 0
            action = None

            # Decode the data into json
            data = json.loads(log_line.decode())
            
            # DNS --> MCAS
            if self.feed == "DNS":
                detection_time = self._epochtime(data['query']['time'])
                client_ip = data['query']['clientIp']
                destination_ip = data['query']['resolved'][0]['response']
                domain = data['query']['domain']
                user_name = data['query']['deviceOwnerId'] or None
                bytes_uploaded = 0
                bytes_downloaded = 0
                bytes_total = 0
                action = data['event']['actionName']

            # PROXY --> MCAS
            elif self.feed == "PROXY":
                detection_time = self._epochtime(data['event']['detectionTime'])
                client_ip = data['event']['internalClientIP']
                destination_ip = data['request']['destinationIP']
                domain = data['request']['domain']
                user_name = data['userIdentity']['encryptedUserID'] or None
                bytes_uploaded = 0
                bytes_downloaded = 0
                bytes_total = 0
                action = data['event']['actionName']

            else:
                aka_log.log.warning(f'{self.name} - Transformation ({self.transformation}) '
                                    f'transformation triggered but '
                                    f'no valid transformation found ... ')

            my_output = transform_config.mcas_input_format.format(detection_time, client_ip, destination_ip, domain, user_name, bytes_uploaded, bytes_downloaded, bytes_total, action)
            
            return my_output

        except Exception as my_error:
            aka_log.log.warning(f"{self.name} - {self.transformation} transformation "
                                f"({self.product}-{self.feed} --> {self.transformation}) "
                                f"somehow crashed/failed: ({my_error})- "
                                f"Discarded message: {log_line}")
            return False

    def _jmespath_transformation(self, log_line, expression):

        # Decode the data into json
        data = json.loads(log_line.decode())
        my_output = expression.search(data)


        return str(my_output)

# EOF
