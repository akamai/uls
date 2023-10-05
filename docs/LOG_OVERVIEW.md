# Log Overview
ULS supports ingestion of different log streams into SIEM. 

To get the highest value out of the ingested data, it is crucial to understand the delivered data.  

Here are some examples (per product) and links to additional information.

## Table of contents

- [Log Overview](#log-overview)
  - [Table of contents](#table-of-contents)
  - [Enterprise Application Access (EAA)](#enterprise-application-access-eaa)
    - [Access Logs (ACCESS)](#access-logs-access)
    - [Admin Logs (ADMIN)](#admin-logs-admin)
    - [Connector Health (CONHEALTH)](#connector-health-conhealth)
    - [Device Posture Inventory (DEVINV)](#device-posture-inventory-devinv)
  - [Secure Internet Access Enterprise (SIA-E)](#secure-internet-access-enterprise-sia-e)
    - [Threat Log (THREAT)](#threat-log-threat)
    - [Accceptable Use Policy Logs (AUP)](#accceptable-use-policy-logs-aup)
    - [DNS Activity](#dns-activity)
    - [PROXY](#proxy)
    - [NETCON](#netcon)
  - [Akamai MFA (MFA)](#akamai-mfa-mfa)
    - [Authentication Logs (AUTH)](#authentication-logs-auth)
  - [Guardicore](#guardicore)
    - [NETLOG](#netlog)
    - [INCIDENT](#incident)
  - [Linode](#linode)
    - [AUDIT Logs](#audit-logs)

## Enterprise Application Access (EAA)

When configuring ULS to access EAA these feed, set `input` argument/variable to `EAA` and `feed` as indicated below in parathesis.
 
### Access Logs (ACCESS)

Additional information regarding the log fields can be found on [here](https://techdocs.akamai.com/eaa/docs/data-feed-siem#access-logs)

```json
{
    "username": "user1",
    "apphost": "vault.akamaidemo.net",
    "http_method": "GET",
    "url_path": "/v1/sys/health?standbycode=200&sealedcode=200&uninitcode=200&drsecondarycode=200&performancestandbycode=200",
    "http_ver": "HTTP/1.1",
    "referer": "https://vault.akamaidemo.net/ui/vault/secrets",
    "status_code": 200,
    "idpinfo": "SENTRY|V",
    "clientip": "84.189.50.66",
    "http_verb2": "GET",
    "total_resp_time": 0.011,
    "connector_resp_time": 0.011,
    "datetime": "2021-07-27T18:20:14+00:00",
    "origin_resp_time": 0.005,
    "origin_host": "10.11.52.131:8200",
    "req_size": 515,
    "content_type": "application/json",
    "user_agent": "Chrome-91-0",
    "device_os": "Mac-OS-X-10-15",
    "device_type": "Other",
    "geo_city": "Kummersbruck",
    "geo_state": "Bavaria",
    "geo_statecode": "BY",
    "geo_countrycode": "DE",
    "geo_country": "Germany",
    "internal_host": "-",
    "session_info": "cookie-valid",
    "groups": "-",
    "session_id": "1b1c728b-298e-4ebd-ce7c-0c1f99ad943f"
}
```

### Admin Logs (ADMIN)

Additional information regarding the log fields can be found on [here](https://techdocs.akamai.com/eaa/docs/data-feed-siem#admin-logs).
```json
{
    "datetime": "2021-07-23T05:54:40",
    "username": "system",
    "resource_type": "connectors",
    "resource": "tmelab-bos",
    "event": "unreachable",
    "event_type": "system"
}
```

### Connector Health (CONHEALTH)

Additional information regarding the log fields can be found on [here](https://techdocs.akamai.com/eaa/docs/data-feed-siem#connector-health)
```json
{
    "connector_uuid": "cht3_GEjQWyMW9LEk7KQfg",
    "name": "demo-v2-con-1-amer",
    "reachable": 1,
    "status": 1,
    "version": "21.01.0-152",
    "privateip": "10.1.4.206",
    "publicip": "123.123.123.123",
    "debugchan": "Y",
    "datetime": "2021-07-23T18:06:35.676Z",
    "ts": "2021-07-23T18:06:35.676Z",
    "cpu": 1.3,
    "disk": 34.4,
    "mem": 32.4,
    "network": 0.06,
    "dialout_total": 1304,
    "dialout_idle": 1302,
    "dialout_active": 1
}
```

### Device Posture Inventory (DEVINV)

When enabled, EAA can provide a full view on the device running EAA Client.
A report is available in Akamai Control Center and can also be extracted using API.
This feed uses the [Device Posture Inventory](https://techdocs.akamai.com/eaa-api/reference/get-device-posture-inventory) in EAA API.

Each event will be one device as a JSON document, example provided with the cli-eaa command `akamai eaa dp inventory|head -n1|jq .`

<details>
    <summary>View device inventory event example (JSON)</summary>

```json
{
    "device_id": "5c98021e78e9c393b07145e388c20ace7733ca88ed63ba0790c09e7ed5c58cf7",
    "device_name": "sfo-mpw9c",
    "risk_posture_tiers": [
        {
        "passed": true,
        "name": "Low",
        "id": 13,
        "tier": true
        }
    ],
    "risk_posture_tags": [
        {
        "passed": true,
        "name": "Healthy iOS",
        "id": 597,
        "tier": false
        },
        {
        "passed": true,
        "name": "latest-of-latest",
        "id": 949,
        "tier": false
        },
        {
        "passed": true,
        "name": "ETP-Healthy-NotCompromised",
        "id": 1831,
        "tier": false
        },
        {
        "passed": false,
        "remediations": [
            "Unsupported operating system."
        ],
        "name": "Demo Tag - CB",
        "id": 2380,
        "tier": false
        },
        {
        "passed": false,
        "remediations": [
            "Unsupported operating system."
        ],
        "name": "Demo - Tag - Anti malware",
        "id": 2381,
        "tier": false
        },
        {
        "passed": true,
        "name": "Device - Not Compromised",
        "id": 2392,
        "tier": false
        },
        {
        "passed": true,
        "name": "Forrester Demo -",
        "id": 2402,
        "tier": false
        },
        {
        "passed": true,
        "name": "Demo - Anti Malware",
        "id": 2407,
        "tier": false
        },
        {
        "passed": true,
        "name": "Demo Tag",
        "id": 2408,
        "tier": false
        }
    ],
    "client_version": "2.7.1",
    "idp_username": "N/A",
    "user_id": "androcho",
    "browsers": [
        {
        "name": "Edge",
        "version": "101.0.1210.47"
        },
        {
        "name": "Chrome",
        "version": "101.0.4951.64"
        },
        {
        "name": "Safari",
        "version": "15.4"
        },
        {
        "name": "Firefox",
        "version": "100.0"
        }
],
"os_name": "macOS",
"os_version": "Monterey 12.3.1 (21E258)",
"signal_timestamp": "2022-05-16T20:21:33.321539+00:00",
"os_update_timestamp": "2022-04-15T20:18:43Z",
"os_auto_update": true,
"anti_malware_running": [
    "Sentinel Agent"
],
"anti_malware_status": [
    {
    "name": "Any Vendor",
    "passed": true
    }
],
"anti_malware_info": [
    {
    "name": "Sentinel Agent",
    "passed": true
    }
],
"firewall_status": "good",
"system_disk_encryption": true,
"etp_client_status": "installed",
"mobile_device": false,
"certificate_profile": [
    {
    "name": "cert",
    "passed": false
    }
],
"etp_signals": {
    "threat_detected": false
}
}
```
</details>

## Secure Internet Access Enterprise (SIA-E)

Formerly known as Enterprise Threat Protector (ETP).  

For large volume of security events (multiple 100K per hour), configure the underlying 
`cli-etp` to issue concurrent API requests.

Depending on your ULS setup you need to pass the `CLIETP_FETCH_CONCURRENT` environment variable.
We recommend to start with the value `2`, observe, and increase up to `8` if you observe backlog.

This will have a small impact on CPU usage, while increasing the number of events.

### Threat Log (THREAT)
Additional information regarding the log fields can be found [here](https://techdocs.akamai.com/etp-reporting/reference/post-threat-event-details)

<details>
    <summary>Security Threat Event example (JSON)</summary>

```json
{
    "pageInfo": {
        "totalRecords": 97913,
        "pageNumber": 1,
        "pageSize": 5
    },
    "dataRows": [
        {
            "id": "0",
            "configId": "1041",
            "l7Protocol": "DNS",
            "query": {
                "time": "2020-05-26T06:34:53Z",
                "clientIp": "172.25.174.232",
                "dnsIp": "198.18.193.241",
                "domain": "d.la1-c2-ia4.salesforceliveagent.com.",
                "uuid": "198.18.193.241-198.18.193.228-1590474893-46281-35384",
                "queryType": "A",
                "deviceId": "c37a4c4e-a7cd-400f-820d-b82762c52975",
                "deviceName": "BOS-WPX5E",
                "resolved": [
                    {
                        "type": "A",
                        "response": "13.110.63.55",
                        "asn": "14340",
                        "asname": "N/A"
                    },
                    {
                        "type": "A",
                        "response": "13.110.61.55",
                        "asn": "14340",
                        "asname": "N/A"
                    },
                    {
                        "type": "A",
                        "response": "13.110.62.55",
                        "asn": "14340",
                        "asname": "N/A"
                    }
                ]
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "domain",
                "detectionTime": "2020-05-26T06:34:53Z",
                "detectionType": "inline",
                "siteId": "51284",
                "siteName": "E2E WIN 174.232 site",
                "policyId": "38307",
                "policyName": "E2E-CML-test",
                "listId": "24",
                "listName": "24",
                "categoryId": "24",
                "categoryName": "24",
                "confidenceId": "-1",
                "confidenceName": "Unknown",
                "actionId": "6",
                "actionName": "Classify",
                "description": "None",
                "reason": "Akamai Intelligence (DNS)",
                "onRamp": "Yes",
                "threatId": 2000,
                "severityId": 0,
                "threatName": "AUP",
                "severityLevel": "Unclassified",
                "onrampType": "etp-client",
                "internalClientIP": "N/A",
                "clientRequestId": "00019749",
                "policyEvaluationSource": "dns"
            }
        },
        {
            "id": "1",
            "configId": "1041",
            "l7Protocol": "DNS",
            "query": {
                "time": "2020-05-26T06:34:52Z",
                "clientIp": "172.25.174.232",
                "dnsIp": "198.18.193.241",
                "domain": "teams.microsoft.com.",
                "uuid": "198.18.193.241-198.18.193.228-1590474892-14345-62675",
                "queryType": "A",
                "deviceId": "c37a4c4e-a7cd-400f-820d-b82762c52975",
                "deviceName": "BOS-WPX5E",
                "resolved": [
                    {
                        "type": "A",
                        "response": "52.113.194.132",
                        "asn": "8068",
                        "asname": "N/A"
                    }
                ]
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "domain",
                "detectionTime": "2020-05-26T06:34:52Z",
                "detectionType": "inline",
                "siteId": "51284",
                "siteName": "E2E WIN 174.232 site",
                "policyId": "38307",
                "policyName": "E2E-CML-test",
                "listId": "24",
                "listName": "24",
                "categoryId": "24",
                "categoryName": "24",
                "confidenceId": "-1",
                "confidenceName": "Unknown",
                "actionId": "6",
                "actionName": "Classify",
                "description": "None",
                "reason": "Akamai Intelligence (DNS)",
                "onRamp": "Yes",
                "threatId": 2000,
                "severityId": 0,
                "threatName": "AUP",
                "severityLevel": "Unclassified",
                "onrampType": "etp-client",
                "internalClientIP": "N/A",
                "clientRequestId": "00019748",
                "policyEvaluationSource": "dns"
            }
        },
        {
            "id": "2",
            "configId": "1041",
            "l7Protocol": "DNS",
            "query": {
                "time": "2020-05-26T06:34:51Z",
                "clientIp": "198.18.179.121",
                "dnsIp": "198.18.193.241",
                "domain": "1590449691.akamaietpmalwaretest.com.",
                "uuid": "198.18.193.241-198.18.179.134-1590474891-6340-2976",
                "queryType": "AAAA",
                "deviceId": "N/A",
                "deviceName": "Not Available",
                "resolved": [
                    {
                        "type": "N/A",
                        "response": "N/A",
                        "asn": "N/A",
                        "asname": "N/A"
                    }
                ]
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "domain",
                "detectionTime": "2020-05-26T06:34:51Z",
                "detectionType": "inline",
                "siteId": "-1",
                "siteName": "Unidentified IPs",
                "policyId": "2240",
                "policyName": "Default",
                "listId": "1",
                "listName": "Malware",
                "categoryId": "1",
                "categoryName": "Malware",
                "confidenceId": "2",
                "confidenceName": "Known",
                "actionId": "1",
                "actionName": "Monitor",
                "description": "None",
                "reason": "Akamai Intelligence (DNS)",
                "onRamp": "No",
                "threatId": 5070,
                "severityId": 2,
                "threatName": "Known Malware",
                "severityLevel": "High",
                "onrampType": "",
                "internalClientIP": "N/A",
                "clientRequestId": "",
                "policyEvaluationSource": "dns"
            }
        },
        {
            "id": "3",
            "configId": "1041",
            "l7Protocol": "DNS",
            "query": {
                "time": "2020-05-26T06:34:51Z",
                "clientIp": "198.18.179.121",
                "dnsIp": "198.18.193.241",
                "domain": "1590449691.akamaietpmalwaretest.com.",
                "uuid": "198.18.193.241-198.18.179.134-1590474891-42367-7406",
                "queryType": "A",
                "deviceId": "N/A",
                "deviceName": "Not Available",
                "resolved": [
                    {
                        "type": "A",
                        "response": "34.193.182.244",
                        "asn": "14618",
                        "asname": "aws"
                    }
                ]
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "domain",
                "detectionTime": "2020-05-26T06:34:51Z",
                "detectionType": "inline",
                "siteId": "-1",
                "siteName": "Unidentified IPs",
                "policyId": "2240",
                "policyName": "Default",
                "listId": "1",
                "listName": "Malware",
                "categoryId": "1",
                "categoryName": "Malware",
                "confidenceId": "2",
                "confidenceName": "Known",
                "actionId": "1",
                "actionName": "Monitor",
                "description": "None",
                "reason": "Akamai Intelligence (DNS)",
                "onRamp": "No",
                "threatId": 5070,
                "severityId": 2,
                "threatName": "Known Malware",
                "severityLevel": "High",
                "onrampType": "",
                "internalClientIP": "N/A",
                "clientRequestId": "",
                "policyEvaluationSource": "dns"
            }
        },
        {
            "id": "4",
            "configId": "1041",
            "l7Protocol": "DNS",
            "query": {
                "time": "2020-05-26T06:34:51Z",
                "clientIp": "198.18.179.121",
                "dnsIp": "198.18.193.241",
                "domain": "1590449691.akamaietpmalwaretest.com.e2e-etp.org.",
                "uuid": "198.18.193.241-198.18.179.134-1590474891-5081-49572",
                "queryType": "AAAA",
                "deviceId": "N/A",
                "deviceName": "Not Available",
                "resolved": [
                    {
                        "type": "N/A",
                        "response": "N/A",
                        "asn": "N/A",
                        "asname": "N/A"
                    }
                ]
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "domain",
                "detectionTime": "2020-05-26T06:34:51Z",
                "detectionType": "inline",
                "siteId": "-1",
                "siteName": "Unidentified IPs",
                "policyId": "2240",
                "policyName": "Default",
                "listId": "4",
                "listName": "DNS Exfiltration",
                "categoryId": "5",
                "categoryName": "DNS Exfiltration",
                "confidenceId": "1",
                "confidenceName": "Suspected",
                "actionId": "1",
                "actionName": "Monitor",
                "description": "None",
                "reason": "Akamai Intelligence (DNS)",
                "onRamp": "No",
                "threatId": 5135,
                "severityId": 4,
                "threatName": "Suspected DNS tunneling",
                "severityLevel": "Low",
                "onrampType": "",
                "internalClientIP": "N/A",
                "clientRequestId": "",
                "policyEvaluationSource": "dns"
            }
        }
    ]
}
```
</details>

### Accceptable Use Policy Logs (AUP)
Additional information regarding the log fields can be found [here](https://techdocs.akamai.com/etp-reporting/reference/get-events-details)

<details>
    <summary>Acceptable Use Policy Event example (JSON)</summary>
```json
{
    "pageInfo": {
        "totalRecords": 97913,
        "pageNumber": 1,
        "pageSize": 5
    },
    "dataRows": [
        {
            "id": "0",
            "configId": "1041",
            "l7Protocol": "DNS",
            "query": {
                "time": "2020-05-26T06:34:53Z",
                "clientIp": "172.25.174.232",
                "dnsIp": "198.18.193.241",
                "domain": "d.la1-c2-ia4.salesforceliveagent.com.",
                "uuid": "198.18.193.241-198.18.193.228-1590474893-46281-35384",
                "queryType": "A",
                "deviceId": "c37a4c4e-a7cd-400f-820d-b82762c52975",
                "deviceName": "BOS-WPX5E",
                "resolved": [
                    {
                        "type": "A",
                        "response": "13.110.63.55",
                        "asn": "14340",
                        "asname": "N/A"
                    },
                    {
                        "type": "A",
                        "response": "13.110.61.55",
                        "asn": "14340",
                        "asname": "N/A"
                    },
                    {
                        "type": "A",
                        "response": "13.110.62.55",
                        "asn": "14340",
                        "asname": "N/A"
                    }
                ]
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "domain",
                "detectionTime": "2020-05-26T06:34:53Z",
                "detectionType": "inline",
                "siteId": "51284",
                "siteName": "E2E WIN 174.232 site",
                "policyId": "38307",
                "policyName": "E2E-CML-test",
                "listId": "24",
                "listName": "24",
                "categoryId": "24",
                "categoryName": "24",
                "confidenceId": "-1",
                "confidenceName": "Unknown",
                "actionId": "6",
                "actionName": "Classify",
                "description": "None",
                "reason": "Akamai Intelligence (DNS)",
                "onRamp": "Yes",
                "threatId": 2000,
                "severityId": 0,
                "threatName": "AUP",
                "severityLevel": "Unclassified",
                "onrampType": "etp-client",
                "internalClientIP": "N/A",
                "clientRequestId": "00019749",
                "policyEvaluationSource": "dns"
            }
        },
        {
            "id": "1",
            "configId": "1041",
            "l7Protocol": "DNS",
            "query": {
                "time": "2020-05-26T06:34:52Z",
                "clientIp": "172.25.174.232",
                "dnsIp": "198.18.193.241",
                "domain": "teams.microsoft.com.",
                "uuid": "198.18.193.241-198.18.193.228-1590474892-14345-62675",
                "queryType": "A",
                "deviceId": "c37a4c4e-a7cd-400f-820d-b82762c52975",
                "deviceName": "BOS-WPX5E",
                "resolved": [
                    {
                        "type": "A",
                        "response": "52.113.194.132",
                        "asn": "8068",
                        "asname": "N/A"
                    }
                ]
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "domain",
                "detectionTime": "2020-05-26T06:34:52Z",
                "detectionType": "inline",
                "siteId": "51284",
                "siteName": "E2E WIN 174.232 site",
                "policyId": "38307",
                "policyName": "E2E-CML-test",
                "listId": "24",
                "listName": "24",
                "categoryId": "24",
                "categoryName": "24",
                "confidenceId": "-1",
                "confidenceName": "Unknown",
                "actionId": "6",
                "actionName": "Classify",
                "description": "None",
                "reason": "Akamai Intelligence (DNS)",
                "onRamp": "Yes",
                "threatId": 2000,
                "severityId": 0,
                "threatName": "AUP",
                "severityLevel": "Unclassified",
                "onrampType": "etp-client",
                "internalClientIP": "N/A",
                "clientRequestId": "00019748",
                "policyEvaluationSource": "dns"
            }
        },
        {
            "id": "2",
            "configId": "1041",
            "l7Protocol": "DNS",
            "query": {
                "time": "2020-05-26T06:34:51Z",
                "clientIp": "198.18.179.121",
                "dnsIp": "198.18.193.241",
                "domain": "1590449691.akamaietpmalwaretest.com.",
                "uuid": "198.18.193.241-198.18.179.134-1590474891-6340-2976",
                "queryType": "AAAA",
                "deviceId": "N/A",
                "deviceName": "Not Available",
                "resolved": [
                    {
                        "type": "N/A",
                        "response": "N/A",
                        "asn": "N/A",
                        "asname": "N/A"
                    }
                ]
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "domain",
                "detectionTime": "2020-05-26T06:34:51Z",
                "detectionType": "inline",
                "siteId": "-1",
                "siteName": "Unidentified IPs",
                "policyId": "2240",
                "policyName": "Default",
                "listId": "1",
                "listName": "Malware",
                "categoryId": "1",
                "categoryName": "Malware",
                "confidenceId": "2",
                "confidenceName": "Known",
                "actionId": "1",
                "actionName": "Monitor",
                "description": "None",
                "reason": "Akamai Intelligence (DNS)",
                "onRamp": "No",
                "threatId": 5070,
                "severityId": 2,
                "threatName": "Known Malware",
                "severityLevel": "High",
                "onrampType": "",
                "internalClientIP": "N/A",
                "clientRequestId": "",
                "policyEvaluationSource": "dns"
            }
        },
        {
            "id": "3",
            "configId": "1041",
            "l7Protocol": "DNS",
            "query": {
                "time": "2020-05-26T06:34:51Z",
                "clientIp": "198.18.179.121",
                "dnsIp": "198.18.193.241",
                "domain": "1590449691.akamaietpmalwaretest.com.",
                "uuid": "198.18.193.241-198.18.179.134-1590474891-42367-7406",
                "queryType": "A",
                "deviceId": "N/A",
                "deviceName": "Not Available",
                "resolved": [
                    {
                        "type": "A",
                        "response": "34.193.182.244",
                        "asn": "14618",
                        "asname": "aws"
                    }
                ]
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "domain",
                "detectionTime": "2020-05-26T06:34:51Z",
                "detectionType": "inline",
                "siteId": "-1",
                "siteName": "Unidentified IPs",
                "policyId": "2240",
                "policyName": "Default",
                "listId": "1",
                "listName": "Malware",
                "categoryId": "1",
                "categoryName": "Malware",
                "confidenceId": "2",
                "confidenceName": "Known",
                "actionId": "1",
                "actionName": "Monitor",
                "description": "None",
                "reason": "Akamai Intelligence (DNS)",
                "onRamp": "No",
                "threatId": 5070,
                "severityId": 2,
                "threatName": "Known Malware",
                "severityLevel": "High",
                "onrampType": "",
                "internalClientIP": "N/A",
                "clientRequestId": "",
                "policyEvaluationSource": "dns"
            }
        },
        {
            "id": "4",
            "configId": "1041",
            "l7Protocol": "DNS",
            "query": {
                "time": "2020-05-26T06:34:51Z",
                "clientIp": "198.18.179.121",
                "dnsIp": "198.18.193.241",
                "domain": "1590449691.akamaietpmalwaretest.com.e2e-etp.org.",
                "uuid": "198.18.193.241-198.18.179.134-1590474891-5081-49572",
                "queryType": "AAAA",
                "deviceId": "N/A",
                "deviceName": "Not Available",
                "resolved": [
                    {
                        "type": "N/A",
                        "response": "N/A",
                        "asn": "N/A",
                        "asname": "N/A"
                    }
                ]
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "domain",
                "detectionTime": "2020-05-26T06:34:51Z",
                "detectionType": "inline",
                "siteId": "-1",
                "siteName": "Unidentified IPs",
                "policyId": "2240",
                "policyName": "Default",
                "listId": "4",
                "listName": "DNS Exfiltration",
                "categoryId": "5",
                "categoryName": "DNS Exfiltration",
                "confidenceId": "1",
                "confidenceName": "Suspected",
                "actionId": "1",
                "actionName": "Monitor",
                "description": "None",
                "reason": "Akamai Intelligence (DNS)",
                "onRamp": "No",
                "threatId": 5135,
                "severityId": 4,
                "threatName": "Suspected DNS tunneling",
                "severityLevel": "Low",
                "onrampType": "",
                "internalClientIP": "N/A",
                "clientRequestId": "",
                "policyEvaluationSource": "dns"
            }
        }
    ]
}
```
</details>

### DNS Activity
Additional information regarding the log fields can be found [here](https://techdocs.akamai.com/etp-reporting/reference/post-dns-activities-details)

<details>
    <summary>DNS Activity Event example (JSON)</summary>
```json
{
    "pageInfo": {
        "totalRecords": 685134,
        "pageNumber": 1,
        "pageSize": 5
    },
    "dataRows": [
        {
            "id": "0",
            "configId": "1041",
            "hitCount": 1,
            "alexaRanking": -1,
            "query": {
                "time": "2020-05-26T06:00:00Z",
                "clientIp": "198.18.179.121",
                "dnsIp": "198.18.193.241",
                "domain": "1590448430.akamaietpmalwaretest.com.",
                "queryType": "A",
                "deviceId": "N/A",
                "deviceName": "Not Available",
                "resolved": [
                    {
                        "type": "A",
                        "response": "34.193.182.244",
                        "asn": "14618",
                        "asname": "aws"
                    }
                ]
            },
            "event": {
                "trigger": "null",
                "siteId": "-1",
                "siteName": "Unidentified IPs",
                "policyId": "2240",
                "policyName": "Default",
                "confidenceName": "Unknown",
                "actionId": "1",
                "actionName": "Monitor",
                "onRamp": "No",
                "onrampType": "",
                "internalClientIP": "N/A",
                "clientRequestId": "",
                "policyEvaluationSource": "dns",
                "deepScanned": false
            }
        },
        {
            "id": "1",
            "configId": "1041",
            "hitCount": 1,
            "alexaRanking": 1000,
            "query": {
                "time": "2020-05-26T06:00:00Z",
                "clientIp": "172.25.174.232",
                "dnsIp": "198.18.193.241",
                "domain": "spocs.getpocket.com.",
                "queryType": "A",
                "deviceId": "c37a4c4e-a7cd-400f-820d-b82762c52975",
                "deviceName": "BOS-WPX5E",
                "resolved": [
                    {
                        "type": "A",
                        "response": "50.16.145.165",
                        "asn": "14618",
                        "asname": "aws"
                    },
                    {
                        "type": "A",
                        "response": "35.169.67.87",
                        "asn": "14618",
                        "asname": "aws"
                    },
                    {
                        "type": "A",
                        "response": "52.202.154.119",
                        "asn": "14618",
                        "asname": "aws"
                    },
                    {
                        "type": "A",
                        "response": "52.204.41.228",
                        "asn": "14618",
                        "asname": "aws"
                    }
                ]
            },
            "event": {
                "trigger": "null",
                "siteId": "51284",
                "siteName": "E2E WIN 174.232 site",
                "policyId": "38307",
                "policyName": "E2E-CML-test",
                "confidenceName": "Unknown",
                "actionId": "6",
                "actionName": "Classify",
                "onRamp": "Yes",
                "onrampType": "etp-client",
                "internalClientIP": "N/A",
                "clientRequestId": "00019313",
                "policyEvaluationSource": "dns",
                "deepScanned": false
            }
        },
        {
            "id": "2",
            "configId": "1041",
            "hitCount": 1,
            "alexaRanking": 1000000,
            "query": {
                "time": "2020-05-26T06:00:00Z",
                "clientIp": "172.25.162.210",
                "dnsIp": "198.18.193.241",
                "domain": "cme-linuscmewlhrwlhr-013-wlhr-public.wbx2.com.",
                "queryType": "A",
                "deviceId": "dc475a9e-c192-4b0b-a34e-a95c0f8dfcad",
                "deviceName": "WIN81-ENT-210",
                "resolved": [
                    {
                        "type": "A",
                        "response": "62.109.242.31",
                        "asn": "13445",
                        "asname": "N/A"
                    }
                ]
            },
            "event": {
                "trigger": "null",
                "siteId": "5003",
                "siteName": "Off Network ETP Clients",
                "policyId": "32965",
                "policyName": "Westford OFF Network policy",
                "confidenceName": "Unknown",
                "actionId": "10",
                "actionName": "Bypass",
                "onRamp": "No",
                "onrampType": "",
                "internalClientIP": "N/A",
                "clientRequestId": "00019274",
                "policyEvaluationSource": "dns",
                "deepScanned": false
            }
        },
        {
            "id": "3",
            "configId": "1041",
            "hitCount": 1,
            "alexaRanking": -1,
            "query": {
                "time": "2020-05-26T06:00:00Z",
                "clientIp": "198.18.179.121",
                "dnsIp": "198.18.193.241",
                "domain": "1590447770.akamaietpmalwaretest.com.",
                "queryType": "A",
                "deviceId": "N/A",
                "deviceName": "Not Available",
                "resolved": [
                    {
                        "type": "A",
                        "response": "34.193.182.244",
                        "asn": "14618",
                        "asname": "aws"
                    }
                ]
            },
            "event": {
                "trigger": "null",
                "siteId": "-1",
                "siteName": "Unidentified IPs",
                "policyId": "2240",
                "policyName": "Default",
                "confidenceName": "Unknown",
                "actionId": "1",
                "actionName": "Monitor",
                "onRamp": "No",
                "onrampType": "",
                "internalClientIP": "N/A",
                "clientRequestId": "",
                "policyEvaluationSource": "dns",
                "deepScanned": false
            }
        },
        {
            "id": "4",
            "configId": "1041",
            "hitCount": 1,
            "alexaRanking": 1000000,
            "query": {
                "time": "2020-05-26T06:00:00Z",
                "clientIp": "198.18.179.159",
                "dnsIp": "198.18.193.241",
                "domain": "e6589.dscb.akamaiedge.net.",
                "queryType": "A",
                "deviceId": "630ace6b-4f26-41df-b411-cd652512cb04",
                "deviceName": "Lab-Mac-19818179159.local",
                "resolved": [
                    {
                        "type": "A",
                        "response": "23.204.70.172",
                        "asn": "20940",
                        "asname": "qwest"
                    }
                ]
            },
            "event": {
                "trigger": "null",
                "siteId": "51277",
                "siteName": "E2E Mac 179.159 site",
                "policyId": "38307",
                "policyName": "E2E-CML-test",
                "confidenceName": "Unknown",
                "actionId": "10",
                "actionName": "Bypass",
                "onRamp": "No",
                "onrampType": "",
                "internalClientIP": "N/A",
                "clientRequestId": "00032083",
                "policyEvaluationSource": "dns",
                "deepScanned": false
            }
        }
    ]
}
```
</details>

### PROXY

Additional information regarding the log fields can be found [here](https://techdocs.akamai.com/etp-reporting/reference/post-traffic-transaction-details)

<details>
    <summary>Proxy Activity Event example (JSON)</summary>
```json
{
    "pageInfo": {
        "totalRecords": 44583,
        "pageNumber": 1,
        "pageSize": 5
    },
    "dataRows": [
        {
            "id": "0",
            "l7Protocol": "HTTP",
            "isEvent": true,
            "request": {
                "startTime": 1590474813791,
                "connectionId": "0x3706B3124FAFAF8C9574",
                "domain": "statsfe2.ws.microsoft.com.",
                "uri": "/ReportingWebService/ReportingWebService.asmx",
                "method": "POST",
                "clientPort": 48176,
                "destinationIP": "52.183.47.176",
                "destinationPort": 80,
                "uuid": "1b72e77c-254a-4ba9-a456-2a1b4407d65b",
                "clientIp": "172.25.162.210",
                "queryStrings": [],
                "headers": [
                    {
                        "name": "Cache-Control",
                        "value": "no-cache"
                    },
                    {
                        "name": "Content-Length",
                        "value": "2369"
                    },
                    {
                        "name": "Content-Type",
                        "value": "text/xml; charset=utf-8"
                    },
                    {
                        "name": "Host",
                        "value": "statsfe2.ws.microsoft.com"
                    },
                    {
                        "name": "Pragma",
                        "value": "no-cache"
                    },
                    {
                        "name": "User-Agent",
                        "value": "Windows-Update-Agent/7.9.9600.19670 Client-Protocol/1.21 EtpClient:3.0.0"
                    },
                    {
                        "name": "X-Forwarded-For",
                        "value": "172.25.162.210, 172.25.162.210"
                    }
                ]
            },
            "response": {
                "endTime": 1590474813793,
                "hash": "",
                "headers": []
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "null",
                "detectionTime": "2020-05-26T06:33:33Z",
                "detectionType": "inline",
                "siteId": "5003",
                "siteName": "Off Network ETP Clients",
                "policyId": "32965",
                "policyName": "Westford OFF Network policy",
                "listId": "-1",
                "listName": "unknown",
                "categoryId": "73",
                "categoryName": "73",
                "confidenceId": "-1",
                "confidenceName": "Unknown",
                "actionId": "4",
                "actionName": "Block - Error Page",
                "blockDescription": "The URL hosts malware.",
                "reason": "Acceptable use policy",
                "severityId": 0,
                "severityLevel": "Unclassified",
                "onrampType": "etp_offnet_client",
                "internalClientIP": "172.25.162.210",
                "clientRequestId": "dc475a9e-c192-4b0b-a34e-a95c0f8dfcad-15904747363383674-1195",
                "deepscanReportPath": "",
                "httpVersion": "1.1",
                "httpUserAgent": "Windows-Update-Agent/7.9.9600.19670 Client-Protocol/1.21 EtpClient:3.0.0",
                "deviceId": "dc475a9e-c192-4b0b-a34e-a95c0f8dfcad",
                "deviceName": "WIN81-ENT-210",
                "deepScanned": false,
                "matchedGroups": [],
                "listIdentifiers": [
                    {
                        "listId": -1,
                        "categoryId": 73,
                        "confidenceId": -1,
                        "threatId": 0,
                        "listName": "unknown",
                        "categoryName": "73",
                        "confidenceName": "Unknown",
                        "threatName": "Unclassified"
                    }
                ]
            },
            "userIdentity": {
                "encryptedUserID": "",
                "encryptedUserName": "",
                "groups": []
            }
        },
        {
            "id": "1",
            "l7Protocol": "HTTPS",
            "isEvent": false,
            "request": {
                "startTime": 1590474750161,
                "connectionId": "0x3706B30F4FAEB4B27FB1",
                "domain": "statics.teams.cdn.office.net.",
                "uri": "/evergreen-assets/icons/1x1-000000ff.png",
                "method": "GET",
                "clientPort": 34656,
                "destinationIP": "2600:1409:d000::17df:3490",
                "destinationPort": 443,
                "uuid": "38c91e98-37fc-40f0-876e-ba60104b4d35",
                "clientIp": "172.25.174.232",
                "queryStrings": [
                    {
                        "name": "cb",
                        "value": "1590474712726"
                    }
                ],
                "headers": [
                    {
                        "name": "Accept",
                        "value": "image/webp,image/apng,image/*,*/*;q=0.8"
                    },
                    {
                        "name": "Accept-Encoding",
                        "value": "gzip, deflate, br"
                    },
                    {
                        "name": "Accept-Language",
                        "value": "en-US"
                    },
                    {
                        "name": "Connection",
                        "value": "keep-alive"
                    },
                    {
                        "name": "Host",
                        "value": "statics.teams.cdn.office.net"
                    },
                    {
                        "name": "Referer",
                        "value": "https://teams.microsoft.com/_"
                    },
                    {
                        "name": "User-Agent",
                        "value": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Teams/1.3.00.12058 Chrome/69.0.3497.128 Electron/4.2.12 Safari/537.36"
                    }
                ]
            },
            "response": {
                "endTime": 1590474750226,
                "hash": "",
                "headers": [
                    {
                        "name": "Access-Control-Allow-Origin",
                        "value": "*"
                    },
                    {
                        "name": "Cache-Control",
                        "value": "public, max-age=604777"
                    },
                    {
                        "name": "Connection",
                        "value": "keep-alive"
                    },
                    {
                        "name": "Content-Length",
                        "value": "68"
                    },
                    {
                        "name": "Content-MD5",
                        "value": "5E5+z+yZNWYywTzT6qPiUA=="
                    },
                    {
                        "name": "Content-Type",
                        "value": "image/png"
                    },
                    {
                        "name": "Date",
                        "value": "Tue, 26 May 2020 06:32:30 GMT"
                    },
                    {
                        "name": "ETag",
                        "value": "\"0x8D6D3F4152295F5\""
                    },
                    {
                        "name": "Last-Modified",
                        "value": "Wed, 08 May 2019 20:30:59 GMT"
                    },
                    {
                        "name": "Server",
                        "value": "Windows-Azure-Blob/1.0 Microsoft-HTTPAPI/2.0"
                    }
                ]
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "null",
                "detectionTime": "2020-05-26T06:32:30Z",
                "detectionType": "N/A",
                "siteId": "51284",
                "siteName": "E2E WIN 174.232 site",
                "policyId": "0",
                "policyName": "0",
                "listId": "-1",
                "listName": "unknown",
                "categoryId": "104",
                "categoryName": "104",
                "confidenceId": "-1",
                "confidenceName": "Unknown",
                "actionId": "5",
                "actionName": "Allow",
                "blockDescription": "The URL hosts malware.",
                "reason": "Acceptable use policy",
                "severityId": 0,
                "severityLevel": "Unclassified",
                "onrampType": "etp_client",
                "internalClientIP": "172.25.174.232",
                "clientRequestId": "c37a4c4e-a7cd-400f-820d-b82762c52975-15904747127323964-48715",
                "deepscanReportPath": "",
                "httpVersion": "1.1",
                "httpUserAgent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Teams/1.3.00.12058 Chrome/69.0.3497.128 Electron/4.2.12 Safari/537.36 EtpClient:3.0.0",
                "deviceId": "c37a4c4e-a7cd-400f-820d-b82762c52975",
                "deviceName": "BOS-WPX5E",
                "deepScanned": false,
                "matchedGroups": [],
                "listIdentifiers": [
                    {
                        "listId": -1,
                        "categoryId": 104,
                        "confidenceId": -1,
                        "threatId": 0,
                        "listName": "unknown",
                        "categoryName": "104",
                        "confidenceName": "Unknown",
                        "threatName": "Unclassified"
                    }
                ]
            },
            "userIdentity": {
                "encryptedUserID": "",
                "encryptedUserName": "",
                "groups": []
            }
        },
        {
            "id": "2",
            "l7Protocol": "HTTPS",
            "isEvent": false,
            "request": {
                "startTime": 1590474718273,
                "connectionId": "0x3706B3154FAE37181163A",
                "domain": "clickstream-killswitch.hd-personalization-prod.gcp.example.com.",
                "uri": "/clickstream-killswitch/v1/detail",
                "method": "GET",
                "clientPort": 42380,
                "destinationIP": "130.211.21.250",
                "destinationPort": 443,
                "uuid": "a1d7f692-c932-466a-82f6-e4e85bba7864",
                "clientIp": "172.25.174.232",
                "queryStrings": [],
                "headers": [
                    {
                        "name": "Accept",
                        "value": "*/*"
                    },
                    {
                        "name": "Accept-Encoding",
                        "value": "gzip, deflate, br"
                    },
                    {
                        "name": "Accept-Language",
                        "value": "en-US,en;q=0.9"
                    },
                    {
                        "name": "Connection",
                        "value": "keep-alive"
                    },
                    {
                        "name": "content-type",
                        "value": "application/json"
                    },
                    {
                        "name": "Host",
                        "value": "clickstream-killswitch.hd-personalization-prod.gcp.example.com"
                    },
                    {
                        "name": "Origin",
                        "value": "https://www.example.com"
                    },
                    {
                        "name": "Referer",
                        "value": "https://www.example.com/"
                    },
                    {
                        "name": "User-Agent",
                        "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
                    }
                ]
            },
            "response": {
                "endTime": 1590474718348,
                "hash": "",
                "headers": [
                    {
                        "name": "Access-Control-Allow-Origin",
                        "value": "https://www.example.com"
                    },
                    {
                        "name": "Content-Length",
                        "value": "1329"
                    },
                    {
                        "name": "Content-Type",
                        "value": "application/json;charset=UTF-8"
                    },
                    {
                        "name": "Date",
                        "value": "Tue, 26 May 2020 06:31:57 GMT"
                    },
                    {
                        "name": "Vary",
                        "value": "Origin, Access-Control-Request-Method, Access-Control-Request-Headers"
                    },
                    {
                        "name": "Via",
                        "value": "1.1 google"
                    }
                ]
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "null",
                "detectionTime": "2020-05-26T06:31:58Z",
                "detectionType": "N/A",
                "siteId": "51284",
                "siteName": "E2E WIN 174.232 site",
                "policyId": "0",
                "policyName": "0",
                "listId": "-1",
                "listName": "unknown",
                "categoryId": "55",
                "categoryName": "Streaming Websites",
                "confidenceId": "-1",
                "confidenceName": "Unknown",
                "actionId": "5",
                "actionName": "Allow",
                "blockDescription": "The URL hosts malware.",
                "reason": "Acceptable use policy",
                "severityId": 0,
                "severityLevel": "Unclassified",
                "onrampType": "etp_client",
                "internalClientIP": "172.25.174.232",
                "clientRequestId": "c37a4c4e-a7cd-400f-820d-b82762c52975-15904746798952196-48708",
                "deepscanReportPath": "",
                "httpVersion": "1.1",
                "httpUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 EtpClient:3.0.0",
                "deviceId": "c37a4c4e-a7cd-400f-820d-b82762c52975",
                "deviceName": "BOS-WPX5E",
                "deepScanned": false,
                "matchedGroups": [],
                "listIdentifiers": [
                    {
                        "listId": -1,
                        "categoryId": 55,
                        "confidenceId": -1,
                        "threatId": 0,
                        "listName": "unknown",
                        "categoryName": "Streaming Websites",
                        "confidenceName": "Unknown",
                        "threatName": "Unclassified"
                    },
                    {
                        "listId": -1,
                        "categoryId": 73,
                        "confidenceId": -1,
                        "threatId": 0,
                        "listName": "unknown",
                        "categoryName": "73",
                        "confidenceName": "Unknown",
                        "threatName": "Unclassified"
                    }
                ]
            },
            "userIdentity": {
                "encryptedUserID": "",
                "encryptedUserName": "",
                "groups": []
            }
        },
        {
            "id": "3",
            "l7Protocol": "HTTPS",
            "isEvent": true,
            "request": {
                "startTime": 1590474706144,
                "connectionId": "0x3706B3154FAE084111637",
                "domain": "c.go-mpulse.net.",
                "uri": "/api/config.json",
                "method": "GET",
                "clientPort": 41176,
                "destinationIP": "2600:1409:d000:38e::11a6",
                "destinationPort": 443,
                "uuid": "8e86b32f-9a83-4162-a008-3e2c58b09f87",
                "clientIp": "172.25.174.232",
                "queryStrings": [
                    {
                        "name": "key",
                        "value": "FDSGP-LEB9B-T8Y2A-5V5ED-9WX2T"
                    },
                    {
                        "name": "d",
                        "value": "www.akamai.com"
                    },
                    {
                        "name": "t",
                        "value": "5301582"
                    },
                    {
                        "name": "v",
                        "value": "1.667.0"
                    },
                    {
                        "name": "if",
                        "value": ""
                    },
                    {
                        "name": "sl",
                        "value": "0"
                    },
                    {
                        "name": "si",
                        "value": "876aebf5-a115-47de-973b-9ac2ba2cdd1c-qaqswv"
                    },
                    {
                        "name": "r",
                        "value": ""
                    },
                    {
                        "name": "bcn",
                        "value": "%2F%2F173e2548.akstat.io%2F"
                    },
                    {
                        "name": "acao",
                        "value": ""
                    },
                    {
                        "name": "ak.ai",
                        "value": "593889"
                    }
                ],
                "headers": [
                    {
                        "name": "Accept",
                        "value": "*/*"
                    },
                    {
                        "name": "Accept-Encoding",
                        "value": "gzip, deflate, br"
                    },
                    {
                        "name": "Accept-Language",
                        "value": "en-US,en;q=0.9"
                    },
                    {
                        "name": "Connection",
                        "value": "keep-alive"
                    },
                    {
                        "name": "Host",
                        "value": "c.go-mpulse.net"
                    },
                    {
                        "name": "Origin",
                        "value": "https://www.akamai.com"
                    },
                    {
                        "name": "User-Agent",
                        "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
                    }
                ]
            },
            "response": {
                "endTime": 1590474706146,
                "hash": "",
                "headers": []
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "null",
                "detectionTime": "2020-05-26T06:31:46Z",
                "detectionType": "inline",
                "siteId": "51284",
                "siteName": "E2E WIN 174.232 site",
                "policyId": "38307",
                "policyName": "E2E-CML-test",
                "listId": "-1",
                "listName": "unknown",
                "categoryId": "31",
                "categoryName": "Chat Site",
                "confidenceId": "-1",
                "confidenceName": "Unknown",
                "actionId": "4",
                "actionName": "Block - Error Page",
                "blockDescription": "The URL hosts malware.",
                "reason": "Acceptable use policy",
                "severityId": 0,
                "severityLevel": "Unclassified",
                "onrampType": "etp_client",
                "internalClientIP": "172.25.174.232",
                "clientRequestId": "c37a4c4e-a7cd-400f-820d-b82762c52975-15904746699129224-48707",
                "deepscanReportPath": "",
                "httpVersion": "1.1",
                "httpUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 EtpClient:3.0.0",
                "deviceId": "c37a4c4e-a7cd-400f-820d-b82762c52975",
                "deviceName": "BOS-WPX5E",
                "deepScanned": false,
                "matchedGroups": [],
                "listIdentifiers": [
                    {
                        "listId": -1,
                        "categoryId": 31,
                        "confidenceId": -1,
                        "threatId": 0,
                        "listName": "unknown",
                        "categoryName": "Chat Site",
                        "confidenceName": "Unknown",
                        "threatName": "Unclassified"
                    }
                ]
            },
            "userIdentity": {
                "encryptedUserID": "",
                "encryptedUserName": "",
                "groups": []
            }
        },
        {
            "id": "4",
            "l7Protocol": "HTTPS",
            "isEvent": false,
            "request": {
                "startTime": 1590474688053,
                "connectionId": "0x3706B3124FADC2CF9570",
                "domain": "d.la1-c2-ia4.salesforceliveagent.com.",
                "uri": "/chat/rest/Visitor/Availability.jsonp",
                "method": "GET",
                "clientPort": 43149,
                "destinationIP": "13.110.63.55",
                "destinationPort": 443,
                "uuid": "7b33eedd-8b7d-463b-80d9-996b74a0a9ee",
                "clientIp": "172.25.174.232",
                "queryStrings": [
                    {
                        "name": "sid",
                        "value": "409d47de-bf85-433c-9c88-79add325835a"
                    },
                    {
                        "name": "r",
                        "value": "906"
                    },
                    {
                        "name": "Availability.prefix",
                        "value": "Visitor"
                    },
                    {
                        "name": "Availability.ids",
                        "value": "[5730f000000HhB2,5730f000000HhAJ,5730f000000HhAY]"
                    },
                    {
                        "name": "callback",
                        "value": "liveagent._.handlePing"
                    },
                    {
                        "name": "deployment_id",
                        "value": "5720f0000009HUh"
                    },
                    {
                        "name": "org_id",
                        "value": "00DA0000000Hu5a"
                    },
                    {
                        "name": "version",
                        "value": "43"
                    }
                ],
                "headers": [
                    {
                        "name": "Accept",
                        "value": "*/*"
                    },
                    {
                        "name": "Accept-Encoding",
                        "value": "gzip, deflate, br"
                    },
                    {
                        "name": "Accept-Language",
                        "value": "en-US,en;q=0.9"
                    },
                    {
                        "name": "Connection",
                        "value": "keep-alive"
                    },
                    {
                        "name": "Host",
                        "value": "d.la1-c2-ia4.salesforceliveagent.com"
                    },
                    {
                        "name": "User-Agent",
                        "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
                    }
                ]
            },
            "response": {
                "endTime": 1590474688139,
                "hash": "",
                "headers": [
                    {
                        "name": "Access-Control-Allow-Origin",
                        "value": "*"
                    },
                    {
                        "name": "Cache-Control",
                        "value": "no-cache"
                    },
                    {
                        "name": "Connection",
                        "value": "close"
                    },
                    {
                        "name": "Content-Encoding",
                        "value": "gzip"
                    },
                    {
                        "name": "Content-Type",
                        "value": "text/javascript"
                    },
                    {
                        "name": "Expires",
                        "value": "-1"
                    },
                    {
                        "name": "Pragma",
                        "value": "no-cache"
                    },
                    {
                        "name": "X-Content-Type-Options",
                        "value": "nosniff"
                    }
                ]
            },
            "event": {
                "correlatedSinkholeEvents": [
                    {
                        "sinkholeId": "ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11",
                        "eventId": "1590113794976#ac4bde1e-7d3d-4ff5-9cf8-772df0b1ce11#28301",
                        "sourcePort": 48022,
                        "destinationPort": 80,
                        "l4Protocol": "TCP",
                        "hostname": "akamaietpcnctest.com",
                        "userAgent": "curl/7.47.0",
                        "l7Protocol": "HTTP",
                        "eventTime": "2020-05-22T02:16:34Z",
                        "url": "/",
                        "sinkholeName": "ETP_DNS_SINKHOLE",
                        "hitCount": 1,
                        "configId": 1041,
                        "internalIP": "198.18.179.187",
                        "sinkholeIP": "172.25.162.242",
                        "machineNames": [
                            "N/A"
                        ]
                    }
                ],
                "trigger": "null",
                "detectionTime": "2020-05-26T06:31:28Z",
                "detectionType": "N/A",
                "siteId": "51284",
                "siteName": "E2E WIN 174.232 site",
                "policyId": "0",
                "policyName": "0",
                "listId": "-1",
                "listName": "unknown",
                "categoryId": "73",
                "categoryName": "73",
                "confidenceId": "-1",
                "confidenceName": "Unknown",
                "actionId": "5",
                "actionName": "Allow",
                "blockDescription": "The URL hosts malware.",
                "reason": "Acceptable use policy",
                "severityId": 0,
                "severityLevel": "Unclassified",
                "onrampType": "etp_client",
                "internalClientIP": "172.25.174.232",
                "clientRequestId": "c37a4c4e-a7cd-400f-820d-b82762c52975-15904746509095241-48705",
                "deepscanReportPath": "",
                "httpVersion": "1.1",
                "httpUserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 EtpClient:3.0.0",
                "deviceId": "c37a4c4e-a7cd-400f-820d-b82762c52975",
                "deviceName": "BOS-WPX5E",
                "deepScanned": false,
                "matchedGroups": [],
                "listIdentifiers": [
                    {
                        "listId": -1,
                        "categoryId": 73,
                        "confidenceId": -1,
                        "threatId": 0,
                        "listName": "unknown",
                        "categoryName": "73",
                        "confidenceName": "Unknown",
                        "threatName": "Unclassified"
                    }
                ]
            },
            "userIdentity": {
                "encryptedUserID": "",
                "encryptedUserName": "",
                "groups": []
            }
        }
    ]
}
```
</details>

### NETCON
Additional information regarding the log fields can be found [here](https://techdocs.akamai.com/etp-reporting/reference/post-network-traffic-connections-details)

<details>
    <summary>Network Connection Event example (JSON)</summary>
```json
{
    "id": "123",
    "connectionId": "0xABCDEF1234567890",
    "domain": "123.123.123.123",
    "connStartTime": "2023-08-23T07:59:11Z",
    "connEndTime": "2023-08-23T07:59:11Z",
    "clientIP": "222.111.222.111",
    "clientPort": 35593,
    "destinationIP": "111.222.111.222",
    "destinationPort": 80,
    "siteId": 1234536,
    "siteName": "ETP DEMO",
    "policyAction": "onramp",
    "onrampType": "explicit_proxy_tls",
    "internalClientIP": "",
    "httpVersion": "N/A",
    "httpUserAgent": "",
    "machineId": "",
    "machineName": "",
    "clientRequestId": "",
    "ovfActionId": -1,
    "ovfActionName": "N/A",
    "stats": {
        "httpRequestCount": 1,
        "inBytes": 0,
        "outBytes": 0
    },
    "dropInfo": {
        "wasDropped": true,
        "droppedReason": "Destination Filter - Internal Host IP"
    },
    "encryptedInternalClientIP": "123123123123123123/ABCDEF",
    "decryptedInternalClientIP": "192.168.11.168",
    "sublocationId": "-1",
    "sublocationName": "N/A",
    "deviceOwnerId": "",
    "encryptedInternalClientName": ""
}
```
</details>

## Akamai MFA (MFA)
Additional information regarding the MFA log fields can be found on [here](https://techdocs.akamai.com/mfa/docs/splunk-app).

### Authentication Logs (AUTH)
Authentication Events Example:  
```json
{
    "uuid": "aud_JfNqdl6zSByrU0ovrbJ6m",
    "created_at": "2021-03-23T19:36:20.047688",
    "browser_ip": "49.207.58.115",
    "app_id": "app_3IyJXh2U9Jiws6bvxcf8X",
    "app_name": "Test Application",
    "device": "push",
    "auth_method": "push",
    "user_id": "user_6Hy1v24DZIr8b0UHYi5dv3",
    "username": "username",
    "is_success": true,
    "device_metadata": "Android",
    "receipt": "",
    "browser_type": "Chrome",
    "browser_version": "88.0.4324",
    "browser_os": "MacOS",
    "browser_os_version": "10.15.7",
    "device_os": "android",
    "device_os_version": "10.0.0",
    "browser_geo_location": "BANGALORE KA, IN",
    "device_geo_location": "BANGALORE KA, IN",
    "device_ip": "49.207.58.115",
    "denial_type": null,
    "device_id": "device_3kbTGOPbHxH3KfYkPzm31e",
    "policy_attr_name": null,
    "policy_uuid": null,
    "principal_type": null,
    "principal_uuid": null
}
```

## Guardicore

### NETLOG
Guardicore netlog example
```json
{
    "id": "123",
    "connectionId": "0xABCDEF1234567890",
    "domain": "123.123.123.123",
    "connStartTime": "2023-08-23T07:59:11Z",
    "connEndTime": "2023-08-23T07:59:11Z",
    "clientIP": "222.111.222.111",
    "clientPort": 35593,
    "destinationIP": "111.222.111.222",
    "destinationPort": 80,
    "siteId": 1234536,
    "siteName": "ETP DEMO",
    "policyAction": "onramp",
    "onrampType": "explicit_proxy_tls",
    "internalClientIP": "",
    "httpVersion": "N/A",
    "httpUserAgent": "",
    "machineId": "",
    "machineName": "",
    "clientRequestId": "",
    "ovfActionId": -1,
    "ovfActionName": "N/A",
    "stats": {
        "httpRequestCount": 1,
        "inBytes": 0,
        "outBytes": 0
    },
    "dropInfo": {
        "wasDropped": true,
        "droppedReason": "Destination Filter - Internal Host IP"
    },
    "encryptedInternalClientIP": "123123123123123123/ABCDEF",
    "decryptedInternalClientIP": "192.168.11.168",
    "sublocationId": "-1",
    "sublocationName": "N/A",
    "deviceOwnerId": "",
    "encryptedInternalClientName": ""
}
```

### INCIDENT
Guardicore incident example
```json
{
      "_cls": "Incident.NetworkVisibilityIncident",
      "_id": "4506a1ba-15d1-4d10-8299-5c10f34975cb",
      "affected_assets": [
        {
          "country": "Israel",
          "country_code": "IL",
          "ip": "172.17.0.3",
          "is_inner": true,
          "labels": [
            "source"
          ],
          "vm": {
            "full_name": "192.168.0.102/Attacker2",
            "id": "b40db74f-5f2d-4cda-9c9b-c2cdd8158b1f",
            "name": "Attacker2",
            "nics": [
              {
                "discovered_ip_addresses": [
                  "192.168.0.1"
                ],
                "ip_addresses": [
                  "192.168.0.1"
                ],
                "mac_address": "00:50:56:bb:2d:ab",
                "network_id": "fe3ef6a8-858f-407d-bd6e-30fb9cc30522",
                "network_name": "CommandsNet",
                "network_orchestration_id": "dvportgroup-105",
                "orchestration_details": [
                  {}
                ],
                "switch_id": "dvs-102",
                "vif_id": "0",
                "vlan_id": 1001
              }
            ],
            "orchestration_details": [
              {
                "orchestration_id": "7f43c9a2-e8b9-4ce7-a2d1-908bd5182d51",
                "orchestration_obj_id": "vm-280588",
                "orchestration_type": "vSphere",
                "revision_id": 190709142948
              }
            ],
            "recent_domains": [
              "mydomain.com"
            ],
            "tenant_name": "192.168.0.102"
          },
          "vm_id": "b40db74f-5f2d-4cda-9c9b-c2cdd8158b1f"
        }
      ],
      "closed_time": 1510979377066,
      "concatenated_tags": [
        {
          "display_name": "Internal",
          "tag_class": "ENRICHER"
        }
      ],
      "destination_asset": {
        "ip": "172.17.0.3",
        "is_inner": true,
        "labels": [
          "destination"
        ],
        "vm": {
          "full_name": "192.168.0.102/Attacker2",
          "id": "b40db74f-5f2d-4cda-9c9b-c2cdd8158b1f",
          "name": "Attacker2",
          "nics": [
            {
              "discovered_ip_addresses": [
                "192.168.0.1"
              ],
              "ip_addresses": [
                "192.168.0.1"
              ],
              "mac_address": "00:50:56:bb:2d:ab",
              "network_id": "fe3ef6a8-858f-407d-bd6e-30fb9cc30522",
              "network_name": "CommandsNet",
              "network_orchestration_id": "dvportgroup-105",
              "orchestration_details": [
                {
                  "orchestration_id": "7f43c9a2-e8b9-4ce7-a2d1-908bd5182d51",
                  "orchestration_obj_id": "vm-280588",
                  "orchestration_type": "vSphere",
                  "revision_id": 190709142948
                }
              ],
              "switch_id": "dvs-102",
              "vif_id": "0",
              "vlan_id": 1001
            }
          ],
          "orchestration_details": [
            {
              "orchestration_id": "7f43c9a2-e8b9-4ce7-a2d1-908bd5182d51",
              "orchestration_obj_id": "vm-280588",
              "orchestration_type": "vSphere",
              "revision_id": 190709142948
            }
          ],
          "recent_domains": [
            "mydomain.com"
          ],
          "tenant_name": "192.168.0.102"
        },
        "vm_id": "74238291-b85a-42fb-bac9-80c402abee04"
      },
      "destination_net": "many",
      "destinations": [
        {
          "ip_int": "1684300813",
          "ports": [
            "ARP"
          ]
        }
      ],
      "direction": "unidirectional",
      "doc_version": 59,
      "end_time": 1504689940953,
      "ended": true,
      "enriched": true,
      "events": [
        {
          "_id": "a120a1ba-15d1-4d10-8299-5c10f34975cb",
          "description": "Scanner detected.",
          "destinations": [
            [
              443,
              "10.0.0.1"
            ]
          ],
          "doc_version": 57,
          "event_source": "DP-422FB8A7-D525-D1A4-B2B8-1ABAD6137A64",
          "event_type": "DatapathScanDetectionEvent",
          "id": "a120a1ba-15d1-4d10-8299-5c10f34975cb",
          "incident_id": "4506a1ba-15d1-4d10-8299-5c10f34975cb",
          "is_experimental": false,
          "processed_time": 1512375007928,
          "received_time": 1512375006000,
          "severity": 40,
          "source_ip": "127.0.0.1",
          "source_vm": {
            "full_name": "192.168.0.102/Attacker2",
            "id": "b40db74f-5f2d-4cda-9c9b-c2cdd8158b1f",
            "name": "Attacker2",
            "nics": [
              {
                "discovered_ip_addresses": [
                  "192.168.0.1"
                ],
                "ip_addresses": [
                  "192.168.0.1"
                ],
                "mac_address": "00:50:56:bb:2d:ab",
                "network_id": "fe3ef6a8-858f-407d-bd6e-30fb9cc30522",
                "network_name": "CommandsNet",
                "network_orchestration_id": "dvportgroup-105",
                "orchestration_details": [
                  {}
                ],
                "switch_id": "dvs-102",
                "vif_id": "0",
                "vlan_id": 1001
              }
            ],
            "orchestration_details": [
              {
                "orchestration_id": "7f43c9a2-e8b9-4ce7-a2d1-908bd5182d51",
                "orchestration_obj_id": "vm-280588",
                "orchestration_type": "vSphere",
                "revision_id": 190709142948
              }
            ],
            "recent_domains": [
              "mydomain.com"
            ],
            "tenant_name": "192.168.0.102"
          },
          "tag_refs": [
            "aa96a1ba-15d1-4d10-8299-5c10f34975cb"
          ],
          "time": 1512374896401,
          "uuid": "a32a528c-293b-4185-80ec-652b435c1297"
        }
      ],
      "experimental_id": "925fd3c9-f933-482f-9eb1-61f61ba4bc3a",
      "first_asset": {
        "asset_id": "2.20.153.161",
        "asset_type": "IP"
      },
      "flow_ids": [
        "17bf0add897bbb7a1bd55c24b9cc7ea5fb92ad6f2dd0be7704734accef4226e6__bd8d287246b85de5334d115adc61a4232fd1d904e6f57cf16c0f7d8adde3eb51__Tcp__80"
      ],
      "has_export": true,
      "has_policy_violations": true,
      "id": "4506a1ba-15d1-4d10-8299-5c10f34975cb",
      "incident_group": [
        {
          "gid": "a7f870fa-85ab-47fe-8156-f5e45e7208eb",
          "gname": "GRP-a7f870fa"
        }
      ],
      "incident_type": "Reveal",
      "iocs": [
        {
          "initiating_tags": [
            "0736307a-8aef-4d42-b4dd-c89da42e9135"
          ],
          "ioc_id": "bfc2399e-9546-4d4a-8989-cf9bcf5426e2",
          "related_tags": [
            "3d7a9595-f293-4c54-addf-4fa22c29725e"
          ],
          "source": "LoginsDetector.detect_successful_logins"
        }
      ],
      "is_experimental": true,
      "labels": [
        "source"
      ],
      "last_updated_time": 1504689940952,
      "originl_id": "",
      "policy_revision": 22,
      "processed_eventS_count": 1,
      "recommendations": [
        {
          "handle_template": "Quarantine File",
          "id": "2206a1ba-15d1-4d10-8299-5c10f34975cb",
          "parts": [
            {
              "type": "text",
              "value": "Quarantine malicious file "
            }
          ],
          "rule_id": "a106a1ba-15d1-4d10-8299-5c10f34975cb",
          "rule_type": "",
          "type": "FileQuarantineRecommendation"
        }
      ],
      "reenrich_count": 0,
      "remote_index": "incidents__2017_12_03_00_00_00",
      "second_asset": {
        "asset_id": "2.20.153.161",
        "asset_type": "IP"
      },
      "sensor_name": "DP-422F8CE0-C6A1-D633-52C4-2EDE049F6094",
      "sensor_type": "VISIBILITY",
      "severity": 40,
      "similarity_calculated": false,
      "source_asset": {
        "ip": "172.17.0.1",
        "is_inner": true,
        "labels": [
          "source"
        ],
        "vm": {
          "full_name": "192.168.0.102/Attacker2",
          "id": "b40db74f-5f2d-4cda-9c9b-c2cdd8158b1f",
          "name": "Attacker2",
          "nics": [
            {
              "discovered_ip_addresses": [
                "192.168.0.1"
              ],
              "ip_addresses": [
                "192.168.0.1"
              ],
              "mac_address": "00:50:56:bb:2d:ab",
              "network_id": "fe3ef6a8-858f-407d-bd6e-30fb9cc30522",
              "network_name": "CommandsNet",
              "network_orchestration_id": "dvportgroup-105",
              "orchestration_details": [
                {
                  "orchestration_id": "7f43c9a2-e8b9-4ce7-a2d1-908bd5182d51",
                  "orchestration_obj_id": "vm-280588",
                  "orchestration_type": "vSphere",
                  "revision_id": 190709142948
                }
              ],
              "switch_id": "dvs-102",
              "vif_id": "0",
              "vlan_id": 1001
            }
          ],
          "orchestration_details": [
            {
              "orchestration_id": "7f43c9a2-e8b9-4ce7-a2d1-908bd5182d51",
              "orchestration_obj_id": "vm-280588",
              "orchestration_type": "vSphere",
              "revision_id": 190709142948
            }
          ],
          "recent_domains": [
            "mydomain.com"
          ],
          "tenant_name": "192.168.0.102"
        },
        "vm_id": "11338291-b85a-42fb-bac9-80c402abee04"
      },
      "source_ip": "10.0.0.1",
      "source_vm": {
        "full_name": "192.168.0.102/Attacker2",
        "id": "b40db74f-5f2d-4cda-9c9b-c2cdd8158b1f",
        "name": "Attacker2",
        "nics": [
          {
            "discovered_ip_addresses": [
              "192.168.0.1"
            ],
            "ip_addresses": [
              "192.168.0.1"
            ],
            "mac_address": "00:50:56:bb:2d:ab",
            "network_id": "fe3ef6a8-858f-407d-bd6e-30fb9cc30522",
            "network_name": "CommandsNet",
            "network_orchestration_id": "dvportgroup-105",
            "orchestration_details": [
              {
                "orchestration_id": "7f43c9a2-e8b9-4ce7-a2d1-908bd5182d51",
                "orchestration_obj_id": "vm-280588",
                "orchestration_type": "vSphere",
                "revision_id": 190709142948
              }
            ],
            "switch_id": "dvs-102",
            "vif_id": "0",
            "vlan_id": 1001
          }
        ],
        "orchestration_details": [
          {
            "orchestration_id": "7f43c9a2-e8b9-4ce7-a2d1-908bd5182d51",
            "orchestration_obj_id": "vm-280588",
            "orchestration_type": "vSphere",
            "revision_id": 190709142948
          }
        ],
        "recent_domains": [
          "mydomain.com"
        ],
        "tenant_name": "192.168.0.102"
      },
      "source_vm_id": "74238291-b85a-42fb-bac9-80c402abee04",
      "start_time": 1504688829035,
      "total_events_count": 
}
```

## Linode
### AUDIT Logs
Additional information regarding the log fields can be found on [here](https://www.linode.com/docs/api/account/#events-list)

```json
{
      "action": "ticket_create",
      "created": "2018-01-01T00:01:01",
      "duration": 300.56,
      "entity": {
        "id": 11111,
        "label": "Problem booting my Linode",
        "type": "ticket",
        "url": "/v4/support/tickets/11111"
      },
      "id": 123,
      "message": "None",
      "percent_complete": null,
      "rate": null,
      "read": true,
      "secondary_entity": {
        "id": "linode/debian9",
        "label": "linode1234",
        "type": "linode",
        "url": "/v4/linode/instances/1234"
      },
      "seen": true,
      "status": null,
      "time_remaining": null,
      "username": "exampleUser"
    }
```

