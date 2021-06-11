# ULS Monitoring
This document describes the ULS monitoring output (STDOUT).
The output will be sent every 5 minutes to stdout by default.

## Field description
| Field| Example | Description |
|---|---|---|
|dt | "2021-06-09T08:15:35.092889" | Date & Time (OS Timezone)|
|uls_product| "ETP" | Selected ULS product |
|uls_feed| "THREAT" | Selected ULS feed |
|uls_output| "HTTP" | Selected ULS output |
|uls_runtime| "3000" | Time in seconds ULS is already running |
|event_count| "625014" | Number of events handled by ULS (overall) |
|event_rate| "10.97" | Average events per second. Average based on the monitoring interval. (Default 5 minutes)|
|mon_interval| "300" | Monitoring interval in seconds|


## Example Output
The output is delivered in JSON format
```json
{"dt": "2021-06-09T08:15:35.092889", "uls_product": "ETP", "uls_feed": "THREAT", "uls_outpout": "HTTP", "uls_runtime": 300, "event_count": 504, "event_rate": 1.68, "mon_interval": 300}
```

## Send docker logs to splunk
For this we're using the embedded docker - splunk logging module.

### Docker-compose
Example (add to every service in your docker-compose.yml)
```yaml
version: "3.0"
...
services:
  uls-tool:
    logging:
        driver: splunk
        options:
          splunk-url: 'https://your.splunk.host:8088'
          splunk-token: 'xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxx'
          splunk-insecureskipverify: 'true'
          splunk-format: 'json'
  ...
```

### Docker.compose template
https://github.com/compose-spec/compose-spec/blob/master/spec.md#using-extensions-as-fragments
```yaml
version: "3.0"
x-logging: &default-logging
  driver: splunk
  options:
    splunk-url: 'https://your.splunk.host:8088'
    splunk-token: 'xxxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxxx'
    splunk-insecureskipverify: 'true'
    splunk-format: 'json'
...
services:
  uls-tool1:
    ...
    logging: *default-logging
    ...
  uls-tool2:
    ...
    logging: *default-logging
    ...
  ...
```

More splunk - options for docker can be found [here](https://docs.docker.com/config/containers/logging/splunk/)
Sidenote: you will still receive logs on the cli running `docker-compose logs -f uls-tool`

![Docker logs in splunk](images/uls_docker_logs_to_splunk.png)

## Docker logs to other SIEMs
If you have other siem, please see dockers logging capabilities [here](https://docs.docker.com/config/containers/logging/configure/).