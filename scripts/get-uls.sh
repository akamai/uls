#!/bin/bash
# This file will install the latest ULS including all of its modules (latest version) into the current directory/uls
# curl -O https://raw.githubusercontent.com/akamai/uls/main/scripts/get-uls.sh && bash get-uls.sh

default_modules="eaa,etp,mfa,gc,ln,acc"
default_install_dir="$(pwd)/uls"

function min_version() {
  # Test if a given version string matches the requirements
  # Usage:
  #   min_version required_min_version version
  # Function returns:
  #   0 if the version is equal or greater than the requirement
  #   1 if the version is lower
  local required_ver="$1"
  local current_ver="$2"
  if [ "$(printf '%s\n' "$required_ver" "$current_ver" | sort -V | head -n1)" = "$required_ver" ]; then 
    return 0
  else
    return 1
  fi
}

echo -e "
	   AKAMAI
   _/    _/  _/          _/_/_/   
  _/    _/  _/        _/          
 _/    _/  _/          _/_/       
_/    _/  _/              _/      
 _/_/    _/_/_/_/  _/_/_/         
                                  
Unified Log Streamer - Installer

Available ULS modules:
  eaa: Enterprise Application Access
  etp: Secure Internet Access Enterprise
  mfa: Akamai phishproof MFA
  gc:  Akamai Guardicore Segmentation
  ln:  Linode Audit log

More about supported feed: 
https://github.com/akamai/uls/blob/main/docs/LOG_OVERVIEW.md"
echo -e "\n\n\n"

# Preflight checks
## check git
if [[ -z $(which git) ]] ; then
  echo "GIT binary was not found - exiting"
  exit 1
fi

## check python version
### check python exists
if [[ -z $(which python3) ]] ; then
  echo "Python3 binary was not found - exiting"
  exit 1
fi

### check python version is correct for ULS
py_min_version="3.9"
py_version=$(python3 --version | cut -d " " -f 2)
min_version "${py_min_version}" "${py_version}" || {
  echo "Python version must be >= ${py_min_version}, found ${py_version} - exiting"
  exit 1
}

## pip3
if [[ -z $(which pip3) ]] ; then
  echo "pip3 binary was not found - exiting"
  exit 1
fi

### Check PIP version
pip3_min_version="22.2"
pip3_version="$(pip3 --version|cut -d' ' -f2)"
min_version "${pip3_min_version}" "${pip3_version}" || {
  echo "pip3 version must be >= ${pip3_min_version}, version detected: ${pip3_version}"
  echo "Consider upgrading your PIP version with command:"
  echo "  $(which pip3) install --upgrade pip"
  exit 1
}

### Show versions to verify the correct binaries for python and pip are being used
echo "We will use the following python binaries to install ULS:"
echo -ne "python3: \t $(ls $(which python3))\n"
echo -ne "pip3: \t\t $(ls $(which pip3))\n\n"
echo -ne "Is this correct (Y|n)"
read py_reply


case $py_reply in
  n|N)
    echo -e "Not the right version ?\nPlease adjust your ENV and SYMLINK settings to point to the correct binaries."
    echo -e "EXITING !"
    exit 1
  ;;
  *)
    echo "Continuing"
esac

# ASK for INSTALL DETAILS 
## Install DIR 
echo -n "Installation Dir [Default: \"$default_install_dir\"] (ENTER for default or new value): "
read install_dir
if [[ -z "${install_dir}" ]] ; then
  install_dir=${default_install_dir}
fi

## Install Modules
echo -n "Modules [$default_modules] (ENTER for all): " 
read install_modules
if [[ -z "$install_modules" ]] ; then
  install_modules=$default_modules
fi

echo -e "\n\n\n\n\n"
echo "Installing ULS to: $install_dir"
echo "Modules to install: $install_modules"

## Are you allright to continue ?
echo -ne "Are the above settings correct? [yN]"
read continue

if [[ ! "$continue" == "y" ]] ; then
  echo "Configuration not confirmed, exiting"
  exit 1
fi

