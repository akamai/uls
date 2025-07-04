# List of parameters / Environmental variables
The following tables list all available command line parameters and their corresponding environmental variables (for advanced usage).

## Table of contents
- [Global](#global)
- [Input](#input)
- [Output](#output)
- [Special Arguments](#special-arguments)
- [Autoresume](#autoresume)

---

## Global

| Parameter          | Env - Var          | Options                                                                          | Default               | Description                                                                                                                                                      |
|--------------------|--------------------|----------------------------------------------------------------------------------|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -h <br> --help     | n/a                | n/a                                                                              | None                  | Display help / usage information                                                                                                                                 |
| -l <br> --loglevel | ULS_LOGLEVEL       | 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'                                  | WARNING               | Adjust the overall loglevel                                                                                                                                      |
| --json-log         | ULS_JSONLOG        | 'True', 'False'                                                                  | False                 | Should ULS write its own logdata in JSON format  instead of plain text output ?                                                                                  |
| --ulslogformat     | ULS_LOGFORMAT      | 'yourlogformatstring'                                                            | False                 | Custom logging format (ULS internal logs) see [additional features documentation](ADDITIONAL_FEATURES.md#uls-logformat) for more information -  (Default: False) |
| --ulslogdatefmt    | ULS_LOG_DATEFORMAT | All [STRFTIME](https://docs.python.org/3/library/time.html#time.strftime) option | "%Y-%m-%d %H:%M:%S%z" | djust the logging date/time format to your needs,                                                                                                                |
| -v <br> --version  | n/a                | n/a                                                                              | None                  | Display ULS version information (incl. CLI & OS versions)                                                                                                        |
| --debugloglines    | ULS_DEBUGLOGLINES  | 'True', 'False'                                                                  | False                 | Should the debug log contain Loglines (useful to debug transformations)                                                                                          |
| --nocallhome       | ULS_NOCALLHOME     | 'True', 'False'                                                                  | False                 | Disable the ULS CallHome feature that helps the ULS developers to continue improving ULS. (enabled by default)                                                   |
| --clidebug         | ULS_CLIDEBUG       | 'True', 'False'                                                                  | False                 | Turn on [DEBUG output of the underlying CLI](DEBUGGING.md#clidebug-mode). This setting will only work with RAW OUTPUT (for security reasons) !                   |


## INPUT

| Parameter                 | Env - Var       | Options                                                                                                                                                                                                                  | Default       | Description                                                                                                                                                                                 |
|---------------------------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -i <br> --input           | ULS_INPUT       | 'EAA', 'ETP', 'MFA', 'GC', 'LINODE', 'ACC'                                                                                                                                                                               | None          | Specify the desired INPUT source                                                                                                                                                            |
| --feed                    | ULS_FEED        | EAA: 'ACCESS', 'ADMIN', 'CONHEALTH', 'DEVINV'<br><br> ETP: 'THREAT', 'AUP', 'DNS', 'PROXY'<br><br> MFA: 'EVENT'<br><br> GC: 'NETLOG', 'INCIDENT', 'AGENT', 'SYSTEM', 'AUDIT'<br><br> LINODE: 'AUDIT'<br><br> ACC: 'EVENTS' | None          | Specify the desired INPUT feed                                                                                                                                                              |
| --format                  | ULS_FORMAT      | 'JSON', 'TEXT'                                                                                                                                                                                                           | JSON          | Specify the desired INPUT (=OUTPUT) format                                                                                                                                                  |
| --inproxy<br>--inputproxy | ULS_INPUT_PROXY | HOST:PORT                                                                                                                                                                                                                | None          | Adjust proxy usage for INPUT data collection (cli) <br>If this parameter does not work as expected, [please read more about it here](./FAQ.md#--inputproxy-proxy-does-not-work-as-expected) |
| --rawcmd                  | ULS_RAWCMD      | \<cli command\>                                                                                                                                                                                                          | None          | USE with caution /!\ <br> This is meant only to be used when told by AKAMAI [Click here for more information](ADDITIONAL_FEATURES.md#rawcmd---rawcmd-feature)                               |
| --edgerc                  | ULS_EDGERC      | /path/to/your/.edgerc                                                                                                                                                                                                    | '~/.edgerc'   | Specify the location of the .edgerc EDGE GRID AUTH file                                                                                                                                     |
| --section                 | ULS_SECTION     | edgerc_config_section                                                                                                                                                                                                    | 'default'     | Specify the desired section within the .edgerc file                                                                                                                                         |
| --starttime               | ULS_STARTTIME   | EPOCH timestamp (in seconds)                                                                                                                                                                                             | `cli_default` | Specify an EPOCH timestamp from where to start the log collection.                                                                                                                          |
| --endtime                 | ULS_ENDTIME     | EPOCH timestamp (in seconds)                                                                                                                                                                                             | None          | Specify an EPOCH timestamp up until where to fetch logs. ULS will exit after reaching this point.<br>ULS will not continue reading logs on CLI errors !!!                                   |
| --inputqueuesize | ULS_INPUT_QUEUESIZE | INPUT_QUEUE_SIZE(int)                                                                                                                                                                                                    | 15000 | Maximum threshold of the input queue. When threshold is reached, ULS will stop operations and exit "Capacity exceeded, too many incoming data vs. slow output" |


## OUTPUT

| Parameter        | Output Type | Env - Var            | Options                                | Default                  | Description                                                                                                                                                                                                                                                                                      |
|------------------|-------------|----------------------|----------------------------------------|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -o <br> --output |             | ULS_OUTPUT           | 'TCP', 'UDP', 'HTTP', 'RAW', 'FILE'    | None                     | Specify the desired OUTPUT target                                                                                                                                                                                                                                                                |
 |             |                      |                                       |                                        |                                                                                                                                                                                                                                                                                                  |
| --host           | TCP / UDP   | ULS_OUTPUT_HOST      | xxx.xxx.xxx.xxx                        | None                     | Specify the desired OUTPUT target host (TCP/UDP only)                                                                                                                                                                                                                                            |
| --port           | TCP / UDP   | ULS_OUTPUT_PORT      | xxxx                                   | None                     | Specify the desired OUTPUT target port (TCP/UDP only)                                                                                                                                                                                                                                            |
| --tcpudpformat  | TCP / UDP   | ULS_TCPUDP_FORMAT    | '<tcpudp_output_format>'               | '%s'                     | Specify the expected output format (e.g. json) where %s will be replaced with the event data. /!\ %s can only be used once                                                                                                                                                                                                                                                                                                 |
|                  |             |                      |                                        |                          |                                                                                                                                                                                                                                                                                                  |
| --httpurl        | HTTP(S)     | ULS_HTTP_URL         | http(s)://\<host\>:\<port\>/\<path\>   | None                     | The HTTP target URL. (HTTP only) <br> Do not use --host / --port for HTTP                                                                                                                                                                                                                        |
| --httpformat     | HTTP(S)     | ULS_HTTP_FORMAT      | '<http_output_format>'                 | '{"event": %s}'          | Specify the expected output format (e.g. json) where %s will be replaced with the event data. /!\ %s can only be used once                                                                                                                                                                       |
| --httpauthheader | HTTP(S)     | ULS_HTTP_AUTH_HEADER | '{"Authorization": "VALUE"}'           | None                     | Specify an Auhtorization header to auth against the HTTP Server (HTTP only) <br>Example:<br>'{"Authorization": "Splunk xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"}'                                                                                                                                        |
| --httpinsecure   | HTTP(S)     | ULS_HTTP_INSECURE    | True                                   | False                    | Disable TLS CA certificate verification                                                                                                                                                                                                                                                          |
| --httpliveness | HTTP(S) | ULS_HTTP_LIVENESS_CHECK | True, False                            | True | Perform liveness check with OPTIONS request that must return 200 or 204 if enabled|
| --httpaggregate  | HTTP(S)     | ULS_HTTP_AGGREGATE   | xxxx                                   | 500                      | Number of events to aggregate for one output request the %s in the httpformat will be replaced by a LIST of events.<br> A value of 1 means no aggregation.<br>Example: %s = [{'event1': 'data1'},{'event2': 'data2'},...]                                                |
| --httpformattype | HTTP(S) | ULS_HTTP_FORMAT_TYPE | 'JSON-LIST',SINGLE-EVENT'              | 'JSON-LIST' | Specifies the type how the given http format is being wrapped (controls, how the httpformat is being rendered in http output) |
|                  |             |                      |                                        |                          |                                                                                                                                                                                                                                                                                                  | 
| --filehandler    | FILE        | ULS_FILE_HANDLER     | 'SIZE','TIME'                          | SIZE                     | Select the handler which decides how the files are rotated if either specific SIZE or TIME has been reached                                                                                                                                                                                      |
| --filename       | FILE        | ULS_FILE_NAME        | '/path/to/file.name'                   | None                     | The PATH + FILENAME where ULS should create the file                                                                                                                                                                                                                                             |
| --filebackupcount | FILE        | ULS_FILE_BACKUPCOUNT | '\<number of files to keep\>'          | 3                        | Select the number of files that should be kept on the file system when rotating the data                                                                                                                                                                                                         |
| --filemaxbytes   | FILE (SIZE) | ULS_FILE_MAXBYTES    | '\<bytes\>'                            | 50 * 1024 * 1024 = 50 MB | Filesize (in bytes) a file can reach before it will be rotated.<br>Only on SIZE - Handler (`--filehandler = size`) !!                                                                                                                                                                            |
| --filetime       | FILE (TIME) | ULS_FILE_TIME        | ['S','M','H','D','W0'-'W6','midnight'] | 'M'                      | Specifies the file rotation trigger unit.<br>S: seconds, M: minutes, H: hours, D: days, 'W0'-'W6' Weekday (W0=Monday), 'midnight': midnight.                                                                                                                                                     |
| --fileinterval   | FILE (TIME) | ULS_FILE_INTERVAL    | '\<interval\>'                         | 30                       | Specifies the file rotation interval based on `--filetime` unit value.<br>Example: 30 and filetime=M would rotate the file every 30 minutes                                                                                                                                                      |
| --fileaction     | FILE        | ULS_FILE_ACTION      | \<file_handler_script.sh '%s'\>        | None                     | Specify a file handler script/binary (e.g. bash) where `'%s'` will be replaced with the absolute filename (.e.g. /path/to/myfile.log). /!\ %s can only be used once! <br>This setting enforces '--filebackupcount' to be set to '1'<br>[Click here for more information](ADDITIONAL_FEATURES.md#) |


## Special Arguments

| Parameter               | Env - Var                  | Options                | Default | Description                                                                                                                                                                                                                               |
|-------------------------|----------------------------|------------------------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| --filter                | ULS_OUTPUT_FILTER          | \<regular expression\> | None    | Filter (regex) to reduce number of OUTPUT log lines<br> Only loglines **matching** the `--filter <expression>` argument will bes sent to the output.<br>[Click here for more information](ADDITIONAL_FEATURES.md#filter---filter-feature) |
| --transformation        | ULS_TRANSFORMATION         | 'MCAS', 'JMESPATH'     | None    | OPTIONAL: Specify an optional transformation to manipulate the output format<br> [Click here for more information](TRANSFORMATIONS.md)                                                                                                    |
| --transformationpattern | ULS_TRANSFORMATION_PATTERN | \<pattern\>            | None    | Specifies the pattern used to transform the log event for the selected transformation. [Click here for more information](TRANSFORMATIONS.md)                                                                                              |


## Autoresume

| Parameter              | Env - Var                 | Options                       | Default | Description                                                                                                   |
|------------------------|---------------------------|-------------------------------|---------|---------------------------------------------------------------------------------------------------------------|
| --autoresume           | ULS_AUTORESUME            | [True, False]                 | False   | Enable automated resume on based on a checkpoint upon api failure or crash (do not use alongside --starttime) |
| --autoresumepath       | ULS_AUTORESUME_PATH       | '/path/to/store/checkpoints/' | var/    | Specify the path where checkpoint files should be written to. (Trailing /)                                    |
| --autoresumewriteafter | ULS_AUTORESUME_WRITEAFTER | <int>                         | 1000    | Specify after how many loglines a checkpoint should be written.                                               |

## Prometheus
| Parameter                             | Env - Var               | Options                   | Default   | Description                                                 |
|---------------------------------------|-------------------------|---------------------------|-----------|-------------------------------------------------------------|
| --prometheus                          | ULS_PROMETHEUS          | [True, False]             | False     | Enable prometheues monitoring support                       |
| --prometheus-port <br> --promport     | ULS_PROMETHEUS_PORT     | <int>                     | 8000      | Prometheues port to listen on                               |
| --prometheus-addr <br> --promaddr     | ULS_PROMETHEUS_ADDR     | xxx.xxx.xxx.xxx           | 127.0.0.1 | Prometheues bind address to listen on                       |
| --prometheus-certfile <br> --promcert | ULS_PROMETHEUS_CERTFILE | '/path/to/store/promcert' | None      | Prometheues certificate file (required alongside a keyfile) |
| --prometheus-keyfile <br>  --promkey  | ULS_PROMETHEUS_KEYFILE  | '/path/to/store/promkey'  | None      | Prometheues key file (required alongside a certfile)        |

## Customizing HTTP & TCPUDP Formatting

Applicable to argument `--tcpudpformat` or environment variable `ULS_TCPUDP_FORMAT`.

By default ULS will write the exact payload received from the API to 
the configured ULS output. Thus, `%s` is the default value.

### Payload decoration (Variable Substition)

If you need to surround the payload with extra information (i.e. metadata for your SIEM), 
you can surround the `%s`. In the example below, didn't surround the `%s` by double-quote
since we want the output to remain a valid JSON:

```json
{"event": %s}
```

### Output Variables

While customizing you might want to use dynamic variables. Substitution happens when ULS
software is starting, if you change your configuration file API hostname, you'll need
to restart ULS so it can take effect.
Besides the below replacements, ULS will also interprete OS (or DOCKER) ENV Vars.


| Variable       | Description                                                  |
|----------------|--------------------------------------------------------------|
| {api_hostname} | This variable will be replaced with the Akamai API Hostname  |
| {uls_input}    | This variable will be replaced with the ULS Input |
| {uls_feed}     | This variable will be replaced with the ULS Feed |


### Example
```bash
# Substitution example
'{"api_host": "{api_hostname}", "input_feed": "{uls_input}-{uls_feed}", "event": %s}'

# OS ENV Var example
export MY_ENV_VAR="THIS IS MY ENV VAR"
'{"api_host": "{api_hostname}", "input_feed": "{uls_input}-{uls_feed}", "additional_env": "$MY_ENV_VAR", "event": %s}'
```