#!/usr/bin/env python3

# Common global variables / constants
__version__ = "1.6.6"
__tool_name_long__ = "Akamai Unified Log Streamer"
__tool_name_short__ = "ULS"


# Generic config
bin_python = "python3"                          # Python binary to use (use OS standard when not using path)
output_line_breaker = '\r\n'                    # Line breaking type (to split messages when streaming data)
main_wait_default = 0.01                        # Default wait time within the main loop
main_wait_max = 60                              # Maximum wait time for the main loop
main_resend_attempts = 10                       # Maximum number of attempts to deliver the data
main_resend_exit_on_fail = False                # Stop program, if a single logline was not able to be delivered after $main_resend_attempts


    # EAA
        # Path to the EAA CLI Executable
bin_eaa_cli = "ext/cli-eaa/bin/akamai-eaa"
        # Available EAA CLI feeds
eaa_cli_feeds = ['ACCESS', 'ADMIN', 'CONHEALTH', 'DEVINV']

    # ETP
        # Path to the ETP CLI Executable
bin_etp_cli = "ext/cli-etp/bin/akamai-etp"
        # Available ETP CLI feeds
etp_cli_feeds = ['THREAT', 'AUP', 'DNS', 'PROXY', 'NETCON']

    # MFA
bin_mfa_cli = "ext/cli-mfa/bin/akamai-mfa"      # Path to the MFA CLI Executable
mfa_cli_feeds = ['EVENT']              # Available MFA CLI feeds

    # Guardicore
bin_gc_cli = "ext/cli-gc/bin/akamai-gc"                                         # Path to the GC CLI Executable
gc_cli_feeds = ['NETLOG', 'INCIDENT', 'AGENT', 'SYSTEM']                       # Available GC CLI feeds

    # LINODE
bin_linode_cli = "ext/cli-linode/bin/akamai-linode"         # Path to the LINODE CLI Executable
linode_cli_feeds = ['AUDIT']                        # Available LINODE CLI feeds

    # INPUT Choices
input_choices = ['EAA', 'ETP', 'MFA', 'GC', 'LINODE']           # Available input types
input_format_choices = ['JSON', 'TEXT']         # Available input format choices (need to be supported by cli)

    # OUTPUT Choices
output_choices = ['TCP', 'HTTP', 'UDP', 'RAW', 'FILE']         # Definition of OUTPUT Choices

    # Transformation Choices
transformation_choices = ['MCAS', 'JMESPATH']


    # LogLevels
log_levels_available = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
log_level_default = 'WARNING'

# INPUT Configuration
input_rerun_retries = 3                         # Number of rerun attempts before giving up
input_run_delay = 1                             # Time in seconds to wait for the first health check
input_rerun_delay = 1                           # Time in seconds between rerun attempts
input_disable_stderr = True                     # Enable STDERR output disabling (see value below to specify when this should happen)
input_disable_stderr_after = 25                 # Disable stderr output after x input_cli cycles --> to prevent buffer overflow
input_queue_size = 10000                        # Maximum number of events we want to store in-memory, default is 10000

# OUTPUT Configuration
output_reconnect_retries = 10                   # Number of reconnect attempts before giving up
output_reconnect_delay = 1                      # Time in seconds between reconnect attempts
    ## TCP / UDP
output_udp_send_buffer = 262144                 # UDP Send buffer in bytes
output_udp_timeout = 10.0                       # UDP SEND / CONNECT Timeout (seconds)
output_tcp_send_buffer = 262144                 # TCP Send buffer in bytes
output_tcp_timeout = 10.0                       # TCP SEND / CONNECT Timeout (seconds)
    ## HTTP
output_http_header = {'User-Agent': f'{__tool_name_long__}/{__version__}', 'Content-Type': 'application/json'}  # HTTP Additional Headers to send (requests module KV pairs)
output_http_timeout = 10                        # Timeout after which a request will be considered as failed
output_http_aggregate_count = 500               # Number of events to aggregate in POST request to HTTP Collector. 1 mean no aggregation
output_http_aggregate_idle = 5                  # Aggregate will send the data regardless of the count if the previous event was x secs ago
output_http_expected_status_code = 200          # Return Code for successful delivery
output_http_liveness_check = True               # Send an OPTIONS request to probe the HTTP Server is live
    ## FILE
output_file_encoding = "utf-8"                  # FILE Encoding setting
output_file_handler_choices = ['SIZE', 'TIME']  # Available Choices for the file handler
output_file_default_backup_count = 3                # Default number of backup files (after rotation)
output_file_default_maxbytes = 50 * 1024 * 1024     # Default maximum size of a file when rotated by the FILE - handler
output_file_default_time_use_utc = False            # Use UTC instead of local system time (Default: False)
output_file_time_choices = ['S','M','H','D','W0','W1','W2','W3','W4','W5','W6','MIDNIGHT']      # Available choices for the time unit
output_file_time_default = 'M'                      # Default value for the time unit (Minutes)
output_file_time_interval = 30                      # Default value for the interval (30)

# Monitoring Configuration
monitoring_enabled = True                       # Set to false to disable monitoring outputs
monitoring_interval = 5 * 60                    # Monitoring output interval (seconds)

# EDGERC_Checks
edgerc_openapi = ["host", "client_token", "client_secret", "access_token"]          # required fields for OPENAPI
edgerc_eaa_legacy = ["eaa_api_host", "eaa_api_key", "eaa_api_secret"]               # required for EAA - Legacy
edgerc_mfa = ["mfa_integration_id", "mfa_signing_key"]                              # Required for MFA
edgerc_gc = ["gc_username", "gc_password", "gc_hostname"]                           # Required for Guardicore
edgerc_linode = ["linode_hostname", "linode_token"]                                             # Required for Linode
edgerc_documentation_url = "https://github.com/akamai/uls/blob/main/docs/AKAMAI_API_CREDENTIALS.md"
edgerc_mock_file = "ext/edgerc"                  # Required for display the version if no edgercfile was given

# Autoresume Configuration
autoresume_checkpoint_path = "var/"              # (Default) Path, where the checkpointfiles should be stored to
autoresume_supported_inputs = ['ETP', 'EAA']     # Internal Var only, to adjust supported inputs
autoresume_write_after = 1000                    # Write checkpoint only every ${autoresume_write_every} loglines

