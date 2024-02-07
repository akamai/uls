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

import time
import threading
import json
import datetime
import sys

import modules.aka_log as aka_log
import uls_config.global_config as uls_config


class UlsMonitoring:

    def __init__(self, stopEvent, product, feed, output):
        """
        Hanlde ULS self monitoring, spills out performance counter on stdout.

        Args:
            stopEvent (threading.Event): Event from the controlling thread to tell the monitoring to stop
            product (string): Akamai Product name/acronym
            feed (string): specific data feed being consumed by ULS
        """

        self._stopEvent = stopEvent
        self._product = product
        self._feed = feed
        self._output = output

        # Prevent other thread interact with the performance counters
        self._metricLock = threading.Lock()

        # Variables
        self.monitoring_enabled = uls_config.monitoring_enabled                     # Monitoring enable Flag
        self.monitoring_interval = uls_config.monitoring_interval                    # Monitoring interval
        self._version = uls_config.__version__

        # Definitions
        self.name = "UlsMonitoring"                          # Class Human readable name
        self.overall_messages_handled = 0                    # Define overall number of messages handled
        self.window_messages_handled = 0                     # Define mon_window number of messages handled
        self.window_messages_bytes = 0                       # Total bytes processed during the window
        self.window_messages_ingested = 0                    # Message ingested from UlsInputCli module
        self.init_time = time.time()                         # Define the init time

        # Define the working thread, daemon allows us to offload
        # of the main program termination to python
        self.mon_thread = threading.Thread(target=self.display, daemon=True)

    def start(self):
        if self.monitoring_enabled:
            aka_log.log.debug(f"{self.name} monitoring thread started...")
            # Start the background thread
            self.mon_thread.start()
        else:
            aka_log.log.debug(f"{self.name} monitoring was disabled - not starting.")

    def display(self):
        """
        Entry point for the monitoring thread
        """
        try:  # Exception handling is crucial once on the thread
            while not self._stopEvent.is_set():
                aka_log.log.debug(f"{self.name} sleeping {self.monitoring_interval} sec...")
                # Wait return True unless the timer expired, which is when
                # ULS is still active and we safely report the activity
                if not self._stopEvent.wait(self.monitoring_interval):
                    mon_msg = {
                       'dt': datetime.datetime.utcnow().isoformat(),
                       'uls_product': self._product,
                       'uls_feed': self._feed,
                       'uls_output': self._output,
                       'uls_version': self._version,
                       'uls_runtime': self._runtime(),
                       'event_count': self.overall_messages_handled,
                       'event_count_interval': self.window_messages_handled,
                       'event_ingested_interval': self.window_messages_ingested,
                       'event_bytes_interval': self.window_messages_bytes,
                       'event_rate': round(self.window_messages_handled / self.monitoring_interval, 2),
                       'mon_interval': self.monitoring_interval
                    }
                    #print(json.dumps(mon_msg))
                    sys.stdout.write(json.dumps(mon_msg) + "\n")
                    sys.stdout.flush()

                    # Reset window based vars
                    with self._metricLock:
                        self.window_messages_handled = 0
                        self.window_messages_bytes = 0
                        self.window_messages_ingested = 0
        except Exception as e:
            aka_log.log.exception(e)

    def increase_message_count(self, bytes=0):
        with self._metricLock:
            self.overall_messages_handled = self.overall_messages_handled + 1
            self.window_messages_handled = self.window_messages_handled + 1
            self.window_messages_bytes += bytes

    def increase_message_ingested(self):
        with self._metricLock:
            self.window_messages_ingested += 1


    def get_message_count(self):
        return self.overall_messages_handled

    def get_stats(self):
        with self._metricLock:
            return f"event_count={self.overall_messages_handled}, runtime={self._runtime()}"

    def _runtime(self):
        return int(time.time() - self.init_time)

# EOF