## Check if ULS is already installed ?
if [[ -f "${install_dir}/bin/uls.py" ]] ; then
  echo -e "\n\nAttention:\n"
  echo "ULS seems to be already installed."
  echo "Proceeding with the installation could lead to some serious issue."
  echo -n "Do you want to proceed [yN]"
  read already_installed
  if [[ ! ${already_installed} == "y" ]] ; then
    echo "Stopping installation - exiting"
    exit 1
  fi
fi

## Continue anyway ?
# Installation
## Grab ULS
git clone -q https://github.com/akamai/uls.git $install_dir/
pip3 install -q -r ${install_dir}/bin/requirements.txt


function py_reqs() {
  to_install=$(pip3 install --dry-run -r $1 | grep -vi "satisfied")
  if [[ ! -z $to_install ]] ; then
    echo "We are going to install the following python3 requirements:"
    echo "----"
    echo $to_install
    echo "----"

    echo "Do you want to stop here and install OS packages instead [y|N]?"
    read package_stop
    case $package_stop in
      y|Y)
          echo "Stopping installation - please install the requried packages manually - exiting"
          exit 1
      ;;
      *)
        echo "installing packages via PIP now"
      ;;
    esac
  fi
}

## Grab EAA-CLI
if [[ "$install_modules" == *"eaa"* ]]  ; then
echo "Installing EAA-CLI"
  git clone -q --depth 1 --single-branch https://github.com/akamai/cli-eaa.git ${install_dir}/ext/cli-eaa
  #echo "${install_dir}/ext/cli-eaa/requirements.txt"
  py_reqs ${install_dir}/ext/cli-eaa/requirements.txt
  pip3 install -q -r ${install_dir}/ext/cli-eaa/requirements.txt
fi 

## GRAB ETP-CLI
if [[ "$install_modules" == *"etp"* ]]  ; then
echo "Installing ETP-CLI"
  git clone -q --depth 1 --single-branch https://github.com/akamai/cli-etp.git ${install_dir}/ext/cli-etp
 py_reqs ${install_dir}/ext/cli-etp/requirements.txt
  pip3 install -q -r ${install_dir}/ext/cli-etp/requirements.txt
fi

## GRAB MFA-CLI
if [[ "$install_modules" == *"mfa"* ]]  ; then
echo "Installing MFA-CLI"
  git clone -q --depth 1 --single-branch https://github.com/akamai/cli-mfa.git ${install_dir}/ext/cli-mfa
  py_reqs ${install_dir}/ext/cli-mfa/requirements.txt
  pip3 install -q -r ${install_dir}/ext/cli-mfa/requirements.txt
fi

## GRAB GC-CLI
if [[ "$install_modules" == *"gc"* ]]  ; then
echo "Installing GC-CLI"
  git clone -q --depth 1 -b dev --single-branch https://github.com/MikeSchiessl/gc-logs.git ${install_dir}/ext/cli-gc
  py_reqs ${install_dir}/ext/cli-gc/bin/requirements.txt
  pip3 install -q -r ${install_dir}/ext/cli-gc/bin/requirements.txt
fi

## GRAB LINODE-CLI
if [[ "$install_modules" == *"acc"* ]]  ; then
echo "Installing ACC-CLI"
  git clone -q --depth 1 -b dev --single-branch https://github.com/MikeSchiessl/acc-logs.git ${install_dir}/ext/cli-linode
  py_reqs ${install_dir}/ext/cli-linode/bin/requirements.txt
  pip3 install -q -r ${install_dir}/ext/cli-linode/bin/requirements.txt
fi

## GRAB ACC-CLI
if [[ "$install_modules" == *"gc"* ]]  ; then
echo "Installing ACC-CLI"
  git clone -q --depth 1 -b dev --single-branch https://github.com/MikeSchiessl/acc-logs.git ${install_dir}/ext/acc-logs
  py_reqs ${install_dir}/ext/acc-logs/bin/requirements.txt
  pip3 install -q -r ${install_dir}/ext/acc-logs/bin/requirements.txt
fi


# Finishing off
echo -e "\n\n\n"
echo "ULS has been successfully installed"
${install_dir}/bin/uls.py --version


exit 0