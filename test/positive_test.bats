#!/usr/bin/env bats


## THIS Should be run from ULS ROOT DIR

# Variables
  # ULS Binary
uls_bin=bin/uls.py

  # Should we using a mocked edgerc (TRUE/FALSE) ?
mocked_edgerc=FALSE

  # TIMEOUT
uls_test_timeout=60


### Switch between mocked and real edgerc
if [ "$mocked_edgerc"=="FALSE" ] ; then
  # REAL EDGERC FILE
  uls_edgerc=~/.edgerc
  uls_section=akamaidemo
  # Variables
  eaa_access_assert="username"
  eaa_devinv_assert="client_version"
  etp_assert="configId"
  jmespath_assert="['"
else
  # TESTING EDGERC FILE & section
  uls_edgerc=test/_mocked_edgerc
  uls_section=testing
  # Variables
  eaa_access_assert=""
  eaa_devinv_assert=""
  etp_assert=""
  jmespath_assert=""
fi

# Load support libs
load 'bats/bats-support/load.bash'
load 'bats/bats-assert/load.bash'


#  POSITIVE tests
## EAA
@test "EAA - ACCESS" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input eaa --feed access --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output --partial $eaa_access_assert
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}
@test "EAA - ADMIN" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input eaa --feed admin --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output --partial ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}
@test "EAA - CONHEALTH" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input eaa --feed admin --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}
@test "EAA - DEVINV" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input eaa --feed devinv --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output --partial $eaa_devinv_assert
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

## ETP
@test "ETP - THREAT" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input etp --feed threat --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output --partial $etp_assert
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

@test "ETP - AUP" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input etp --feed aup --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output --partial $etp_assert
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

@test "ETP - DNS" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input etp --feed dns --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output --partial $etp_assert
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

@test "ETP - PROXY" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input etp --feed proxy --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output --partial $etp_assert
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

## MFA
@test "MFA - EVENT" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input mfa --feed event --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

## FILE OUTPUT
@test "FILE: ETP - THREAT" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input etp --feed threat --output file --filename "/tmp/uls_tmplogfile.log" --edgerc $uls_edgerc --section $uls_section
    assert_output ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
    rm -fr /tmp/uls_tmplogfile.log
}

@test "FILEACTION: ETP - THREAT" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input etp --feed threat --output file --filename "/tmp/uls_tmplogfile.log" --filebackup 1 --fileaction "/bin/zip '%s'" --edgerc $uls_edgerc --section $uls_section
    assert_output ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
    rm -fr /tmp/uls_tmplogfile.log
}

## Transformation
@test "TRANSFORM - MCAS" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input etp --feed dns --output raw --transformation mcas --edgerc $uls_edgerc --section $uls_section
    assert_output --partial "detection_time"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

@test "TRANSFORM - JMESPATH" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input eaa --feed access --output raw --transformation jmespath --transformationpattern '[geo_country, geo_state]' --edgerc $uls_edgerc --section $uls_section
    assert_output --partial $jmespath_assert
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

## AUTORESUME
@test "AUTORESUME - Create File" {
    rm -f /tmp/uls_eaa_access.ckpt
    run timeout --preserve-status $uls_test_timeout $uls_bin --input eaa --feed access --output raw --edgerc $uls_edgerc --section $uls_section --autoresume --autoresumepath /tmp/
    assert_output --partial $eaa_access_assert
    #assert_output --partial " seems to be empty"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
    rm -f /tmp/uls_eaa_access.ckpt
}