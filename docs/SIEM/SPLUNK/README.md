# SPLUNK
This document describes how to configure [Splunk](https://www.splunk.com/) in order to receive data from ULS.
The recommended way (in order to minimize network/encryption overhead) is the TCP connector.
Nevertheless, ULS has been tested with TCP & HTTP output module towards splunk.

## INPUTS
### TCP INPUT
Please follow the [SPLUNK DOCUMENTATION](https://docs.splunk.com/Documentation/SplunkCloud/latest/Data/Monitornetworkports).

### HTTP EVENT COLLECTOR
Please follow the [SPLUNK DOCUMENTATION](https://docs.splunk.com/Documentation/Splunk/8.2.0/Data/UsetheHTTPEventCollector).


## KNOWN ISSUES
### Line breaking with tcp (streaming) input fails
Depending on your configured settings, SPLUNK could fail determining the line breaks correctly.  
Many messages might appear as "one" event within splunk.
To fix this, please follow the instructions below:  

Add the following to the file `$SPLUNK_HOME/etc/system/local/props.conf`:
```text
[akamai_etp]
SHOULD_LINEMERGE = false
```
The default linebreaker `LINE_BREAKER = ([\r\n]+)` configuration should perfectly match.  
More information on props can be found [here](https://docs.splunk.com/Documentation/Splunk/Latest/Admin/Propsconf)