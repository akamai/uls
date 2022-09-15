#!/bin/bash
set -e

default_uls_dir="$(pwd)"


echo -e "
	   AKAMAI
   _/    _/  _/          _/_/_/
  _/    _/  _/        _/
 _/    _/  _/          _/_/
_/    _/  _/              _/
 _/_/    _/_/_/_/  _/_/_/

Universal Log Stream - Updater"
echo -e "\n\n\n"





# ASK for INSTALL DETAILS
## Install DIR
echo -n "Update (ULS) Dir [Default: \"$default_uls_dir\"] (ENTER for default or new value): "
read uls_dir
if [[ -z "${uls_dir}" ]] ; then
  uls_dir=${default_uls_dir}
fi

# Pre flight checks
if [[ -f "${uls_dir}/bin/uls.py" ]] ; then
  echo "ULS found in ${uls_dir}"
elif [[ -f "${uls_dir}/../bin/uls.py" ]] ; then
  uls_dir="${uls_dir}/../"
  echo "ULS found in ${uls_dir}"
else
  echo -e "\n\n\n"
  echo "ULS not found in ${uls_dir} ."
  echo "Please specify a the correct directory (root of ULS) - exiting"
  exit 1
fi

echo "Current Versions (pre update)"
${uls_dir}/bin/uls.py --version

echo -e "\n\n\nDo you want to continue ? [yN]"
read continue

if [[ ! "${continue}" == "y" ]] ; then
  echo "Aborting update - exiting"
  exit 1
fi


# Running the updates
## ULS
echo "Updating ULS"
git -C ${uls_dir} pull -q
pip3 install -q -r ${uls_dir}/bin/requirements.txt

## EAA
if [[ -d "${uls_dir}/ext/cli-eaa" ]] ; then
  echo "EAA-CLI detected, updating"
  git -C ${uls_dir}/ext/cli-eaa pull -q
  pip3 install -q -r ${uls_dir}/ext/cli-eaa/requirements.txt
else
  echo "NO EAA-CLI detected - skipping"
fi

## ETP
if [[ -d "${uls_dir}/ext/cli-etp" ]] ; then
  echo "ETP-CLI detected, updating"
  git -C ${uls_dir}/ext/cli-etp pull -q
  pip3 install -q -r ${uls_dir}/ext/cli-etp/requirements.txt
else
  echo "NO ETP-CLI detected - skipping"
fi

## MFA
if [[ -d "${uls_dir}/ext/cli-mfa" ]] ; then
  echo "MFA-CLI detected, updating"
  git -C ${uls_dir}/ext/cli-mfa pull -q
  pip3 install -q -r ${uls_dir}/ext/cli-mfa/requirements.txt
else
  echo "NO MFA-CLI detected - skipping"
fi

## GC
if [[ -d "${uls_dir}/ext/cli-gc" ]] ; then
  echo "GC-CLI detected, updating"
  git -C ${uls_dir}/ext/cli-gc pull -q
  pip3 install -q -r ${uls_dir}/ext/cli-gc/bin/requirements.txt
else
  echo "NO GC-CLI detected - skipping"
fi


## LINODE
if [[ -d "${uls_dir}/ext/cli-ln" ]] ; then
  echo "LINODE-CLI detected, updating"
  git -C ${uls_dir}/ext/cli-linode pull -q
  pip3 install -q -r ${uls_dir}/ext/cli-linode/bin/requirements.txt
else
  echo "NO LN-CLI detected - skipping"
fi


echo -e "\n\n\nUpdate is complete."
echo "Updated versions (post update)"
${uls_dir}/bin/uls.py --version


exit 0