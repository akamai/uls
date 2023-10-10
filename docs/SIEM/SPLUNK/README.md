# SPLUNK

## Table of contents

- [Introduction](#introduction)
- [Configuration Options](#configuration-options)
- [Additional Splunk Documentation](#additional-splunk-documentation)
- [Key Performance Indicators for EAA](#key-performance-indicators-for-eaa)
  - [[1] No dialout (per connector)](#1-no-dialout-per-connector)
  - [[3] Connector available dialout nearing 0](#3-connector-available-dialout-nearing-0)
  - [[4] High Dialout multiplexing for client-based app](#4-high-dialout-multiplexing-for-client-based-app)
  - [[5] Application HTTP Status code breakdown by Application](#5-application-http-status-code-breakdown-by-application)
    - [For client less app](#for-client-less-app)
    - [For client based app](#for-client-based-app)
  - [[8] Response time percentile](#8-response-time-percentile)
  - [Top tunnel hostnames](#top-tunnel-hostnames)
  - [Top internal app FQDNs](#top-internal-app-fqdns)
  - [Unique users](#unique-users)
- [KNOWN ISSUES](#known-issues)
  - [Line breaking with tcp (streaming) input fails](#line-breaking-with-tcp-streaming-input-fails)

## Introduction

This document describes how to configure [Splunk](https://www.splunk.com/) in order to receive data from ULS.
The recommended way (in order to minimize network/encryption overhead) is the TCP connector.
Nevertheless, ULS has been tested with UDP, TCP & HTTP output module towards Splunk.

It is recommended to use ULS default format **(JSON)** and Splunk Source_type: _json for best user experience.
In search commands it might be neccessary to add the ["SPATH"](https://docs.splunk.com/Documentation/Splunk/8.2.0/SearchReference/Spath) abstraction to search within the json fields:  
```text
index=akamai source=uls_etp_threat | spath | top event.actionName
```

Splunk also works perfectly with the ULS provided [monitoring data](../../MONITORING.md)

## Configuration Options
### HTTP
Splunk ingestion via HTTP towards the SPLUNK HEC can be done via multiple ways:
- LIST of JSON LOG EVENTS
  This method required JSON parsing on the INPUT - minimizing the HTTP payload size. Payload example:
  ```json
  {"event": [{logevent1},{logevent2},{...}]}
  ```
  The required ULS settings look as follows:
  ```bash
  bin/uls.py \
  -i eaa \
  -f access \
  -o http \
  --httpurl https://splunk-URL:8088/services/collector/event \
  --httpauthheader '{"Authorization": "Splunk 123-321-456"}'
  ```
- SINGLE EVENT
  This method allows a raw ingestion of the data, increasing the HTTP payload size. Payload example:
  ```json
  {"event": {logevent1}}{"event": {logevent2}}{"event": {...}}
  ```
  The required ULS settings look as follows:
  ```bash
  bin/uls.py \
  -i eaa \
  -f access \
  -o http \
  --httpurl https://splunk-URL:8088/services/collector/event \
  --httpauthheader '{"Authorization": "Splunk 123-321-456"}' \
  --httpformattype SINGLE-EVENT
  ```

## Additional Splunk Documentation
- [TCP](https://docs.splunk.com/Documentation/SplunkCloud/latest/Data/Monitornetworkports)
- [HTTP](https://docs.splunk.com/Documentation/Splunk/8.2.0/Data/UsetheHTTPEventCollector)
- [UDP](https://docs.splunk.com/Documentation/SplunkCloud/latest/Data/Monitornetworkports)

## Key Performance Indicators for EAA

Splunk search queries provided as examples, feel free to customize them as you see fit. 

If you are willing to share them feel free to update this document and open a [pull request](../../../README.md#development).

### [1] No dialout (per connector)

```
index="uls_eaa" source="uls_eaa-conhealth" | spath
| search reachable = 1 status = 1 dialout_total = 0
 ```

### [3] Connector available dialout nearing 0

Each EAA application consume dialout connection on the EAA connector attached it.
Floor, ceiling and step can be configure to make your environment, 99% of the time the default value should be fine. It is good to keep an eye on the idle dailout, if they are close to zero, the application may not be able to respond.

```spl
index="uls_eaa" source="uls_eaa-conhealth"
| eval dialout_free_ratio=dialout_idle/dialout_total
| search dialout_free_ratio<=0.10
```

Action: Increase the dialout ceiling in the Advanced Settings tab of the application configuration.

### [4] High Dialout multiplexing for client-based app

When Active / (Total - Idle) gets greater than 1 we use multiplexing (feature introduce with dialout v2)

```spl
index="uls_eaa" source="uls_eaa-conhealth" | spath
| eval dividend=( if(isnull(dialout_total), 0, dialout_active) - if(isnull(dialout_idle), 0, dialout_idle))
| eval highdo_ratio=if(dividend>0, -1, if(isnull(dialout_active), 0, dialout_active) / dividend)
| search highdo_ratio > 1
| table _time, name, dialout_active, dialout_total, dialout_idle, highdo_ratio
```

### [5] Application HTTP Status code breakdown by Application

#### For client less app

```spl
index="uls_eaa" source="uls_eaa-access" | spath
| search internal_host="-"
| eval status=case(like(status_code,"1%"),"1xx",like(status_code,"2%"),"2xx",like(status_code,"3%"),"3xx",like(status_code,"4%"),"4xx",like(status_code,"5%"),"5xx")
| stats count by apphost, status
```

#### For client based app

```spl
index="uls_eaa" source="uls_eaa-access" | spath
| search NOT internal_host="-"
| eval status=case(like(status_code,"1%"),"1xx",like(status_code,"2%"),"2xx",like(status_code,"3%"),"3xx",like(status_code,"4%"),"4xx",like(status_code,"5%"),"5xx")
| stats count by apphost, status
```

### [8] Response time percentile

The performance may need to be filtered by application type (clientless vs. cliented), and also by application.

```spl
index="uls_eaa" source="uls_eaa-access" | spath
| search NOT internal_host="-"
| bin _time span=30m
| stats perc50(total_resp_time) perc75(total_resp_time) perc95(total_resp_time) perc99(total_resp_time) by _time
```

### Top tunnel hostnames

```spl
index="uls_eaa" source="uls_eaa-access" | spath
| search NOT internal_host="-"
| stats count as access_count by apphost
```

### Top internal app FQDNs

```spl
index="uls_eaa" source="uls_eaa-access" | spath
| search NOT internal_host="-"
| stats count as access_count by internal_host
```

<!--
### Client: EAA Client version distribution
Will require Device Posture feed

### Client: OS distribution
Will require Device Posture feed
-->

### Unique users

```spl
index="uls_eaa" source="uls-eaa-access" | spath
| search NOT username IN ("-", "anon-user")
| stats dc(username)
```

## KNOWN ISSUES

### Line breaking with tcp (streaming) input fails
Depending on your configured settings, SPLUNK could fail determining the line breaks correctly.  
Many messages might appear as "one" event within splunk.
To fix this, please follow the instructions below:  

Add the following to the file `$SPLUNK_HOME/etc/system/local/props.conf`:
Example source name = uls_eaa-access
```text
[source::uls_eaa-access]
SHOULD_LINEMERGE = false
```

But you can also use a wildcard for all source types
```text
[source::uls_*]
SHOULD_LINEMERGE = false
```

The default linebreaker `LINE_BREAKER = ([\r\n]+)` configuration should perfectly match.  
More information on props can be found [here](https://docs.splunk.com/Documentation/Splunk/Latest/Admin/Propsconf)

