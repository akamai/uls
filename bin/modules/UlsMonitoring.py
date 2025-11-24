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
import psutil

import modules.aka_log as aka_log
import uls_config.global_config as uls_config
import modules.UlsTools as UlsTools

class UlsMonitoring:

    def __init__(self, stopEvent, product, feed, output,
                 prom_enabled: bool = False,
                 prom_port: int = 8000,
                 prom_host: str = '127.0.0.1',
                 prom_certfile: str = None,
                 prom_keyfile: str = None,
                 nocallhome: bool = False,):
        """
        Hanlde ULS self monitoring, spills out performance counter on stdout.

        Args:
            stopEvent (threading.Event): Event from the controlling thread to tell the monitoring to stop
            product (string): Akamai Product name/acronym
            feed (string): specific data feed being consumed by ULS
        """

        # Core monitoring stuff
        self._stopEvent = stopEvent
        self._product = product
        self._feed = feed
        self._output = output

        # Prometheues
        self.prometheues_enabled = prom_enabled
        self.promeuteheus_port = prom_port
        self.promeuteheus_host = prom_host
        self.promeuteheus_cert = prom_certfile
        self.promeuteheus_key = prom_keyfile

        self.prom_checkpoint = None
        self.prom_overall_messages = None
        self.prom_overall_bytes = None
        self.prom_overall_messages_ingested = None
        # Prevent other thread interact with the performance counters
        self._metricLock = threading.Lock()

        # Variables
        self.monitoring_enabled = uls_config.monitoring_enabled                     # Monitoring enable Flag
        self.monitoring_interval = uls_config.monitoring_interval                   # Monitoring interval
        self._version = uls_config.__version__

            # Callhome
        self.nocallhome = nocallhome                                                # Callhome enabled or disabled
        self.callhome_stats_enabled = uls_config.callhome_stats_enabled             # Is the Callhome stats function enabled
        self.callhome_stats_aggregate_count = uls_config.callhome_stats_aggregate_count     # Number of "stat" iteration to pause between sending data
        self.callhome_stat_count = 1                       # Starting point for the callhome stats

            # CPU & Memory
        self.cpu_samples = []
        self.mem_samples = []

            # Definitions
        self.name = "UlsMonitoring"                          # Class Human readable name
        self.overall_messages_handled = 0                    # Define overall number of messages handled
        self.overall_bytes_handled = 0                       # DEfine overall number of bytes handled
        self.window_messages_handled = 0                     # Define mon_window number of messages handled
        self.window_messages_bytes = 0                       # Total bytes processed during the window
        self.window_messages_ingested = 0                    # Message ingested from UlsInputCli module
        self.init_time = time.time()                         # Define the init time
        self.checkpoint = None                               # Last checkpoint
        self.checkpoint_lastwrite = None                     # Last time, the heckpoint was updated

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

        if self.prometheues_enabled:
            aka_log.log.debug(f"{self.name} Prometheus monitoring started...")
            self.start_prometheus(port=self.promeuteheus_port, host=self.promeuteheus_host, cert=self.promeuteheus_cert, key=self.promeuteheus_key)

    def start_prometheus(self, port, host="127.0.0.1", cert=None, key=None):
        from prometheus_client import start_http_server
        from prometheus_client import Info, Counter, Gauge
        from prometheus_client import REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR

        # Disable unwanted collectors
        REGISTRY.unregister(PROCESS_COLLECTOR)
        REGISTRY.unregister(PLATFORM_COLLECTOR)
        REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_objects_collected_total'])

        # Start the Server
        server, t = start_http_server(port=port, addr=host, certfile=cert, keyfile=key)
        server.base_environ.clear()

        # Show the version
        version = Info('uls_version', 'The current ULS Version')
        version.info({'version': uls_config.__version__})

        uls_stream_info = Info('uls_stream_info', "The selected ULS input product")
        uls_stream_info.info({'product': self._product, 'feed': self._feed, 'output': self._output})

        starttime = Info('uls_starttime', "The time, the uls process was started")
        starttime.info({'starttime': f'{self.init_time}'})

        self.prom_checkpoint = Info(name='uls_checkpoint', documentation='The current ULS checkpoint info')



        # Counters
        self.prom_overall_messages = Counter('uls_overall_messages_incoming', 'Number of all handled incoming log lines')
        self.prom_overall_bytes = Counter('uls_overall_bytes_incoming', 'Size of all handled incoming log lines')
        self.prom_overall_messages_ingested = Counter('uls_overall_messages_ingested', 'Number of all handled outgoing log lines')


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
                        'dt': datetime.datetime.now(datetime.UTC).isoformat(),
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
                        'mon_interval': self.monitoring_interval,
                        'cpu_usage': round(sum(self.cpu_samples) / (self.window_messages_handled | 1), 2),
                        'mem_usage': round(sum(self.mem_samples) / (self.window_messages_handled | 1), 2),
                        'current_checkpoint': self.checkpoint,
                        'checkpoint_lastupdate': self.checkpoint_lastwrite
                    }

                    # --- Handle Callhome stats (if enabled)
                    if self.callhome_stats_enabled and not self.nocallhome:
                        # --- we reached the stats_aggregate_count and need to generate a callhome message now
                        if self.callhome_stat_count == self.callhome_stats_aggregate_count:
                            aka_log.log.debug(f"{self.name} Callhome stats agg_count reached - we need to send a stats message now")
                            UlsTools.callhome(
                                nocallhome_state=self.nocallhome,
                                position="stats",
                                callhome_data={
                                    'input': self._product,
                                    'feed': self._feed,
                                    'output': self._output,
                                    'runtime': self._runtime(),
                                    'event_count': self.overall_messages_handled,
                                    'event_bytes': self.overall_bytes_handled,
                                    'mon_interval': self.monitoring_interval * self.callhome_stats_aggregate_count,
                                })
                            self.callhome_stat_count = 1
                        else:
                            self.callhome_stat_count += 1
                    else:
                        aka_log.log.debug(f"{self.name} Callhome stats functionality is disabled.")
                    # --- End of the callhome block

                    # --- Write the logging output to the console / stdout
                    sys.stdout.write(json.dumps(mon_msg) + "\n")
                    sys.stdout.flush()

                    # Reset window based vars
                    with self._metricLock:
                        self.window_messages_handled = 0
                        self.window_messages_bytes = 0
                        self.window_messages_ingested = 0
                        self.cpu_samples = []
                        self.mem_samples = []

        except Exception as e:
            aka_log.log.exception(e)

    def increase_message_count(self, bytes=0):
        with self._metricLock:
            self.overall_messages_handled = self.overall_messages_handled + 1
            self.window_messages_handled = self.window_messages_handled + 1
            self.window_messages_bytes += bytes
            self.overall_bytes_handled += bytes

            # Also increase the prom counters
            if self.prometheues_enabled:
                self.prom_overall_messages.inc()
                self.prom_overall_bytes.inc(bytes)

            # Let's also collect some CPU & MEMORY USAGE
            # note ty myself: not sure this is the best place to measure the cpu / mem but it's a good start
            self.cpu_samples.append(psutil.cpu_percent(interval=None))
            self.mem_samples.append(psutil.virtual_memory().percent)


    def increase_message_ingested(self):
        with self._metricLock:
            self.window_messages_ingested += 1

            if self.prometheues_enabled:
                self.prom_overall_messages_ingested.inc()


    def get_message_count(self):
        return self.overall_messages_handled

    def get_stats(self):
        with self._metricLock:
            return f"event_count={self.overall_messages_handled}, runtime={self._runtime()}"

    def _runtime(self):
        return int(time.time() - self.init_time)


    def update_checkpoint(self, checkpoint: str=None):
        """
        Update the checkpoint value we show in the monitoring output
        """
        self.checkpoint = checkpoint
        self.checkpoint_lastwrite = datetime.datetime.now(datetime.UTC).isoformat()

        if self.prometheues_enabled:
            self.prom_checkpoint.info({'checkpoint': str(self.checkpoint), 'last_update': str(self.checkpoint_lastwrite)})
# EOF

