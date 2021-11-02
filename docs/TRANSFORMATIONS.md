# ULS TRANSFORMATIONS
Transformations have been introduced to ULS in version `1.2.0` to support additional 3rd party integrations and custom log formats.

## Table of contents
- [Microsoft Cloud Application Security (MCAS)](#microsoft-cloud-application-security-mcas)
- [JMESPATH](#jmespath)

## Microsoft Cloud Application Security (MCAS)
MCAS Transformation only supports the following products (inputs) and feeds

|Input|Feed|Output
|---|---|---|
|ETP|PROXY|"detection_time={0} client_ip={1} destination_ip={2} domain={3} user_name={4} bytes_uploaded={5} bytes_downloaded={6} bytes_total={7} action={8}"|
|ETP|DNS|"detection_time={0} client_ip={1} destination_ip={2} domain={3} user_name={4} bytes_uploaded={5} bytes_downloaded={6} bytes_total={7} action={8}"|

The transformation options can be configured in the file `config/transformation_config.py`

### MCAS Examples
```bash
# ETP - DNS (RAW)
bin/uls.py --section akamaidemo --input etp --feed dns --output raw --transformation mcas

# ETP Proxy (RAW)
bin/uls.py --section akamaidemo --input etp --feed proxy --output raw --transformation mcas
```


## JMESPATH
ULS supports JMESPATH (JSON query language) to reduce the size of a message or specify the JSON fields sent into the SIEM (i.e. for security reasons).
JMESPATH supports all available products (inputs) and feeds.

Before using JMESPATH, JMESPATH needs to be installed on the system (ULS docker automatically ships with JMESPATH installed).
```bash
pip3 install -r bin/requirements.txt
```

The `JMESPATH` transformation requieres an additional argument to specify the search pattern `--transformationpattern`

A really good JMESPATH tutorial can be found [here](https://jmespath.org/tutorial.html).
Additional documentation can be found [here](https://jmespath.org).

### JMESPATH Examples
```bash
# ETP DNS logs - transformed to show only time, cientip, domain and action in JSON fortmat (sent to RAW output)
 bin/uls.py --input etp --feed dns --output raw  --transformation jmespath --transformationpattern '{time: query.time, client: query.clientIp, domain: query.domain, action: event.actionName}'
  
# EAA ACCESSS logs transformed to output only username, apphost, status and clientip in JSON format (sent to RAW output) 
bin/uls.py --input eaa --feed access --section akamaidemo --output raw --transformation jmespath --transformationpattern '{username: username, apphost: apphost, status: status_code, clientip: clientip}'

# EAA ACCESSS logs transformed to output only country, state and city in LIST format (sent to RAW output)
bin/uls.py --input eaa --feed access --section akamaidemo --output raw --transformation jmespath --transformationpattern '[geo_country, geo_state, geo_city]'
```
