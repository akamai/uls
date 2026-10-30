#!/bin/bash
# This file will install the latest ULS including all of its modules (latest version) into the current directory/uls
# curl -O https://raw.githubusercontent.com/akamai/uls/main/scripts/get-uls.sh && bash get-uls.sh

default_modules="eaa,etp,gc,ln,acc"
known_modules=(eaa etp gc ln acc)
default_install_dir="$(pwd)/uls"

function die() {
  echo "ERROR: $*" >&2
  echo "Installation FAILED - exiting" >&2
  exit 1
}

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

function has_module() {
  # Exact match of a module name against the selected module list
  local m
  for m in "${selected_modules[@]}"; do
    [[ "$m" == "$1" ]] && return 0
  done
  return 1
}

function clone_or_update() {
  # Usage: clone_or_update repo_url target_dir [git clone options...]
  local repo="$1" target="$2"
  shift 2
  if [[ -d "${target}/.git" ]] ; then
    echo "  ${target} already exists - updating"
    git -C "${target}" pull -q --ff-only || die "Could not update ${target}"
  else
    git clone -q "$@" "${repo}" "${target}" || die "Could not clone ${repo} into ${target}"
  fi
}
CVE-2026-111497
function py_reqs() {
  local to_install
  to_install=$(pip3 install --dry-run -r "$1" | grep -vi "satisfied")
  if [[ -n "$to_install" ]] ; then
    echo "We are going to install the following python3 requirements:"
    echo "----"
    echo "$to_install"
    echo "----"

    echo "Do you want to stop here and install OS packages instead [y|N]?"
    read -r package_stop
    case $package_stop in
      y|Y)
          echo "Stopping installation - please install the required packages manually - exiting"
          exit 1
      ;;
      *)
        echo "installing packages via PIP now"
      ;;
    esac
  fi
}

function install_reqs() {
  [[ -f "$1" ]] || die "Requirements file $1 not found"
  py_reqs "$1"
  pip3 install -q -r "$1" || die "pip3 failed to install requirements from $1"
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
  gc:  Akamai Guardicore Segmentation
  ln:  Linode Audit log
  acc: Akamai Control Center logs

More about supported feed:
https://github.com/akamai/uls/blob/main/docs/LOG_OVERVIEW.md"
echo -e "\n\n\n"

# Preflight checks
## check git
if ! command -v git > /dev/null ; then
  echo "GIT binary was not found - exiting"
  exit 1
fi

## check python version
### check python exists
if ! command -v python3 > /dev/null ; then
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
if ! command -v pip3 > /dev/null ; then
  echo "pip3 binary was not found - exiting"
  exit 1
fi

### Check PIP version
pip3_min_version="22.2"
pip3_version="$(pip3 --version|cut -d' ' -f2)"
min_version "${pip3_min_version}" "${pip3_version}" || {
  echo "pip3 version must be >= ${pip3_min_version}, version detected: ${pip3_version}"
  echo "Consider upgrading your PIP version with command:"
  echo "  $(command -v pip3) install --upgrade pip"
  exit 1
}

### Show versions to verify the correct binaries for python and pip are being used
echo "We will use the following python binaries to install ULS:"
echo -ne "python3: \t $(python3 -c 'import sys; print(sys.executable)') (${py_version})\n"
echo -ne "pip3: \t\t $(pip3 --version)\n\n"
echo -ne "Is this correct (Y|n)"
read -r py_reply


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
read -r install_dir
if [[ -z "${install_dir}" ]] ; then
  install_dir=${default_install_dir}
fi

## Install Modules
echo -n "Modules [$default_modules] (ENTER for all): "
read -r install_modules
if [[ -z "$install_modules" ]] ; then
  install_modules=$default_modules
fi

### Split the comma separated list and validate every entry
IFS=',' read -r -a raw_modules <<< "${install_modules// /}"
selected_modules=()
for m in "${raw_modules[@]}"; do
  [[ -z "$m" ]] && continue
  if [[ ! " ${known_modules[*]} " == *" $m "* ]] ; then
    echo "Unknown module \"$m\" - valid modules are: ${known_modules[*]} - exiting"
    exit 1
  fi
  selected_modules+=("$m")
done

echo -e "\n\n\n\n\n"
echo "Installing ULS to: $install_dir"
echo "Modules to install: ${selected_modules[*]}"

## Are you allright to continue ?
echo -ne "Are the above settings correct? [yN]"
read -r continue

if [[ ! "$continue" == "y" ]] ; then
  echo "Configuration not confirmed, exiting"
  exit 1
fi

## Check if ULS is already installed ?
if [[ -f "${install_dir}/bin/uls.py" ]] ; then
  echo -e "\n\nAttention:\n"
  echo "ULS seems to be already installed."
  echo "Proceeding will update the existing installation (git pull) and its modules."
  echo -n "Do you want to proceed [yN]"
  read -r already_installed
  if [[ ! ${already_installed} == "y" ]] ; then
    echo "Stopping installation - exiting"
    exit 1
  fi
elif [[ -e "${install_dir}" && -n "$(ls -A "${install_dir}" 2>/dev/null)" ]] ; then
  die "${install_dir} exists and is not empty (and is not a ULS installation)"
fi

# Installation
## Grab ULS
echo "Installing ULS"
clone_or_update https://github.com/akamai/uls.git "${install_dir}"
install_reqs "${install_dir}/bin/requirements.txt"

## Grab EAA-CLI
if has_module eaa ; then
  echo "Installing EAA-CLI"
  clone_or_update https://github.com/akamai/cli-eaa.git "${install_dir}/ext/cli-eaa" --depth 1 --single-branch
  install_reqs "${install_dir}/ext/cli-eaa/requirements.txt"
fi

## GRAB ETP-CLI
if has_module etp ; then
  echo "Installing ETP-CLI"
  clone_or_update https://github.com/akamai/cli-etp.git "${install_dir}/ext/cli-etp" --depth 1 --single-branch
  install_reqs "${install_dir}/ext/cli-etp/requirements.txt"
fi

## GRAB GC-CLI
if has_module gc ; then
  echo "Installing GC-CLI"
  clone_or_update https://github.com/MikeSchiessl/gc-logs.git "${install_dir}/ext/cli-gc" --depth 1 --single-branch
  install_reqs "${install_dir}/ext/cli-gc/bin/requirements.txt"
fi

## GRAB LINODE-CLI
if has_module ln ; then
  echo "Installing LINODE-CLI"
  clone_or_update https://github.com/MikeSchiessl/ln-logs.git "${install_dir}/ext/cli-linode" --depth 1 --single-branch
  install_reqs "${install_dir}/ext/cli-linode/bin/requirements.txt"
fi

## GRAB ACC-CLI
if has_module acc ; then
  echo "Installing ACC-CLI"
  clone_or_update https://github.com/MikeSchiessl/acc-logs.git "${install_dir}/ext/acc-logs" --depth 1 --single-branch
  install_reqs "${install_dir}/ext/acc-logs/bin/requirements.txt"
fi


# Finishing off
echo -e "\n\n\n"
python3 "${install_dir}/bin/uls.py" --version || die "ULS was installed but does not start"
echo "ULS has been successfully installed"


exit 0
