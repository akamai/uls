#!/usr/bin/env bats

## THIS Should be run from ULS ROOT DIR

# Variables
  # ULS Binary
uls_bin=bin/uls.py

  # Should we using a mocked edgerc (TRUE/FALSE) ?
mocked_edgerc=FALSE

# TIMEOUT
  # How much time is timeout allowed to run
  uls_test_timeout=90
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




## AUTORESUME
@test "AUTORESUME - EAA - ACCESS" {
    rm -f /tmp/uls_eaa_access.ckpt
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed access --output raw --edgerc $uls_edgerc --section $uls_section --autoresume --autoresumepath /tmp/ --autoresumewriteafter 5
    assert_output --partial $eaa_access_assert
    #assert_output --partial " seems to be empty"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ]  || [ "$status" -eq 137 ]       #return value from uls when interrupted --> with --preserve status on timeout
    rm -f /tmp/uls_eaa_access.ckpt
}

@test "AUTORESUME - EAA - ADMIN" {
    rm -f /tmp/uls_eaa_admin.ckpt
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed admin --output raw --edgerc $uls_edgerc --section $uls_section --autoresume --autoresumepath /tmp/ --autoresumewriteafter 5
    assert_output --partial $eaa_access_assert
    #assert_output --partial " seems to be empty"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ]  || [ "$status" -eq 137 ]       #return value from uls when interrupted --> with --preserve status on timeout
    rm -f /tmp/uls_eaa_admin.ckpt
}

@test "AUTORESUME - EAA - CONHEALTH" {
    rm -f /tmp/uls_eaa_conhealth.ckpt
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed conhealth --output raw --edgerc $uls_edgerc --section $uls_section --autoresume --autoresumepath /tmp/ --autoresumewriteafter 5
    assert_output --partial $eaa_access_assert
    #assert_output --partial " seems to be empty"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ]  || [ "$status" -eq 137 ]       #return value from uls when interrupted --> with --preserve status on timeout
    rm -f /tmp/uls_eaa_conhealth.ckpt
}

@test "AUTORESUME - EAA - DEVINV" {
    rm -f /tmp/uls_eaa_devinv.ckpt
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed devinv --output raw --edgerc $uls_edgerc --section $uls_section --autoresume --autoresumepath /tmp/ --autoresumewriteafter 5
    assert_output --partial $eaa_access_assert
    #assert_output --partial " seems to be empty"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ]  || [ "$status" -eq 137 ]       #return value from uls when interrupted --> with --preserve status on timeout
    rm -f /tmp/uls_eaa_devinv.ckpt
}