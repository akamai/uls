#!/bin/bash
#
# Description
# -----------
# Creates a sample file to test against QRadar DSM Editor.
#
# Requirements
# ------------
# - Akamai CLI with eaa modules
# - Credentials in the default section of the ~/.edgerc file

# Adjust how far back you want the log to go
# It will vary based on your EAA account activity
START=$(( $(date +%s) - 7 * 24 * 60 * 60 ))

shuf() { awk 'BEGIN {srand(); OFMT="%.17f"} {print rand(), $0}' "$@" |
               sort -k1,1n | cut -d ' ' -f2-; }

tmp_dir=$(mktemp -d -t ak-uls-qradar-XXXXXXXXXX)
echo "Working in temporary directory $tmp_dir"

echo "Fetching access events..."
akamai eaa log admin --start $START --json --output $tmp_dir/eaa_admin.json
echo "Fetching admin audit events..."
akamai eaa log access --start $START --json --output $tmp_dir/eaa_access.json
echo "Fetching connector health events..."
akamai eaa connector list --perf --json > $tmp_dir/eaa_conhealth.json

cat $tmp_dir/eaa_admin.json | shuf | head -n 50 > $tmp_dir/eaa_admin_min.json
cat $tmp_dir/eaa_access.json | shuf | head -n 50 > $tmp_dir/eaa_access_min.json
cat $tmp_dir/eaa_conhealth.json | shuf > $tmp_dir/eaa_conhealth_min.json

cat $tmp_dir/eaa_admin_min.json $tmp_dir/eaa_access_min.json $tmp_dir/eaa_conhealth_min.json | shuf > eaa_feeds_combined_sample.json

stat eaa_feeds_combined_sample.json
echo "File 'eaa_feeds_combined_sample.json' created in the current directory ($(pwd))."

rm -v -rf $tmp_dir