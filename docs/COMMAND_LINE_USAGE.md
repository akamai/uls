# ULS Command Line Usage

This document describes the "command line usage" of the ULS software.  
All commands referenced in this document are run from the repositories root level.

### Table of contents

- [ULS Command Line Usage](#uls-command-line-usage)
    - [Overview](#overview)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Clone ULS Repo](#clone-uls-repo)
    - [Enterprise Access CLI's](#enterprise-access-clis)
    - [Setup the .EDGERC File](#setup-the-edgerc-file)
    - [Setup the .EDGERC File](#setup-the-edgerc-file-1)
  - [Usage](#usage)
    - [Usage examples](#usage-examples)
  - [ULS as a service: systemd](#uls-as-a-service-systemd)

## Requirements
To run the operations within the following documentation, you need to have the following tools installed:
- git
- python >= 3.9 (including pip)
- Akamai API credentials file - `.edgerc` (see [API Credentials](AKAMAI_API_CREDENTIALS.md) for creation instructions)
- Understanding of available [ULS CLI PARAMETERS](ARGUMENTS_ENV_VARS.md)
- Access to `github.com`, `pypi.org`, `pythonhosted.org` and `pypi.python.org` within your firewall

## Installation
### Clone ULS Repo
Clone the ULS repository from github, change into the ULS repository directory afterwards and install requirements.
```bash
git clone https://github.com/akamai/uls.git
cd uls
pip3 install -r bin/requirements.txt
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
pip3 install -r ext/cli-etp/requirements.txt

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

## ULS as a service: systemd

If you are planning to use multiple Akamai feed with ULS, bear in mind you will need to repeat the instruction below multiple times. We built this guide with CentOS 7.

We assume you have followed the instruction above to install ULS as command line.
Before you install the service, make sure it works manually with the configured user.

Create a new file in systemd directory (e.g. `/etc/systemd/system`), use a name that is easy to remember, like `uls-etp-dns.service`

```INI
# ULS as systemd service example
# uls-etp-dns.service

[Unit]
Description=Akamai ULS feed ETP/DNS  # << Adjust the description with the feed name
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=uls  # << Change this to reflect the user on your system 
WorkingDirectory=/usr/local/uls  # << Change with ULS location
ExecStart=/usr/bin/python3 /usr/local/uls/bin/uls.py --input etp --feed dns --output tcp --host 127.0.0.1 --port 9090  # << Adjust python path and uls path

[Install]
WantedBy=multi-user.target
```

Test the service with the following command:
```
$ systemctl start uls-etp-dns
```

Make sure everything is working:

```
$ systemctl status uls-etp-dns
```

Expected output:

```
● uls-etp-dns.service - Akamai ULS feed ETP/DNS
   Loaded: loaded (/etc/systemd/system/uls-etp-dns.service; disabled; vendor preset: disabled)
   Active: active (running) since Wed 2021-09-01 23:51:39 UTC; 4s ago
 Main PID: 9428 (python3)
   CGroup: /system.slice/uls-etp-dns.service
           ├─9428 /usr/bin/python3 /root/uls/bin/uls.py --input etp --feed dns --output tcp --host 127.0.0.1 --port 9090
           └─9430 python3 ext/cli-etp/bin/akamai-etp --edgerc /root/.edgerc --section default --user-agent-prefix ULS/1.1.0_ETP-DNS event dns -f
```

To make sure the service will start if the machine restarts, use:

```
$ systemctl enable uls-etp-dns
```

You might need to adjust some settings until you get what you need. Keep in mind to notify systemd you change the .service file using

```
$ systemctl daemon-reload
```

For more information on systemd, see man help `man systemd.exec`