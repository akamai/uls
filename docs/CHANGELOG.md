# Version History

## v1.0.0
|||
|---|---|
|Date|2021-08-10
|Kind|Bugfix / Feature
|Author|mschiess@akamai.com, adrocho@akamai.com
- Minor improvements
  - EdgeRC file check (preflight) and "~" expansion to solve some common issues
  - fixed some typos in the "docker-compose" file
  - bumped EAA-CLI to version 0.4.2
  - simplified cli - command re-usage (visual parsing of subprocess cmd)
  - cleaned up the Dockerfile
  - added [Log_Overview](LOG_OVERVIEW.md) page to extend background on logged data


## v0.9.0
|||
|---|---|
|Date|2021-07-26-2021
|Kind|Bugfix / Feature
|Author|mschiess@akamai.com, adrocho@akamai.com
- Minor improvements 
  - fixed some typos / instructions
  - bumped EAA version to 0.4.1
  - bumped MFA version to 0.6.0
  - updated docker base image to python/3.9.6-slim-buster
  - Added API Credentials documentation
  - fixed a bug in rawcmd handling
  - Improved cli input error handling to leverage "restarting" towards docker
  - added FAQ documents
- Feature:
  - [FILTER (--filter) feature](ADDITIONAL_FEATURES.md#filter---filter-feature) introduced to reduce number of sent log lines towards SIEM
  

## v0.0.4
|||
|---|---|
|Date|2021-06-17
|Kind|Bugfix / Feature
|Author|mschiess@akamai.com
- Minor improvements 
  - Wait_time and wait_max shifted to config
  - added -f flag as alternative to --flag
  - fixed an exception that was introduced in v0.0.3
  - bumped MFA -CLI to 0.0.5 in dockerfile
  - added an additional debugging example
- Feature:
  - EAA CONNECTOR HEALTH (CONHEALTH) now available
  - Preflight (forced) check for available cli's

## v0.0.3
|||
|---|---|
|Date|2021-06-15
|Kind|Bugfix / Feature
|Author|mschiess@akamai.com <br> adrocho@akamai.com
- introduced line breaker variable for output
- fixed a bug in the "poll" handling
- fixed a bug that caused Popen PIPE to hang in certain circumstances
- bumped Dockerfile to newer CLI versions
- [introduced RAW output](ADDITIONAL_FEATURES.md#rawcmd---rawcmd-feature) (send data to stdout)

## v0.0.2
|||
|---|---|
|Date|2021-06-10
|Kind|Bugfix
|Author|mschiess@akamai.com <br> adrocho@akamai.com
- fixed monitoring output bug in docker-compose
- fixed bug in Dockerfile that prevented development builds
- fixed a bug in EAA CLI handler

## v0.0.1 (Initial Commit)
|version|v0.0.1|
|---|---|
|Date|2021-06-09
|Kind|Initial Commit
|Author|mschiess@akamai.com <br> adrocho@akamai.com
- INPUT: EAA, ETP, MFA (based on CLI's)
- OUTPUT: HTTP, TCP, UDP
- Docker & docker-compose examples
- Error & Reconnection handling
- Monitoring hook introduced Example:
- Kill Signal handling
- Configuration file `bin/config/global_config.py`
- Documentation & usage examples