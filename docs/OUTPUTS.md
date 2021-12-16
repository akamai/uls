# ULS Outputs

This document describes the different "OUTPUT" options of ULS.  
All commands referenced in this document are run from the repositories root level.


## Table of contents
- [TCP & UDP](#tcp--udp)  
- [HTTP and HTTPS](#http-and-https)  
- [RAW](#raw)   
- [FILE](#file)  

## TCP & UDP
As UDP and TCP behave very similar on ULS OUTPUT level, they are combined within this section.
UDP and TCP can be used to deliver data streams to any listener on a UDP / TCP socket that awaits a SYSLOG - 'alike' data stream.
Alongside with the output set to either UDP or TCP, ULS requires a HOST and a PORT specification, to deliver the data to.

|OUTPUT|Required Parameters|Optional Parameters|
|---|---|---|
|--output udp|--host \<target name/ip> --port \<target port>| None |
|--output tcp|--host \<target name/ip> --port \<target port>| None |
More information regarding the parameters can be found [here](ARGUMENTS_ENV_VARS.md#output).

**Examples:**
```bash
# Send ETP - PROXY data via TCP to 10.10.100.100 on port 5544
bin/uls.py --input etp --feed proxy --output tcp --host 10.10.100.100 --port 5544

# Sends MFA - AUTH data via UDP to localhost on port 8877
bin/uls.py --input mfa --feed auth --output udp --host localhost --port 8877


```

ULS will resolve domain names using the hosts DNS resolution capabilities.


## HTTP and HTTPS
Several SIEM do provide a way to ingest logs via HTTP(S), so ULS is supporting this feature as well.
Data is sent towards the HTTP listener via a POST request, containing the data in the payload.

|OUTPUT|Required Parameters| Optional Parameters                                                                                |
|---|---|----------------------------------------------------------------------------------------------------|
|--output http|--httpurl \<target url including port and path\>| --httpformat \<output format\><br> --httpauthheader '{"Authorization": "VALUE"}'<br>--httpinsecure |
More information regarding the parameters can be found [here](ARGUMENTS_ENV_VARS.md#output).

**Examples:**
```bash
# Send ETP - Threat data via HTTP to https://splunk.local:9898/services/collector/event and authenticate using Auth header and value (SPLUNK example)
bin/uls.py --input etp --feed threat --output http --httpurl "https://splunk.local:9898/services/collector/event" --httpauthheader '{"Authorization": "1234567890ABCDEFGH"}'

# SEND EAA - ACCESS data via HTTP to https://10.10.9.9:443/ingest without authentication, accept an insecure tls certificate and specify another payload format: data=$logline
bin/uls.py --input eaa --feed access --output http --httpurl "https://10.10.9.9:443/ingest" --httpinsecure --httpformat 'data=%s'
```

## RAW
RAW output has originally been introduced for local debug purposes.
The data will be displayed on stdout.
This enables a quick tests like:
- Data retrieval
- Filter testing
- Transformation testing
- Generic ULS demo/test (without the requirement for a valid endpoint)

|OUTPUT|Required Parameters|Optional Parameters|
|---|---|---|
|--output raw||
More information regarding the parameters can be found [here](ARGUMENTS_ENV_VARS.md#output).

**Examples:**
```bash
# Send EAA - Admin data to the RAW output
bin/uls.py --input eaa --feed admin --output raw
```

## FILE
The file output has been introduced in ULS version 1.2.0 to support logging/archiving operations.
Data is written to an output file and rotated depending on the giben parameters (see examples below).

|OUTPUT| Required Parameters                                                                                                                  | Optional Parameters                                                                                                                              |
|---|--------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
|--output file| --filehandler \<file handler ('SIZE','TIME')\> <br>--filename '/path/to/file.name'<br> --filebackupcount \<number of files to keep\> | --filemaxbytes '\<bytes\>'<br> --filetime ['S','M','H','D','W0'-'W6','midnight']<br> --fileinterval \<interval\><br>--fileaction <action script> |
More information regarding the parameters can be found [here](ARGUMENTS_ENV_VARS.md#output).

**Examples:**
```bash
# Send ETP - AUP data to a file /var/log/akamai/etp_aup/etp_aup.log and rotate it on every 100MB (keep last 10 files)
bin/uls.py --input etp --feed aup --output file --filename /var/log/akamai/etp_aup/etp_aup.log --filehandler size --filemaxbytes 10485760000 --filebackupcount 10

# Send EAA - ACCESS data to a file /var/log/akamai/eaa_access/eaa_access.log and rotate it every 6 hours (keep last 25 files)
bin/uls.py --input etp --feed aup --output file --filename /var/log/akamai/eaa_access/eaa_access.log --filehandler time --filetime h --fileinterval 6 --filebackupcount 25
```
