#!/bin/bash

# This file updates all existing "git" - cli repos within the ULS "ext/" directory.


# find the correct path for ext/
MY_TARGET_PATH="ext/"
if [[ ! -d "${MY_TARGET_PATH}" ]] ; then
  MY_TARGET_PATH="../${MY_TARGET_PATH}"
fi
if [[ ! -d "${MY_TARGET_PATH}" ]] ; then
  MY_TARGET_PATH="../../${MY_TARGET_PATH}"
fi
if [[ ! -d "${MY_TARGET_PATH}" ]] ; then
  MY_TARGET_PATH="../../../${MY_TARGET_PATH}"
fi
if [[ ! -d "${MY_TARGET_PATH}" ]] ; then
  MY_TARGET_PATH="$(pwd)/ext/"
fi
if [[ ! -d "${MY_TARGET_PATH}" ]] ; then
  echo "not able to find the right path - exiting"
  exit 1
fi
echo "Updating clis in ${MY_TARGET_PATH}"

# Actually do the update
for cli_path in `ls -d ${MY_TARGET_PATH}*/ ` ; do
  echo "CLI: $(basename ${cli_path})"
  git -C ${cli_path} pull
done
exit 0

# EOF
