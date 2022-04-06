# ULS DOCKER ETP-TENANT EXAMPLES

Enterprise Threat Protector (ETP) allows customers and partners to manage multiple ETP tenants each coming with separated data feeds.

See [Akamai ETP multi-tenancy documentation](https://techdocs.akamai.com/etp/docs/delegated-tenant-access#multi-tenancy) for more details.

ULS can be configured to be a data hub to fetch and distribute these feeds from multiple tenants into one or multiple destinations.

This directory contains configuration examples (for simple copy & paste usage) that illustrate ETP multi-tenant feature.

## docker-compose.yml

[This file](docker-compose.yml) contains examples for 2 different ETP tenants collecting the same "threat" feed.

## ENV files
The files contains all available ENV VARS explained in a single file.  
Tenant 1 [etp-threat-tenant-1.env](./etp-threat-tenant-1.env)  
Tenant 2 [etp-threat-tenant-2.env](./etp-threat-tenant-2.env)

## EDGERC example

This is a sample `.edgerc` file explaining the ["ETP Multi Tenant support"](./.edgerc-example)