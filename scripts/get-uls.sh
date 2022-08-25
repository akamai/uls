#!/bin/bash
# This file will install the latest ULS including all of its modules (latest version) into the current directory/uls
# bash $(curl https://)

default_modules="eaa,etp,mfa,gc,ln"
default_install_dir="$(pwd)/uls"


echo -e "
	   AKAMAI
   _/    _/  _/          _/_/_/   
  _/    _/  _/        _/          
 _/    _/  _/          _/_/       
_/    _/  _/              _/      
 _/_/    _/_/_/_/  _/_/_/         
                                  
Universal Log Stream - Installer"
echo -e "\n\n\n"

# Preflight checks
## check git
if [[ -z $(which git) ]] ; then
  echo "GIT binary was not found - exiting"
  exit 1
fi

## check python version
if [[ -z $(which python3) ]] ; then
  echo "Python3 binary was not found - exiting"
  exit 1
fi

py_version=$(python3 --version | cut -d " " -f 2)
if [[ $(echo ${py_version} | cut -d "." -f 1 ) -ne 3 ]] || [[ $(echo ${py_version} | cut -d "." -f 2 ) -lt 9 ]]; then
  echo "Wrong Python version - exiting"
  exit 1
fi

## pip3
if [[ -z $(which pip3) ]] ; then
  echo "Python3 binary was not found - exiting"
  exit 1
fi

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

## Continue anywaY ?


# Installation 
## Grab ULS
git clone -q https://github.com/akamai/uls.git $install_dir/
pip3 install -q -r ${install_dir}/bin/requirements.txt


## Grab EAA-CLI
if [[ "$install_modules" == *"eaa"* ]]  ; then
echo "Installing EAA-CLI"
  git clone -q --depth 1 --single-branch https://github.com/akamai/cli-eaa.git ${install_dir}/ext/cli-eaa
  pip3 install -q -r ${install_dir}/ext/cli-eaa/requirements.txt
fi 

## GRAB ETP-CLI
if [[ "$install_modules" == *"etp"* ]]  ; then
echo "Installing ETP-CLI"
  git clone -q --depth 1 --single-branch https://github.com/akamai/cli-etp.git ${install_dir}/ext/cli-etp
  pip3 install -q -r ${install_dir}/ext/cli-etp/requirements.txt
fi

## GRAB MFA-CLI
if [[ "$install_modules" == *"mfa"* ]]  ; then
echo "Installing MFA-CLI"
  git clone -q --depth 1 --single-branch https://github.com/akamai/cli-mfa.git ${install_dir}/ext/cli-mfa
  pip3 install -q -r ${install_dir}/ext/cli-mfa/requirements.txt
fi

## GRAB GC-CLI
if [[ "$install_modules" == *"gc"* ]]  ; then
echo "Installing GC-CLI"
  git clone -q --depth 1 -b dev --single-branch https://github.com/MikeSchiessl/gc-logs.git ${install_dir}/ext/cli-gc
  pip3 install -q -r ${install_dir}/ext/cli-gc/bin/requirements.txt
fi

## GRAB LN-CLI
if [[ "$install_modules" == *"ln"* ]]  ; then
echo "Installing LN-CLI"
  git clone -q --depth 1 -b dev --single-branch https://github.com/MikeSchiessl/ln-logs.git ${install_dir}/ext/cli-linode
  pip3 install -q -r ${install_dir}/ext/cli-ln/bin/requirements.txt
fi

# Finishing off
echo -e "\n\n\n"
echo "ULS has been successfully installed"
${install_dir}/bin/uls.py --version


exit 0