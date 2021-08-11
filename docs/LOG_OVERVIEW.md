# Log Overview
ULS supports ingestion of different log streams into SIEM. To get the highest value out of the ingested data, it is crucial to understand the delivered data.  
Here are some examples (per product) and links to additional information.

## Overview
- [Enterprise Application Access](#enterprise-application-access)
  - [Access Logs (ACCESS)](#access-logs-access)
  - [Admin Logs(ADMIN)](#admin-logs-admin)
  - [Connector Health(CONHEALTH)](#connector-health-conhealth)
- [Enterprise Threat Protector](#etp)
  - [Threat Logs]()
  - [Accceptable Use Policy Logs (AUP)]()
- [Akamai MFA](#akamai-mfa)
  - [Authentication Logs (AUTH)](#authentication-logs) 
  - [Policy Logs(POLICY)](#policy-logs)

## Enterprise Application Access
### Access Logs (ACCESS)
Additional information regarding the log fields can be found on [here](https://learn.akamai.com/en-us/webhelp/enterprise-application-access/eaa-logs-from-eaa-api-and-splunk/GUID-8F07B320-2DD7-4035-9A8E-4E7435DFA3EA.html)
```text
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
Additional information regarding the log fields can be found on [here](https://learn.akamai.com/en-us/webhelp/enterprise-application-access/eaa-logs-from-eaa-api-and-splunk/GUID-F772F01C-46D1-411C-A41F-D4B780D998FB.html).
```text
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
Additional information regarding the log fields can be found on [here](https://learn.akamai.com/en-us/webhelp/enterprise-application-access/eaa-logs-from-eaa-api-and-splunk/GUID-A79FBF43-DE2C-405A-8900-0D77DC8CEAF4.html)
```text
{
    "connector_uuid": "cht3_GEjQWyMW9LEk7KQfg",
    "name": "demo-v2-con-1-amer",
    "reachable": 1,
    "status": 1,
    "version": "21.01.0-152",
    "privateip": "10.1.4.206",
    "publicip": "123.123.123.123",
    "debugchan": "Y",
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

## Enterprise Threat Protector (ETP)
### Threat Log (THREAT)
Additional information regarding the log fields can be found on [here](https://developer.akamai.com/api/enterprise_security/enterprise_threat_protector_reporting/v3.html#threatevent)
```text
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

### Accceptable Use Policy Logs (AUP)
Additional information regarding the log fields can be found on [here](https://developer.akamai.com/api/enterprise_security/enterprise_threat_protector_reporting/v3.html#event)
```text
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


## Akamai MFA
Additional information regarding the log fields can be found on [here](https://learn.akamai.com/en-us/webhelp/enterprise-mfa/akamai-mfa-logs-from-splunk-application/GUID-0F17296F-90F3-483E-AFDE-F98FBC51A8AC.html).
### Authentication Logs (AUTH)
Authentication Events Example:  
```text
{"uuid": "aud_JfNqdl6zSByrU0ovrbJ6m", "created_at": "2021-03-23T19:36:20.047688", "browser_ip": "49.207.58.115", "app_id": "app_3IyJXh2U9Jiws6bvxcf8X", "device": "push", "auth_method": "push", "user_id": "user_6Hy1v24DZIr8b0UHYi5dv3", "username": "nityagi", "is_success": true, "device_metadata": "Android", "receipt": "", "browser_type": "Chrome", "browser_version": "88.0.4324", "browser_os": "MacOS", "browser_os_version": "10.15.7", "device_os": "android", "device_os_version": "10.0.0", "browser_geo_location": "BANGALORE KA, IN", "device_geo_location": "BANGALORE KA, IN", "device_ip": "49.207.58.115"}
```

### Policy Logs (POLICY)
Policy Denied Events Example:  
```text
{"id": "aud_5mRypRCazgr8ucRJtICVJt", "created_at": "2021-03-23T17:20:50.524672", "user_id": "user_3CbCStOKG0uGdjRILocuxW", "principal_id": "Tenant", "policy_id": "policy_5iMncPFO8euHE8JRviQL4j", "policy_attribute_name": "Existing User"}
```