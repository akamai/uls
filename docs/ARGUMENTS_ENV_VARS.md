# List of parameters / Environmental variables
The following tables list all available command line parameters and their corresponding environmental variables (for advanced usage).


## Global
|Parameter|Env - Var|Options|Default|Description|
|---|---|---|---|---|
|-h <br> --help | n/a | n/a | None | Display help / usage information |
|-l <br> --loglevel | ULS_LOGLEVEL | 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' | WARNING | Adjust the overall loglevel |
|-v <br> --version| n/a | n/a | None | Display ULS version information (incl. CLI & OS versions) |


## INPUT
|Parameter|Env - Var|Options|Default|Description|
|---|---|---|---|---|
|-i <br> --input | ULS_INPUT | 'EAA', 'ETP', 'MFA' | None | Specify the desired INPUT source |
|--feed | ULS_FEED | EAA: 'ACCESS', 'ADMIN', 'CONHEALTH'<br> ETP: 'THREAT', 'AUP'<br> MFA: 'AUTH','POLICY' | None | Specify the desired INPUT feed |
|--format | ULS_FORMAT | 'JSON', 'TEXT' | JSON | Specify the desired INPUT (=OUTPUT) format |
|--inproxy<br>--inputproxy | ULS_INPUT_PROXY | HOST:PORT| None | Adjust proxy usage for INPUT data collection (cli) |
|--rawcmd | ULS_RAWCMD | \<cli command\> | None | USE with caution /!\ <br> This is meant only to be used when told by AKAMAI [Click here for more information](ADDITIONAL_FEATURES.md#rawcmd---rawcmd-feature)|
|--edgerc | ULS_EDGERC | /path/to/your/.edgerc | '~/.edgerc' | Specify the location of the .edgerc EDGE GRID AUTH file |
|--section | ULS_SECTION | edgerc_config_section | 'default' | Specify the desired section within the .edgerc file |

## OUTPUT
|Parameter|Env - Var|Options|Default|Description|
|---|---|---|---|---|
|-o <br> --output| ULS_OUTPUT | 'TCP', 'UDP', 'HTTP', 'RAW' | None | Specify the desired OUTPUT target |
|--host | ULS_OUTPUT_HOST | xxx.xxx.xxx.xxx | None | Specify the desired OUTPUT target host (TCP/UDP only) |
|--port| ULS_OUTPUT_PORT | xxxx | None | Specify the desired OUTPUT target port (TCP/UDP only) |
|--filter| ULS_OUTPUT_FILTER | \<regular expression\> | None | Filter (regex) to reduce number of sent log files (Only send lines that match the --filter argument) [Click here for more information](ADDITIONAL_FEATURES.md#filter---filter-feature)|
|--httpurl| ULS_HTTP_URL | http(s)://\<host\>:\<port\>/\<path\> | None | The HTTP target URL. (HTTP only) <br> Do not use --host / --port for HTTP|
|--httpformat| ULS_HTTP_FORMAT| '<http_output_format>'|'{"event": %s}'| Specify the expected output format (i.e. json) where %s will be replaced with the event data.
|--httpauthheader| ULS_HTTP_AUTH_HEADER | '{"Authorization": "VALUE"}' | None | Specify an Auhtorization header to auth against the HTTP Server (HTTP only) <br>Example:<br>'{"Authorization": "Splunk xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"}' |
|--httpinsecure| ULS_HTTP_INSECURE | True | False | Disable TLS CA certificate verification |
