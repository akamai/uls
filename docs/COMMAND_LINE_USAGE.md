# ULS Command Line Usage
This document describes the "command line usage" of the ULS software.  
All commands referenced in this document are run from the repositories root level.


### Overview
- [ULS Command Line Usage](#uls-command-line-usage)
    - [Overview](#overview)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Enterprise Access CLI's](#enterprise-access-clis)
    - [Setup the edgerc file](#setup-the-edgerc-file)
  - [Usage](#usage)
    - [Usage examples](#usage-examples)

## Requirements
To run the operations within the following documentation, you need to have the following tools installed:
- git
- python >= 3.9 (including pip)
- Akamai API credentials file - `.edgerc` (see [API Credentials](AKAMAI_API_CREDENTIALS.md) for creation instructions)
- Understanding of available [ULS CLI PARAMETERS](ARGUMENTS_ENV_VARS.md)
- Access to `github.com`, `pypi.org`, `pythonhosted.org` and `pypi.python.org` within your firewall

## Installation
### Clone ULS Repo
Clone the ULS repository from github and change into the repository directory aferwards.
```bash
git clone https://github.com/akamai/uls.git
cd uls
```

### Enterprise Access CLI's
The Secure Enterprise Access Products CLI Tools need to be installed into the `ext` directory within this repo.
Please run the following commands to download the CLI tools and install the requirements.
```bash
# Enterprise Application Access (EAA)
git clone --depth 1 --single-branch https://github.com/akamai/cli-eaa.git ext/cli-eaa && \
pip3 install -r ext/cli-eaa/requirements.txt

# Enterprise Threat Protector (ETP)
git clone --depth 1 --single-branch https://github.com/akamai/cli-etp.git ext/cli-etp && \
pip install -r ext/cli-etp/requirements.txt

# Akamai Phish Proof Multi Factor Authenticator (AKAMAI-MFA)
git clone --depth 1 --single-branch https://github.com/akamai/cli-mfa.git ext/cli-mfa && \
pip3 install -r ext/cli-mfa/requirements.txt
```

### Setup the .EDGERC File
Copy the `.edgerc` file ([instructions for creation](AKAMAI_API_CREDENTIALS.md)) to your users home directory (~):
```bash
cp /path/to/your/.edgerc ~/.edgerc
```
### Setup the .EDGERC File
Copy the `.edgerc` file ([instructions for creation](AKAMAI_API_CREDENTIALS.md)) to your users home directory (~):
```bash
cp /path/to/your/.edgerc ~/.edgerc
```

## Usage
The command line interface is split into 3 different sections:
- Global commands (i.e. --loglevel debug)
- Input configuration (i.e. --input eaa)
- Output configuration (i.e. --output tcp)

A full list of options/parameters can be printed by typing
```bash
python3 bin/uls.py --help
```

Starting ULS on the command line, ULS will run in foreground and literally run forever (unless terminated).  
As a docker/container usage is recommended, ULS does not bring any threading/daemon support right now.
All log output will be directed to STDOUT by default.

### Usage examples
- EAA ADMIN LOG ==> TCP LISTENER
    ```bash
    python3 bin/uls.py --input eaa --feed admin --output tcp --host 10.10.10.200 --port 9090
    ```

- ETP THREAT LOG ==> UDP LISTENER
    ```bash
    python3 bin/uls.py --input etp --feed threat --output udp --host 10.10.10.200 --port 9090
    ```
- MFA AUTH LOG ==> HTTP LISTENER (SPLUNK) 
  disabled TLS verification
  ```bash
   python3 bin/uls.py --input=MFA --feed auth --output HTTP --httpformat '{"event": %s}' --httpauthheader '{"Authorization": "Splunk xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"}' --httpurl "https://127.0.0.1:9091/services/collector/event" --httpinsecure
  ```

- Logging to a file and sending process to the background
    ```bash
    python3 bin/uls.py --input etp --feed threat --output udp --host 10.10.10.200 --port 9090 &> /path/to/my/logfile &
    ```
  Rather consider [docker usage](./DOCKER_USAGE.md) instead of this
  