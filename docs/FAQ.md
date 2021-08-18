# Frequently asked questions (FAQ)

## Contents
- [How can the ULS process be monitored ?](#how-can-the-uls-process-be-monitored-)  
- [Which SIEM are supported ?](#which-siem-are-supported-)
- [Where to get the API credentials ?](#where-to-get-the-api-credentials-)
- [What command line Options are available ? ](#what-command-line-options-are-available-)
- [What environmental variables (ENV VARS) are available](#what-environmental-variables-env-vars-are-available-#)
- [--version does not show all versions](#ulspy---version-does-not-show-all-versions)
- [--inputproxy <proxy> does not work as expected](#--inputproxy-proxy-does-not-work-as-expected)

----
## FAQ
### How can the ULS process be monitored ?
ULS provides a [dedicated monitoring output](MONITORING.md) that allows to understand the performance values as well as the throughput.
This can also be used to monitor the "alive state" of ULS.

---
### Which SIEM are supported ?
In general, ULS supports all SIEM that allow any of the provided ULS outputs. Some SIEM may require additional configuration.
We try to collect the instructions out of the experiences collected for specific SIEM in [this folder](SIEM).

---
### ULS is not behaving as expected 
- Try to updated ULS to the latest version.
- Try to update the related "CLI-TOOLS" to the latest version
- Check the [debugging section](DEBUGGING.md) for deeper analysis

---
### Where to get the API credentials ?
There is a dedicated document [explaining API credentials creation](AKAMAI_API_CREDENTIALS.md).

---
### What command line Options are available ? 
There is a dedicated document explaining the [command line parameters and environment variables.](ARGUMENTS_ENV_VARS.md)

---
### What environmental variables (ENV VARS) are available ?
There is a dedicated document explaining the [command line parameters and environment variables.](ARGUMENTS_ENV_VARS.md)

---
### `uls.py --version` does not show all versions
This is (sadly) a known issue. It is a problem within some of the CLI's if no ".edgerc" file is provided. If you provide a `.edgerc`, the show is correct.

---

### `--inputproxy <proxy>` does not work as expected
This is (sadly) a known issue.  
The good news is we do have a proper workaround for this.
Instead of setting the Option `--inputproxy <proxy>` or the ENV var `ULS_INPUT_PROXY` do the following:

Set the ENV following ENV vars to your environment / container.
```text
HTTP_PROXY=http://your.proxy.internal:3128"
HTTPS_PROXY=http://your.proxy.internal:3128"
NO_PROXY="localhost,127.0.0.1,::1"
```
Those can also be added to the .evn file when using docker / docker-compose.  
**Please ensure, you are ADDING YOUR SIEM HOST IP to the NO_PROXY line when the SIEM is internal to avoid issues**  
`NO_PROXY="localhost,127.0.0.1,::1,my_siem.host"`