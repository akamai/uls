# IBM QRadar<!-- omit in toc -->

## Table of contents<!-- omit in toc -->

- [Inputs](#inputs)
  - [EAA feeds](#eaa-feeds)
- [ULS output configuration](#uls-output-configuration)

This document describes how to configure [IBM QRadar](https://www.ibm.com/security/security-intelligence/qradar) in order to receive data from ULS.

The recommended way (in order to minimize network/encryption overhead) is the TCP (Syslog) connector.

Each feed has a corresponding definition file (zip). Use QRadar Extension Management to import it into your QRadar environment.

## Inputs

### EAA feeds

The following QRadar DSM version 1.1.1 is able to parse the 3 different EAA feeds coming from a single source (same host running ULS).

> Download [EAA Combined feeds QRadar DSM version 1.1.1](akamai-eaa-combined-dsm-v.1.1.1.zip)

Last update: March 28th, 2022

## ULS output configuration

Please follow the [QRADAR documentation](https://www.ibm.com/docs/en/dsm?topic=options-http-receiver-protocol-configuration).
