#!/usr/bin/env bats


## THIS Should be run from ULS ROOT DIR

# Variables
    # ULS Binary
uls_bin=bin/uls.py

    # TESTING EDGERC FILE
#uls_edgerc=~/.edgerc
uls_edgerc=test/_mocked_edgerc

    # TESTING SECTION
uls_section=testing

    # TIMEOUT
uls_test_timeout=30


# Load support libs
load 'test/bats/bats-support/load.bash'
load 'test/bats/bats-assert/load.bash'


#  POSITIVE tests
## EAA
@test "EAA - ACCESS" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input eaa --feed access --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}
@test "EAA - ADMIN" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input eaa --feed admin --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output ""
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

## ETP
@test "ETP - THREAT" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input etp --feed threat --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

@test "ETP - AUP" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input etp --feed aup --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

@test "ETP - DNS" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input etp --feed dns --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

@test "ETP - PROXY" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input etp --feed proxy --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output ""
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
    assert_output ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

@test "TRANSFORM - JMESPATH" {
    run timeout --preserve-status $uls_test_timeout $uls_bin --input eaa --feed access --output raw --transformation jmespath --transformationpattern '[geo_country, geo_state]' --edgerc $uls_edgerc --section $uls_section
    assert_output ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

## AUTORESUME
@test "AUTORESUME - Create File" {
    rm -f /tmp/uls_eaa_access.ckpt
    run timeout --preserve-status $uls_test_timeout $uls_bin --input eaa --feed access --output raw --edgerc $uls_edgerc --section $uls_section --autoresume --autoresumepath /tmp/
    assert_output ""
    #assert_output --partial " seems to be empty"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
    rm -f /tmp/uls_eaa_access.ckpt
}