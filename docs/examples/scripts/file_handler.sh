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
