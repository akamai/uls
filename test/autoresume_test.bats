#!/usr/bin/env bats

## THIS Should be run from ULS ROOT DIR

# Variables
  # ULS Binary
uls_bin=bin/uls.py

  # Should we using a mocked edgerc (TRUE/FALSE) ?
mocked_edgerc=FALSE

# TIMEOUT
  # How much time is timeout allowed to run
  uls_test_timeout=30
  # Send a kill signal after
  uls_kill_timeout=110
  # Used for regular timeout
  uls_timeout_signal="TERM"
  uls_timeout_params=" --preserve-status --kill-after $uls_kill_timeout --signal ${uls_timeout_signal} ${uls_test_timeout} "

### Switch between mocked and real edgerc
if [ "$mocked_edgerc"=="FALSE" ] ; then
  # REAL EDGERC FILE
  uls_edgerc=~/.edgerc
  uls_section=akamaidemo


  # Variables
  eaa_access_assert="username"
  eaa_devinv_assert="client_version"
  etp_assert="configId"
  gc_assert="flow_id"
  linode_assert=""
  jmespath_assert='["'
else
  # TESTING EDGERC FILE & section
  uls_edgerc=test/_mocked_edgerc
  uls_section=testing
  # Variables
  eaa_access_assert=""
  eaa_devinv_assert=""
  etp_assert=""
  gc_assert=""
  linode_assert=""
  jmespath_assert=""
fi

# Load support libs
load 'bats/bats-support/load.bash'
load 'bats/bats-assert/load.bash'




## before we use this here, we need to actively allow "monitoring interval manipuluation"

#for item in ACCESS ADMIN CONHEALTH DEVINV DIRHEALTH; do

## AUTORESUME
@test "AUTORESUME - EAA ACCESS - Create" {
    rm -f /tmp/uls_eaa_access.ckpt
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed access --output raw --edgerc $uls_edgerc --section $uls_section --moninterval 10 -o none --autoresumewriteafter 1 --autoresume --autoresumepath /tmp/ -l debug
    assert_output --partial "current_checkpoint\": \"$(date +%Y-%m-%d)"
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ]  || [ "$status" -eq 137 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

@test "AUTORESUME - EAA ACCESS - FileCheck" {
    run timeout ${uls_timeout_params} cat /tmp/uls_eaa_access.ckpt
    assert_output --partial "checkpoint\": \"$(date +%Y-%m-%d)"
    [ "$status" -eq 0 ]
}

@test "AUTORESUME - EAA ACCESS - RESUME" {
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed access --output raw --edgerc $uls_edgerc --section $uls_section --moninterval 10 -o none --autoresumewriteafter 1 --autoresume --autoresumepath /tmp/ -l debug
    assert_output --partial "Autoresume Checkpoint successfully loaded. Checkpoint Time: $(date +%Y-%m-%d)"
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ]  || [ "$status" -eq 137 ]
}