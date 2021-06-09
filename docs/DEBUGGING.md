# ULS DEBUGGING
This document describes the debugging of the ULS software.  
Please make sure you follow the steps before filing an issue on the  [GitHub Issues Page](https://github.com/akamai/uls/issues).
Follow the steps to collect "supportive" data you should also provide when filing an issue.

## Table of contents
- [Version Information](#version-information)
- [Debug Output](#debug-output)

## Version information
Providing information about relevant module & software versions can help identify issues.
###Commands to trigger version output
####Command Line:
```bash
python3 bin/uls.py --version
```
####Docker
```bash
docker run -ti --mount type=bind,source="/path/to/your/.edgerc",target="/opt/akamai-uls/.edgerc",readonly --rm akamai/uls -v 
```

###Example Output
```text
Akamai Unified Log Streamer Version information
ULS Version             0.0.1

EAA Version             0.3.8
ETP Version             0.3.4
MFA Version             0.0.4

OS Plattform            Linux-5.10.25-linuxkit-x86_64-with-glibc2.28
OS Version              5.10.25-linuxkit
Python Version          3.9.5

```


## Debug Output
To debug problems into depth, ULS provides an extremely verbose output about every step processed within ULS.
###Commands to trigger debug output
####Command Line:
```bash
python3 bin/uls.py --loglevel debug <rest of your ULS command>
```
####Docker
```bash
docker run -ti --mount type=bind,source="/path/to/your/.edgerc",target="/opt/akamai-uls/.edgerc",readonly \
  --rm akamai/uls --loglevel debug \
  <rest of your ULS command> 
```

Instead of adding it to the command line, you can also set the `ULS_LOGLEVEL` ENV VAR to "DEBUG"
