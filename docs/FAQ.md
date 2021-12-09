# Frequently asked questions (FAQ)

## Table of contents
- [How can the ULS process be monitored ?](#how-can-the-uls-process-be-monitored-)  
- [Which SIEM are supported ?](#which-siem-are-supported-)
- [Where to get the API credentials ?](#where-to-get-the-api-credentials-)
- [What command line Options are available ? ](#what-command-line-options-are-available-)
- [What environmental variables (ENV VARS) are available](#what-environmental-variables-env-vars-are-available-#)
- [--inputproxy <proxy> does not work as expected](#--inputproxy-proxy-does-not-work-as-expected)
- [Logs are not showing up in my SIEM](#logs-are-not-showing-up-in-siem)
- [ULS on Windows error: "[WinError 2] The system cannot find the file specified"](#uls-on-windows-error-winerror-2-the-system-cannot-find-the-file-specified)

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

### `--inputproxy <proxy>` does not work as expected
There might be some very special use - cases, where the `--inputproxy` parameter fails.
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

---
### Logs are not showing up in SIEM
- Check if ULS is receiving the correct data (use [RAW](OUTPUTS.md#raw) to verify local config)
- Check if ULS can reach the SIEM input (check ULS logs `--loglevel debug`) Common connection issues: firewalls, proxys, local listening ports, host acl's 
- Set the time "Range" to "all time" (As some Akamai Enterprise logs arrive with a delay of up to 3 hours)
- Double check for sanity reasons, that no (additional) filters wihtin your SIEM have been applied
Some excellent troubleshooting guidance from SPLUNK (but also applies to other SIEM as well) can be found [here](https://docs.splunk.com/Documentation/Splunk/6.4.1/Troubleshooting/Cantfinddata)

---
### ULS on Windows error: "[WinError 2] The system cannot find the file specified"
ULS requires the OS to provide a python3 executable. The python installation on Windows somehow (unlike other OS) just installs a "python" executable.  
Luckily this is something that can get sorted easily and in multiple different ways (just pick the one that suites you best):
1) **Create a python3.bat (recommended)**  
To avoid copying the binary you can create a `batch` file and place it in some dir specified in the `$PATH` (the python dir is ok, too).  
Create a python3.bat with the following content:
    ```text
    python %*
    ```  

2) **Copy the binary**  
Go to your python directory on Windows e.g. `C:\Users\Administrator\AppData\Local\Programs\Python\Python310` or `C:\Program Files\Python\Python310`.  
Now copy the `python.exe` executable to  `python3.exe` within the same folder.  

  
3) **Create a powershell alias (temproary only)**  
If you are using powershell, run this before you start ULS.
    ```text
    Set-Alias -Name python3 -Value python
    ```  

4) **Create a symbolic link (requires [mklink](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/mklink))**  
    ```text
    mklink "C:\path\to\symlink\python3.exe" "C:\path\to\Python3\python.exe"
    ```
   
5) **Change ULS config (not recommended)**  
You can modify the bin_python variable within the ULS global config file's `bin/config/global_config.py` 'Generic config' section.#
Change
    ```text
    bin_python = "python3"
    ```
    to
    ```text
    bin_python = "python"
    ```
    **WARNING:** This change prevents the global_config.py file to get updated via GIT in the future. You need to manually take care of updating changes within the file.
    
---
