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
@test "MFA - AUTH" {
    skip "MFA API currently broken"
    run timeout --preserve-status $uls_test_timeout $uls_bin --input mfa --feed auth --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
}

@test "MFA - POLICY" {
    skip "MFA API currently broken"
    run timeout --preserve-status $uls_test_timeout $uls_bin --input mfa --feed policy --output raw --edgerc $uls_edgerc --section $uls_section
    assert_output ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ]       #return value from uls when interrupted --> with --preserve status on timeout
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