# IBM QRadar<!-- omit in toc -->

## Table of contents<!-- omit in toc -->

- [Inputs](#inputs)
  - [EAA Access Log Source Type definition (ACCESS)](#eaa-access-log-source-type-definition-access)
  - [EAA Audit logs (ADMIN)](#eaa-audit-logs-admin)
  - [EAA Connector Health (CONHEALTH)](#eaa-connector-health-conhealth)
- [ULS output configuration](#uls-output-configuration)

This document describes how to configure [IBM QRadar](https://www.ibm.com/security/security-intelligence/qradar) in order to receive data from ULS.

The recommended way (in order to minimize network/encryption overhead) is the TCP (Syslog) connector.

Each feed has a corresponding definition file (zip). Use QRadar Extension Management to import it into your QRadar environment.

## Inputs

### EAA Access Log Source Type definition (ACCESS)

Download the latest QRadar definition for ACCESS feed: [qradar-eaa-access-definition.zip](qradar-eaa-access-definition.zip)

Access fields are mapped as follow:

| EAA field | QRadar property | QRadar expression |
| --------- | ----------- | ----------- |
| username | Username | JSON `/"username"` |
| apphost | Application name | JSON `/"apphost"` |
| http_method | - | - |
| url_path | URL | JSON `/"url_path"` |
| http_ver | - | - |
| referer | - | - |
| status_code | Completion code | JSON `/"status_code"` |
| idpinfo | Identity Extended Field | JSON `/"idpinfo"` |
| clientip | Source IP | JSON `/"clientip"` |
| http_verb2 | - | - |
| total_resp_time | - | - |
| connector_resp_time | - | - |
| datetime | Date Time | JSON `/"datetime"` |
| origin_resp_time | - | - |
| origin_host | - | - |
| req_size | - | - |
| content_type | - | - |
| user_agent | - | - |
| device_os | - | - |
| device_type | - | - |
| geo_city | - | - |
| geo_state | - | - |
| geo_statecode | - | - |
| geo_countrycode | - | - |
| geo_country | - | - |
| internal_host | Destination Host Name | Regex `internal_host": "(.*?):(.*?)"` group 1 |
| internal_host | Destination Port | Regex `internal_host": "(.*?):(.*?)"` group 2|
| session_info | - | - |
| groups | Identity Group Name | JSON `/"groups"` |
| session_id | - | - |
| client_id | - | - |
| deny_reason | - | - |
| bytes_out | BytesSent | JSON `/"bytes_out"` |
| bytes_in | BytesReceived | JSON `/"bytes_in"` |
| con_ip | Post NAT Source IP | JSON `/"con_ip"` |
| con_srcport | Post NAT Source Port | JSON `/"con_srcport"` |

See also [EAA access log definition](https://techdocs.akamai.com/eaa/docs/data-feed-siem#access-logs) for a full definition.

### EAA Audit logs (ADMIN)

Download the latest QRadar definition for ADMIN feed: [qradar-eaa-admin-definition.zip](qradar-eaa-admin-definition.zip)

Admin audit fields are mapped as follow:

| EAA field | QRadar property | QRadar expression |
| --------- | ----------- | ----------- |
| datetime | Log Source Time | JSON `/"datetime"` |
| username | Username | JSON `/"username"` |
| resource_type | ObjectType | JSON `/"resource_type"` |
| resource | ObjectName | JSON `/"resource"` | 
| event | Event ID | JSON `/"event"` |
| event_type | Event Category | JSON `/"event_type"` |

See also [EAA admin log definition](https://techdocs.akamai.com/eaa/docs/data-feed-siem#admin-logs) for a full definition.

### EAA Connector Health (CONHEALTH)

Download the latest QRadar definition for ADMIN feed: [qradar-eaa-conhealth-definition.zip](qradar-eaa-conhealth-definition.zip)

Connector health fields are mapped as follow:

| EAA field | QRadar property | QRadar expression |
| --------- | ----------- | ----------- |
| connector_uuid | Resource | JSON `/"connector_uuid"` |
| name | ObjectName | JSON `/"name"` |
| reachable | - | JSON `/"reachable"` |
| status | Completion status | JSON `/"status"` | 
| version | Subsystem name | JSON `/"version"` |
| privateip | Source IP | JSON `/"privateip"` |
| publicip | Pre NAT Source IP | JSON `/"publicip"` |
| debugchan | debugchan | JSON `/"debugchan"` |
| ts | - | JSON `/"ts"` with Date format `YYYY-MM-DD"T"HH:mm:ss.sss"Z"` |
| cpu | - | JSON `/"cpu"` |
| disk | - | JSON `/"disk"` |
| mem | - | JSON `/"mem"` |
| network | - | JSON `/"network"` |
| dialout_total | - | JSON `/"dialout_total"` |
| dialout_idle | - | JSON `/"dialout_idle"` |
| dialout_active | - | JSON `/"dialout_active"` |

See also [EAA connector health feed definition](https://techdocs.akamai.com/eaa/docs/data-feed-siem#connector-health) for a full definition.

## ULS output configuration

Please follow the [QRADAR documentation](https://www.ibm.com/docs/en/dsm?topic=options-http-receiver-protocol-configuration).
