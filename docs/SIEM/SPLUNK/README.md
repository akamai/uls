# SPLUNK
This document describes how to configure [Splunk](https://www.splunk.com/) in order to receive data from ULS.
The recommended way (in order to minimize network/encryption overhead) is the TCP connector.
Nevertheless, ULS has been tested with UDP, TCP & HTTP output module towards splunk.

It is recommended to use ULS default format **(JSON)** and Splunk Source_type: _json for best user experience.
In search commands it might be neccessary to add the ["SPATH"](https://docs.splunk.com/Documentation/Splunk/8.2.0/SearchReference/Spath) abstraction to search within the json fields:  
```text
index=akamai source=uls_etp_threat | spath | top event.actionName
```

Splunk also works perfectly with the ULS provided [monitoring data](../../MONITORING.md)
## Additional Documentation
- [TCP](https://docs.splunk.com/Documentation/SplunkCloud/latest/Data/Monitornetworkports)
- [HTTP](https://docs.splunk.com/Documentation/Splunk/8.2.0/Data/UsetheHTTPEventCollector)
- [UDP](https://docs.splunk.com/Documentation/SplunkCloud/latest/Data/Monitornetworkports)


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

