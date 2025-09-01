# ULS - MISC directory
MISC contains a set of scripts and useful tools around ULS.

## ext_cli_update.sh
This tool helps updating the CLI's, independent of any used installer

Usage
```shell
cd /opt/akamai/uls # Or wherever your ULS directory is...
bash misc/ext_cli_update.sh  
```

---

## mnt_docker_testing.sh (Maintainer only)
This tool helps cross compile a testing container

Usage
```aiignore
cd /opt/akamai/uls # Or wherever your ULS directory is...
bash misc/mnt_docker_testing.sh  

# Confirm with (y) for a push 
```