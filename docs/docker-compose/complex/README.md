# ULS Complex Example

This example provides a real world usage example for ULS within a `docker compose` setup.
It combines three different AKAMAI Secure Enterprise Access feeds.
All docker related controls can be found in [docker-compose.yml](docker-compose.yml)

## EAA-ACCESS
|IN|OUT|FILE|
|---|---|---|
|EAA-ACCESS|TCP|[eaa-access.env](eaa-access.env)|

## ETP-THREAT
|IN|OUT|FILE|
|---|---|---|
|ETP-THREAT|HTTP|[etp-threat.env](etp-threat.env)|

## MFA-AUTH
|IN|OUT|FILE|
|---|---|---|
|MFA-AUTH|UDP|[mfa-auth.env](mfa-auth.env)|




