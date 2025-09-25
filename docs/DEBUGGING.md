# ULS Troubleshooting and debugging

This document describes how to troubleshoot and debug Unified Log Streamer software.  

Please make sure you follow the steps before filing an issue on the [GitHub Issues Page](https://github.com/akamai/uls/issues), collecting these information increase our chance to understand the issue, and shorten the time to provide you support.

## Make sure you're using the latest version

We strive at fixing issues as they arise and add new features, with new version coming throughout the months.

We strongly encourage to always get the latest version of ULS. You can find the latest version in the [release page](https://github.com/akamai/uls/releases). See also [ULS updater script documentation](COMMAND_LINE_USAGE.md#automated-update).

## Table of contents

- [ULS Troubleshooting and debugging](#uls-troubleshooting-and-debugging)
  - [Make sure you're using the latest version](#make-sure-youre-using-the-latest-version)
  - [Table of contents](#table-of-contents)
  - [Version information](#version-information)
    - [Commands to trigger version output](#commands-to-trigger-version-output)
      - [Command line](#command-line)
      - [Docker](#docker)
    - [Example Output](#example-output)
  - [Tell us what you're trying to do](#tell-us-what-youre-trying-to-do)
  - [Debug output from ULS](#debug-output-from-uls)
    - [Commands to trigger debug output](#commands-to-trigger-debug-output)
      - [Command Line](#command-line-1)
      - [Docker](#docker-1)
  - [Debug output from CLI's](#debug-output-from-clis)
    - [Steps to get CLI Debug output](#steps-to-get-cli-debug-output)
      - [CLIDEBUG mode](#clidebug-mode)
      - [manual CLI debugging](#manual-cli-debugging)
      - [DOCKER / DOCKER-COMPOSE](#docker--docker-compose)

---

---

## Version information

Providing information about relevant module & software versions can help identify issues.

### Commands to trigger version output

#### Command line

```bash
python3 bin/uls.py --version
```

#### Docker

```bash
docker run -ti --mount type=bind,source="/path/to/your/.edgerc",target="/opt/akamai-uls/.edgerc",readonly --rm akamai/uls -v 
```

### Example Output

```text
Akamai Unified Log Streamer Version information
ULS Version             0.0.1

EAA Version             0.3.8
SIA/ETP Version         0.3.4
MFA Version             0.0.4

OS Plattform            Linux-5.10.25-linuxkit-x86_64-with-glibc2.28
OS Version              5.10.25-linuxkit
Python Version          3.9.5
```

---

## Tell us what you're trying to do
When raising a ticket or a bug, please make sure, you include the command (input, feed, output config) of what you were originally trying to do.  
This helps us diving into the correct sections of the code.  

When providing the data, please make sure, you're not leaking any sensitive data such as credentials, usernames or PII.

---

## Debug output from ULS

To debug problems into depth, ULS provides an extremely verbose output about every step processed within ULS.

### Commands to trigger debug output
#### Command Line

```bash
python3 bin/uls.py --loglevel debug <rest of your ULS command>
```

#### Docker

```bash
docker run -ti \
  --mount type=bind,source="/path/to/your/.edgerc",target="/opt/akamai-uls/.edgerc",readonly \
  --rm \
  --name uls_debugging \
  akamai/uls --loglevel debug <rest of your ULS command parameters> 
```

Instead of adding it to the command line, you can also set the `ULS_LOGLEVEL` ENV VAR to "DEBUG"

---

## Debug output from CLI's

This is helpful when a deeper debugging from within the CLI tool is required.  

### Steps to get CLI Debug output

#### CLIDEBUG mode
In ULS 1.9.0, a new feature `--clidebug` was introduced to simplify debugging.  
The `--clidebug` option will only work alongside the "RAW" output.  
This is to prevent sending of any sensitive data outside of the "ULS instance".  

How to use the `--clidebug` flag (Example on GuardiCore):
```shell
# This will print loglines AND the CLI debug output
python3 bin/uls.py --input gc --feed netlog --output raw --clidebug

# This will print the loglines, the CLI debug output and ULS debug output
python3 bin/uls.py --input gc --feed netlog --output raw --clidebug --loglevel debug
```


#### manual CLI debugging

 1) Run the desired stream in [ULS DEBUG mode](#debug-output-from-uls) and grab the command output i.e.
    ```bash
     ULS D UlsInputCli - CLI Command:  ['python3', 'ext/cli-eaa/bin/akamai-eaa', '--edgerc', '~/.edgerc', '--section', 'akamaidemo', '--user-agent-prefix', 'ULS/0.0.3_EAA-CONHEALTH', 'connector', 'list', '--perf', '--tail', '--json']
    ```
 2) Use the output to draft an RAWCMD and run it with the --rawcmd flag
    ```bash
    python3.9 bin/uls.py --rawcmd "--edgerc ~/.edgerc --section akamaidemo connector list --perf --tail --json" --output raw
    ```
    Feel free to omit the "--user-agent-prefix" flag
    To get a more detailed output, you can add the CLI debugging flag `-d`
    ```bash
    python3.9 bin/uls.py --rawcmd "-d --edgerc ~/.edgerc --section akamaidemo connector list --perf --tail --json" --output raw --loglevel debug
    ```
    Via this way, you can get the full CLI debugging output within ULS

#### DOCKER / DOCKER-COMPOSE

1) Start a debugging docker instance and connect to it's console
   ```bash
   docker run -ti \
     --mount type=bind,source="/path/to/your/.edgerc",target="/opt/akamai-uls/.edgerc",readonly \
     --entrypoint "/bin/bash" \
     --name uls_debugging \
     --rm akamai/uls:latest
   ```

2) Run CLI directly within the container  
    Example:
    ```bash
     ext/cli-eaa/bin/akamai-eaa -d --edgerc ~/.edgerc --section akamaidemo connector list --perf --tail --json
    ```
    This will debug the exact same thing as above, but without passing the data through ULS (and eventually your SIEM)  
    As alternative you also can run the above command omn the CLI directly ;) 

---
