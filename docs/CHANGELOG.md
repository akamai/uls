# Version History
## v1.7.2
|||
|---|---|
|Date|2023-XXXX
|Kind| MINOR release
|Author|mschiess@akamai.com
- **Minor improvements** 
  - Introduced **Secure Internet Access** (formerly ETP) as INPUT specification (as an alias to ETP)  
  - added "ETP NETCON" to the autoresume feature
  - prevented "EAA DIRHEALTH" to be mistakenly autoresumed
  - Imrpoved [log overview](LOG_OVERVIEW.md) readability
  - Added `--debugloglines` to allow control of input loglines being sent to the debug log
  - Added [Microsoft Sentinel SIA / ETP integration](SIEM/SENTINEL/Readme.md) documentation
  - Added a FAQ entry [regarding time synchronization](FAQ.md#error-invalid-timestamp-on-api-call)
- **BUGFIX**
  - Fixed a bug in the autoresume function that created a problem with timezones in certain circumstances

## v1.7.1
|||
|---|---|
|Date|2023-10-11
|Kind| BUGFIX release
|Author|mschiess@akamai.com
- **BUGFIX**
  - Fixed a bug in the ETP & EAA CLI that prevented ULS to run properly in docker environment
    - [docker] bumped CLI-EAA to "0.6.3"
    - [docker] bumped CLI-ETP version to "0.4.5"
- **Housekeeping**
  - Added additional automated testing to the docker release process

## v1.7.0
|||
|---|---|
|Date|2023-10-10
|Kind| FEATURE release
|Author|mschiess@akamai.com, androcho@akamai.com
- **Features**
  - Allowing the configuration of the HTTPFORMATTYPE, which controls the building of payloads for aggregated HTTP requests (click [here](FAQ.md#what-is-http-formattype) for additional information)
  - Allow adjustment of the "INPUT QUEUE SIZE" threshold (--inputqueuesize) in order to handle huge API pages and fast API output
  - New feed for EAA: Directory Health (dirhealth) to fetch health details for configured directories wihtin EAA 
- **Minor improvements**
  - Added additional checking in the auto installer
  - [docker] bumped python version to "3.12.0"
  - [docker] bumped GC-LOGS version to "0.0.2(beta)", now supporting credentials in ENV VARS
  - [docker] bumped CLI-EAA to "0.6.2"
  - [docker] bumped CLI-ETP version to "0.4.4" - fixed a bug in output ordering + empty response handling.
  - "get_uls.sh" now allows selection of OS package installation rather than pip3. [See](https://github.com/akamai/uls/issues/46) for more information
- **Housekeeping**
  - DocFix Readme.md (thx [@ihommani](https://github.com/akamai/uls/pull/47))
  - Increased default input_queue_size from 10000 to 15000 to avoid race conditions when an API is answering very fast


## v1.6.6
|||
|---|---|
|Date|2023-08-23
|Kind| Minor release
|Author|mschiess@akamai.com, androcho@akamai.com
- **Features**
  - Added '--httpliveness' to disable HTTP(S) OPTIONS request for liveness checking
  - Added new feed for ETP: Network traffic connections details (netcon) [Requires CLI-ETP >= 0.4.2]
- **Minor improvements**
  - DOC Fix for manual CLI installation
  - [docker] bumped CLI-EAA version to "0.5.9"
  - [docker] bumped CLI-ETP version to "0.4.2"
- **Housekeeping**
  - Updated the ETP Links from developer.akamai.com to techdocs.akamai.com
  - Added "docker file liniting" into test scripts
  
## v1.6.5
|||
|---|---|
|Date|2023-07-28
|Kind| Minor release
|Author|mschiess@akamai.com
- **Minor improvements**
  - Allow manipulation of the [TCP & UDP output format](ARGUMENTS_ENV_VARS.md#list-of-parameters--environmental-variables) (--tcpudpformat / ULS_TCPUDP_FORMAT).
  - [docker] bumped source image to 3.11.4-slim-bookworm (new debian release)

## v1.6.4
|||
|---|---|
|Date|2023-05-02
|Kind| Minor release
|Author|mschiess@akamai.com
- **Minor improvements**
  - Updated docs to clarify the required timestamp format (undefined --> epoch time in seconds)
  - [docker] bumped CLI-EAA version to "0.5.7"
  - [docker] bumped python version to 3.11.3
  - [docker] bumped CLI-GC version to "v0.0.1(beta)"
  - [docker] bumped CLI-MFA version to 0.1.1
- **Bugfix**
  - `--endtime <value>` didn't cause ULS to eventually stop ops. This is now fixed.
  - improved container detection (only cosmetic improvement)

## v1.6.3

|||
|---|---|
|Date|2022-11-29
|Kind| Minor release
|Author|mschiess@akamai.com

- **Minor improvements**
  - Introduced '--httpaggregate' / 'ULS_HTTP_AGGREGATE' option to allow easier management of the HTTP(S) aggregation function 
  - fixed concatenation issue on HTTP (multi-event bundle)
  - [docker] bumped CLI-ETP version to 0.4.0 (future api support fix)
  - [docker] bumped python version to 3.11.0
  - fixed a bug in the "file output handler" - reported in [issue#35](https://github.com/akamai/uls/issues/35)
  - fixed a bug in the "get_uls.sh" script which stated the wrong error message when pip was not found
  - minor fix to properly detect "podman" as docker alternative
  - Amendend installation steps for Guardicore and Linode log-fetcher(s)

## v1.6.2

|||
|---|---|
|Date|2022-10
|Kind| Minor release
|Author|mschiess@akamai.com

- **Minor improvements**
  - Bumped EAA CLI to version 0.5.1 (additional SIEM fields - EAA release 2022.02)
  - Amended FAQ to [handle self-signed certificates alongside Guardicore](./FAQ.md#uls-throws-tls-an-error-when-connecting-towards-guardicore-api---input-gc)
  - Added installation ID ("random string" + "current date YMD" + "first installed version") to support debugging process
  - fixed a bug in the Dockerfile that left uls/var unusable
- **Housekeeping**
  - fixed some bugs in testing (false negative) & speeded up testing process

## v1.6.1

|||
|---|---|
|Date|2022-10
|Kind| BUGFIX release
|Author|mschiess@akamai.com

- **Minor improvements** 
  - Dropped CLI installation verification for CLI's not used by ULS
- **Housekeeping**
  - Added parallel testing processes to speed up testing (see [Testing Readme](../test/README.md))
  - added randomization tokens for "mocked" edgerc file (to avoid race condition in prallel testing)


## v1.6.0

|||
|---|---|
|Date|2022-09
|Kind| FEATURE release
|Author|mschiess@akamai.com
- **Features**
  - Support for Akamai Guardicore Segmentation (experimental)
    - Available feeds: netlog, incident, agent, system  
      Please ensure to [update your .edgerc](./AKAMAI_API_CREDENTIALS.md#guardicore-api-integration) file for GC usage
  - Support for Akamai Linode Cloud (experimental)
    - Available feed: audit  
      Please ensure to [update your .edgerc](AKAMAI_API_CREDENTIALS.md#linode-api-credentials) file for LINODE usage

- **Minor improvements** 
  - ULS [Install Script](COMMAND_LINE_USAGE.md#automated-installation) allows fully working ULS installation via a single script
  - ULS [Updater](COMMAND_LINE_USAGE.md#automated-update) helps to maintain a proper updated version of ULS + Modules
  - Amended [Command Line Usage](COMMAND_LINE_USAGE.md) documentation on how to use the installer / updater
  - bumped python container (docker) to version 3.10.7
  - bumped ETP-CLI version to 0.3.9 which should massively reduce the fetch lag
  - Added [documentation](./HIGH_AVAILABILITY.md) to explain high availability options for ULS


## v1.5.1

|||
|---|---|
|Date|2022-08
|Kind| BUGFIX release
|Author|androcho@akamai.com

- **Bugfix**
  - Use cli-eaa version 0.5.0.2 fixing a timezone issue on the EAA ADMIN feed


## v1.5.0

|||
|---|---|
|Date|2022-07
|Kind| FEATURE release
|Author|mschiess@akamai.com, androcho@akamai.com

- **Performance improvements**
  - Rework to handle large number of events (100k+ per minute) and fail safe 
    when the Output can't cope with the pace of incoming events.
  - New parameters in `bin/config/global_config.py`:
    - If your output is slower than incoming events, 
      ULS can buffer `input_queue_size` events. If buffer gets full, ULS will stop with an error message.
    - HTTP output can now aggregate messages, two options:
      - `output_http_aggregate_count`
      - `output_http_aggregate_idle` 
- **Minor improvements**  
  - new attributes in monitoring output:
    - `event_ingested_interval` # events read from CLI input
    - `event_bytes_interval` # total size in bytes processed
- **Housekeeping**
  - Documented missing dependencies in [test/README.md](../test/README.md)


## v1.4.0
|||
|---|---|
|Date|2022-05-20
|Kind| FEATURE release
|Author|mschiess@akamai.com, androcho@akamai.com

- **Features**
  - Device Inventory (DEVINV) feed added for EAA (requires eaa-cli >= 0.4.9.1)

- **Minor improvements**
  - bumped EAA to version v0.5.0
  - bumped ETP to version v0.3.8
  - bumped python to version 3.10.4-slim-bullseye
  
- **Bugfix**
  - Fixed a bug in the test scripts to support real `.edgerc`

## v1.3.5
|||
|---|---|
|Date|2022-04-05
|Kind| Bugfix release
|Author|mschiess@akamai.com, androcho@akamai.com
- **Minor improvements**
  - More QRADAR log source type definitions (thx to bitonio)
  - Added docker-compose ETP - Tenant example

## v1.3.4
|||
|---|---|
|Date|2022-03-08
|Kind| Bugfix release
|Author|mschiess@akamai.comm androcho@akamai.com
- **Minor improvements**
  - Added QRADAR log source type definitions (thx to bitonio)
  - Added SUMO Logic (thx to huskar20 for the contribution)
  - bumped CLI-MFA to v0.0.9
  - added resources, nodeSelector, tolerations and affinity to the helm values.yaml / template


## v1.3.3
|||
|---|---|
|Date|2022-02-28
|Kind| Bugfix release
|Author|mschiess@akamai.com
- **Bugfix**
  - Adopted to new MFA CLI Version (only single feed "EVENT" available anymore)
  - Amended new dates to the file headers
  - Added volume to dockerfile as data storage for "autoresume"


## v1.3.2
|||
|---|---|
|Date|2022-02-10
|Kind| Bugfix release
|Author|mschiess@akamai.com
- **Features**
  - Kubernetes deployment example / Helm charts added ([start here](KUBERNETES_USAGE.md))  
  

- **Minor improvements**
  - Bumped ETP-CLI to version 0.3.7 in Dockerfile
  - Bumped EAA-CLI version to 0.4.6 in Dockerfile  
  

- **Bugfixes**
  - fixed issue when using file handler and rotation at "midnight" - running back in time for 30 days
  - added a sanity (dictionary) check for "--httpauthheader"
  - fixed a bug in http reconnecting forever in certain circumstances
  - added a sanity check for "HTTP_OUT_FORMAT" to avoid issues with the ´%s´ seclector
  - removed forced http authentication token "--httpauthheader" (allow None)
  - discovered a bug in configparser -> [see FAQ entry](FAQ.md#uls-does-not-start-due-to-missing-field-in-config)


## v1.3.1
|||
|---|---|
|Date|2021-12-20
|Kind| Bugfix release
|Author|mschiess@akamai.com
- **Bugfixes**
  - fixed a checkpoint issue when using ETP / THREAD 
  - some doc fixes

## v1.3.0
|||
|---|---|
|Date|2021-12-17
|Kind| Feature & Bugfix release
|Author|mschiess@akamai.com
- **Features**
  - [internal] Added automated test scripts to improve continuous release quality
  - [AUTO-RESUME feature](ADDITIONAL_FEATURES.md#autoresume--resume) enables ULS to automatically continue operation starting from the last saved checkpoint.
  - [FileAction support](ADDITIONAL_FEATURES.md#post-processing-of-files-fileoutput-only) to trigger custom scripts upon file rotation event.


- **Minor improvements**
  - Bumped ETP-CLI to version 0.3.6 in Dockerfile
  - Bumped EAA-CLI version to 0.4.5 in Dockerfile
  - Added additional fields to the monitoring output ([uls_version, event_count_interval](MONITORING.md))


- **Bugfixes**
  - removed hard requirement to run ULS via bin/uls.py - can now be run from everywhere 
  - introduced HTTP Timeout (for HTTP OUTPUT) to the configuration file (http stream did not issue proper error messages in some cases)
  - Fixed an output issue on "CLI failure", added configureable output handling to the config
  - replaced pip with pip3 in CLI usage docs
  - Fixed a windows bug (bypass blocking on windows) + added a [FAQ entry on how fix a installation specific bug](FAQ.md#uls-on-windows-error-winerror-2-the-system-cannot-find-the-file-specified)


## v1.2.0
|||
|---|---|
|Date|2021-11-02
|Kind| Feature & Bugfix release
|Author|mschiess@akamai.com, androcho@akamai.com
- **Features**
  - [Transformation Support for output format transformation ](TRANSFORMATIONS.md)(additional log formats and integrations) introduced
  - [MCAS transformation](TRANSFORMATIONS.md#microsoft-cloud-application-security-mcas): Microsoft Cloud Application Security
  - [JMESPATH transformation](TRANSFORMATIONS.md#jmespath): Create your own pattern / filter / searches
  - added [--starttime ](ARGUMENTS_ENV_VARS.md#input)to tell ULS where to start scratching the logs (EPOCH time required)
  - added [--endtime](ARGUMENTS_ENV_VARS.md#input) to allow cherry-picking of a specific time-slice (EPOCH time required)
  - added [FILE OUTPUT ](OUTPUTS.md#file)support (writes log streams to a file to the local filesystem)
- **Bugfix**
  - Fixed a bug in proxy handling (using cli param), re-enabled CLI cmd and amended docs
  - Fixed a bug that prevented "--version" to work properly
  - Fixed a bug that mitigates version display bug on the CLI (solves the symptom only)
  - Fixed a bug that potentially allowed buffered output from the CLI's (CLI calls and DOCKERFILE)
- **Minor improvements**
  - updated base container to "python:3.10-slim-bullseye"  ****
  - Introduced "systemd" example to [Command Line Usage docs](COMMAND_LINE_USAGE.md#uls-as-a-service-systemd)
  - Introduced docker check to version check and amendment to UA Header
  - Introduced - Message re-transmission on network error
  - ReFactored INPUT / OUTPUT handler to reduce compute & memory footprint
  - bumped EAA CLI Version to 0.4.4 (docker only)
  - Introduced dedicated ["OUTPUT" documentation](OUTPUTS.md)
  - introduced uls own requirements.txt in the [bin directory](../bin/requirements.txt) - still trying to keep req's as low as possible. 
  
## v1.1.0
|||
|---|---|
|Date|2021-08-18
|Kind|Bugfix / Feature
|Author|mschiess@akamai.com
- **Features**
  - Added **DNS** and **PROXY** feeds to ETP Input (<3 Sara)
- **Minor improvements**
  - Version number fix (Stated 0.9.0 instead of 1.x.x)
  - debug "message" fix ( changed HTTP to HTTP(S) to avoid misunderstanding)
  - documented workaround for discovered proxy issue
  - enabled json highlighting in [Log_overview](./LOG_OVERVIEW.md)
  - added better error guidance when basic stuff is unset (input / output)
  - moved docker-compose from root dir to /docs
  - added `read_only: true` to the docker-compose.yml files (security enhancement)

## v1.0.0
|||
|---|---|
|Date|2021-08-10
|Kind|Bugfix / Feature
|Author|mschiess@akamai.com, androcho@akamai.com
- **Minor improvements**
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
|Author|mschiess@akamai.com, androcho@akamai.com
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
|Author|mschiess@akamai.com <br> androcho@akamai.com
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
|Author|mschiess@akamai.com <br> androcho@akamai.com
- fixed monitoring output bug in docker-compose
- fixed bug in Dockerfile that prevented development builds
- fixed a bug in EAA CLI handler

## v0.0.1 (Initial Commit)
|version|v0.0.1|
|---|---|
|Date|2021-06-09
|Kind|Initial Commit
|Author|mschiess@akamai.com <br> androcho@akamai.com
- INPUT: EAA, ETP, MFA (based on CLI's)
- OUTPUT: HTTP, TCP, UDP
- Docker & docker-compose examples
- Error & Reconnection handling
- Monitoring hook introduced Example:
- Kill Signal handling
- Configuration file `bin/config/global_config.py`
- Documentation & usage examples