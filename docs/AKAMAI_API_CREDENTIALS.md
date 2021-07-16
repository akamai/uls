# Akamai API credentials for ULS

This document describes how to create Akamai API credentials and configure them in ULS to access the different products and data feeds.

### Table of contents

- [Akamai API credentials for ULS](#akamai-api-credentials-for-uls)
    - [Table of contents](#table-of-contents)
  - [Feeds / API overview](#feeds--api-overview)
  - [Setting up API credentials for ULS](#setting-up-api-credentials-for-uls)
    - [Enterprise Application Access (EAA)](#enterprise-application-access-eaa)
      - [EAA Legacy API (for Access and Admin Audit feeds)](#eaa-legacy-api-for-access-and-admin-audit-feeds)
      - [EAA {OPEN} API (for Connector Health feed)](#eaa-open-api-for-connector-health-feed)
    - [Enterprise Threat Protector (ETP)](#enterprise-threat-protector-etp)
      - [ETP {OPEN} API Reporting](#etp-open-api-reporting)
    - [Akamai MFA](#akamai-mfa)
      - [MFA Integration for logging](#mfa-integration-for-logging)
  - [.edgerc file](#edgerc-file)
    - [Advanced .edgerc Usage](#advanced-edgerc-usage)
      - [Multiple customer contracts](#multiple-customer-contracts)
      - [Partner & employee enhancement](#partner--employee-enhancement)
      - [ETP API EVENT Filters](#etp-api-event-filters)

## Feeds / API overview

|Product long name|Acronym|Feed|API|
|---|---|---|---|
|Enterprise Application Access|EAA|ACCESS|[EAA Legacy API](#eaa-legacy-api-for-access-and-admin-audit-feeds)|
|Enterprise Application Access|EAA|ADMIN|[EAA Legacy API](#eaa-legacy-api-for-access-and-admin-audit-feeds)|
|Enterprise Application Access|EAA|HEALTH|[{OPEN} API / Enterprise Application Access](#eaa-open-api-for-connector-health-feed)|
|Enterprise Threat Protector|ETP|THREAT|[{OPEN} API / ETP Report](#etp-open-api-reporting)|
|Enterprise Threat Protector|ETP|AUP|[{OPEN} API / ETP Report](#etp-open-api-reporting)|
|Akamai MFA|MFA|AUTH|[MFA Integration](#mfa-integration-for-logging)|
|Akamai MFA|MFA|POLCIY|[MFA Integration](#mfa-integration-for-logging)|

## Setting up API credentials for ULS

ULS will read the API credentials from a text file, by default named `.edgerc` in the home directory of the current user. The credentials configuration file can have multiple sections allowing to use multiple tenants (in case of multi-contract structure, or Akamai Partner).

### Enterprise Application Access (EAA) 

#### EAA Legacy API (for Access and Admin Audit feeds)

To create **EAA Legacy API** credentials, connect to [Akamai Control Center](https://control.akamai.com)

- Select **Enterprise Center** from the main navigation menu on the left
- Navigate to **General Settings** > **Settings**
- Select the **API Keys** tab
- Click **Generate new API Key** top right button
- Enter a name and a description
- On the confirmation screen, copy the **Key** and the **Secret**
![img.png](images/uls_apicreds_eaa_ec.png)
- Add/replace/amend the following section to your `.edgerc` file and replace the data accordingly, example in the default section:
  
```INI
[default]
; API credentials for EAA access and admin logs
eaa_api_host = manage.akamai-access.com
eaa_api_key = XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXX
eaa_api_secret = XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXX
```

#### EAA {OPEN} API (for Connector Health feed)

To create **Akamai {OPEN} API** credentials, please follow [these instructions](https://developer.akamai.com/legacy/introduction/Prov_Creds.html).

Make sure the API user has **READ-WRITE** permission on the **Enterprise Application Access** API. For ULS usage, it is safe to provide all required API permission (such as EAA, ETP) to a single API user. We do not recommend All APIs.

![img.png](images/uls_apicreds_eaa_openapi.png)

Please add/replace/amend the following section to your `.edgerc` file and replace the data accordingly, example in the default section:

```INI
[default]
; Akamai {OPEN} API credentials
host = akaa-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx.luna.akamaiapis.net
client_token = akab-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx
client_secret = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
access_token = akab-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx
```

### Enterprise Threat Protector (ETP)

#### ETP {OPEN} API Reporting

To create **AKAMAI {OPEN} API** credentials, please follow [these instructions](https://developer.akamai.com/legacy/introduction/Prov_Creds.html).

Make sure the API user has **READ-WRITE** permission to the **etp-config** API
For ULS usage, it is safe to provide all required roles (such as EAA, ETP) to a single api user.

For ETP usage, an additional config value (**etp_config_id**) is required.
The `etp_config_id` value can be obtained as follows:
- Connect to [Akamai Control Center](https://control.akamai.com)
- Select **Enterprise Center**
- Select **Locations** > **Locations** (or any other ETP specific page)
- Check out the URL bar of your browser, locate your **ETP configuration identifier** between `/etp/` and `/location/`:
![img.png](images/uls_apicreds_etp_customerid.png)

Please add/replace/amend the following section to your `.edgerc` file and replace the data accordingly:
```INI
[default]
; Akamai {OPEN} API credentials
host = akaa-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx.luna.akamaiapis.net
client_token = akab-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx
client_secret = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
access_token = akab-xxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxx

; ETP Config ID (required for ETP usage, can be obtained from the Akamai Web Interface)
etp_config_id = your-ETP-config-ID
```

### Akamai MFA

#### MFA Integration for logging

To create **MFA Integration** credentials, connect to [Akamai Control Center](https://control.akamai.com).

- Select **Enterprise Center** from the main navigation menu on the left
- Navigate to **MFA** > **Integrations**
- Click on (+) to add a new integration
    <img src="images/uls_apicreds_mfa_create.png" width="500px" />
- Confirm by clicking the **Save & Deploy** button
- **Copy** the credentials as shown below:
    <img src="images/uls_apicreds_mfa_creds.png"  width="500px" />
- Add/replace/amend the following section to your `.edgerc` file and replace the data accordingly:

```INI
[default]
; Akamai MFA logging integration credentials
mfa_integration_id = app_xxxxxxxxxxxxxxxxxxxxx
mfa_signing_key = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## .edgerc file

The `.edgerc` file hosts all relevant credentials required by ULS (and underlying CLI's). Some basic information around `.edgerc` can be found [here](https://developer.akamai.com/legacy/introduction/Conf_Client.html).
This repo also provides a [.edgerc sample file](examples/.edgerc-sample) with all config sections added and explained.
Feel free to use the file as a template and comment out the sections not needed with `;`. 

### Advanced .edgerc Usage 

#### Multiple customer contracts

If your organization has multiple contracts, please add the following "contract_id" line to your `.edgerc` file in order select the proper contract.  
If ETP and EAA are on different contracts, we recommend the creation of two different `.edgerc` files.

```INI
[default]
; If your organization have multiple contracts with EAA service
; please add it below. Contact your Akamai representative to obtain it
contract_id = A-B-1CD2E34
```

#### Partner & employee enhancement

For Partners or AKAMAI employees please add the "extra_qs" line to your `.edgerc` file in order to switch towards the desired tenant. Please replace "TENANT-SWITCH-KEY" with the provided switch key.

```INI
[default]
; If you are a partner managing multiple customers, you can use the switchkey
; For more information, see:
; https://learn.akamai.com/en-us/learn_akamai/getting_started_with_akamai_developers/developer_tools/accountSwitch.html
extra_qs = accountSwitchKey=TENANT-SWITCH-KEY
```

#### ETP API EVENT Filters

For Enterprise Threat protector (ETP), events can already be filtered at API level, so they won't even be transferred towards ULS.
This can be used for performance / scaling as well for cost saving reasons.
Please find more information around filtering on ETP API in the [ETP APIv3 documentation](https://developer.akamai.com/api/enterprise_security/enterprise_threat_protector_reporting/v3.html#filter)

```INI
[default]
etp_event_filters = {"list":{"nin":["12345"]}}
```