#!/usr/bin/env python3

# Common global variables / constants
__version__ = "0.0.2"
__tool_name_long__ = "Akamai Unified Log Streamer"
__tool_name_short__ = "ULS"


# Generic config
bin_python = "python3"                          # Python binary to use (use OS standard when not using path)
output_line_breaker = '\r\n'                    # Line breaking type (to split messages when streaming data)
    # EAA
bin_eaa_cli = "ext/cli-eaa/bin/akamai-eaa"      # Path to the EAA CLI Executable
eaa_cli_feeds = ['ACCESS', 'ADMIN']             # Available EAA CLI feeds
    # ETP
bin_etp_cli = "ext/cli-etp/bin/akamai-etp"      # Path to the ETP CLI Executable
etp_cli_feeds = ['THREAT', 'AUP']               # Available ETP CLI feeds
    # MFA
bin_mfa_cli = "ext/cli-mfa/bin/akamai-mfa"      # Path to the MFA CLI Executable
mfa_cli_feeds = ['POLICY', 'AUTH']              # Available MFA CLI feeds

    # INPUT Choices
input_choices = ['EAA', 'ETP', 'MFA']           # Available input types
input_format_choices = ['JSON', 'TEXT']         # Available input format choices (need to be supported by cli)

    # OUTPUT Choices
output_choices = ['TCP', 'HTTP', 'UDP']         # Definition of OUTPUT Choices

    # LogLevels
log_levels_available = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
log_level_default = 'WARNING'


# INPUT Configuration
input_rerun_retries = 3                         # Number of rerun attempts before giving up
input_run_delay = 1                             # Time in seconds to wait for the first health check
input_rerun_delay = 1                           # Time in seconds between rerun attempts


# OUTPUT Configuration
output_reconnect_retries = 10                   # Number of reconnect attempts before giving up
output_reconnect_delay = 1                      # Time in seconds between reconnect attempts
output_udp_send_buffer = 262144                 # UDP Send buffer in bytes
output_udp_timeout = 10.0                       # UDP SEND / CONNECT Timeout (seconds)
output_tcp_send_buffer = 262144                 # TCP Send buffer in bytes
output_tcp_timeout = 10.0                       # TCP SEND / CONNECT Timeout (seconds)
                                                # Additional Headers to send (requests module KV pairs)
output_http_header = {'User-Agent': f'{__tool_name_long__}/{__version__}'}


# Monitoring Configuration
monitoring_enabled = True                       # Set to false to disable monitoring outputs
monitoring_interval = 5 * 60                    # Monitoring output interval (seconds)
