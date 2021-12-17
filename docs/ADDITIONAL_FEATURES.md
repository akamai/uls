# Additional ULS Features
This document handles the usage of features not explained anywhere else.

## Table of contents<!-- omit in toc -->
- [FILTER (--filter) Feature](#filter---filter-feature)
- [RAWCMD (--rawcmd) Feature](#rawcmd---rawcmd-feature)
- [ULS TRANSFORMATIONS](#uls-transformations)
- [AUTORESUME / RESUME](#autoresume--resume)
- 

## FILTER (--filter) Feature
This feature got introduced in ULS v0.9.0.  
It allows to decrease the number of log lines sent to SIEM for cost, performance or security reasons.

The filter is **regex** based so it is capable of filtering "json" AND raw text events. 
Only events **matching the filter pattern will be sent towards the selected SIEM** output.
Filtering can lead to higher CPU / MEMORY consumption in production environments.  
For ETP there is also an option to [filter directly on the API request side](AKAMAI_API_CREDENTIALS.md#etp-api-event-filters).

### Usage examples:
- Filter for "geo_country": "Germany" (in EAA Access logs)
    ```bash
    python3 bin/uls.py -i eaa -f access -o raw <additional params> --filter '.*"geo_country": "Germany".*'
    ```
- Filter for "actionName": "Block - Error Page" (in ETP Threat logs)
    ```bash
    python3 bin/uls.py -i etp -f threat -o raw <additional params> --filter '.*"actionName": "Block - Error Page".*'
    ```
Always test your filter with the "RAW" console output on the command line before you send the data towards a SIEM
```bash
python3 bin/uls.py -i eaa --feed access --filter '.*"geo_country": "Germany".*' -o raw
```

## RAWCMD (--rawcmd) Feature
This feature got introduced in ULS v0.0.3.  
Attention: This is a pretty critical setting, which can break ULS behaviour.

Raw commands within ULS can be used to trigger cli calls, that have not been integrated into ULS (yet).
This allows a more flexible implementation to solve some edge cases.
RAWCMD just requires the input to be selected.

Example:
```bash
python3 bin/uls.py -i etp --rawcmd 'event threat -f' -l debug -o raw
```
This will also run the etp threat feed in "tail -f" mode

Please be aware: Not all output from the cli will be redirected to ULS by default.

# ULS TRANSFORMATIONS
Transformations have been introduced to ULS in version `1.2.0` to support additional 3rd party integrations and custom log formats.
Please see the dedicated "[Transformations docs](TRANSFORMATIONS.md)" available.


# AUTORESUME / RESUME
This feature was introduced in ULS 1.3.0.  
Different circumstances (network isse, server maintainence, ...) could lead to an interruption of the log stream or ULS itself.
As this could cause a gap in the continuous log delivery, ULS now offers the option to enable automated resume upon the last recorded checkpoint.

AUTORESUME will create a checkpoint every 1000 lines of log (configureable) to prevent too many FS operations.
This means, in the worst case, the 1000 lines of log are going to be re-imported.

Example:
```bash
bin/uls.py -input etp -feed threat --output raw --autoresume
```
Autoresume can also be set via [environment variables (ENV)](ARGUMENTS_ENV_VARS.md#autoresume).  
Attention: Do not use --autoresume alongside the --starttime argument or ENV variable, as ULS would not know where to start from.
For DOCKER based environments, please make sure you're using a volume or mount towards the var (default but configureable) directory within ULS.

Additional configuration options:
[--autoresumepath](ARGUMENTS_ENV_VARS.md#autoresume)
[--autoresumewriteafter](ARGUMENTS_ENV_VARS.md#autoresume)


# POST PROCESSING OF FILES (FileOutput only)
This feature was introduced in ULS 1.3.0.
This allows to take over the control of the file post-processing workflow (asynchronous).
It is highly recommended to specify a binary or script that consumes the absolute file name as input.

Ensure the following things:
- this will only work with `--output file`
- this will only work with `--filebackupcount 1`
- ensure to escape the `%s` like `'%s'` when specificy on the console


## Warnings
- ULS will just fire the process - but not care about "error/fallback handling"
- If the script "messes" up the file, the file is lost!
- If the file is not processed fast enough - the file is lost / overwritten! (size the rotation rules accordingly)
- Output of the "file handler" will be directly written to the console
- ULS will NOT take care of rotating your processed files. Please delete old log files on your own.


Example:  
/opt/msycript.sh
```bash
#!/bin/bash

target_dir="/tmp"
file_name="log_$(date +%Y%M%d-%H%m%S).gz"

if [[ -z $1 ]] ; then
        echo "No file given - please specify absolute path"
        exit 1
fi
gzip -cvf $1 > ${target_dir=}/${file_name=}
echo "->  ${target_dir=}/${file_name=}"
rm $1
```
You can find the [example script here](examples/scripts/file_handler.sh).

Run ULS using the fileaction script
```bash
./bin/uls.py -i etp -f threat -o file --filename /tmp/logtest/test1.log --filehandler SIZE --filemaxbytes 10240000 --fileaction --filebackupcount 1 "/opt/msycript.sh '%s'"  
```

Here's  a recommendation on how to use this feature to avoid any "glitches":  
Use the --fileaction handler to move the file into an observed queue directory and start a new process from there.
This will ensure a "fast handling" within ULS and provide even more flexibility/stability towards the worklfow and its error handling.

