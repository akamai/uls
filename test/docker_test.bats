#!/usr/bin/env bats

## THIS Should be run from ULS ROOT DIR

# Variables
  # ULS Binary
uls_bin=bin/uls.py

  # Should we using a mocked edgerc (TRUE/FALSE) ?
mocked_edgerc=FALSE

# TIMEOUT
  # How much time is timeout alklowed to run
  uls_test_timeout=10
  # Send a kill signal after
  uls_kill_timeout=15
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
  jmespath_assert="['"
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

# DOCKER TESTING

## Make sure everything is tidy and clean after every test ;)
teardown () {
    docker stop uls-bats-test && docker rm uls-bats-test
    return 0
}

## CREATE a local DOCKER IMAGE
@test "DOCKER IMAGE BUILD" {
    run docker build -t uls:bats .
    [ "$status" -eq 0 ]
}

## RUN AN EAA TEST
@test "DOCKER EAA TEST" {
    run timeout ${uls_timeout_params} docker run --rm --name "uls-bats-test" --mount type=bind,source="${uls_edgerc}",target="/opt/akamai-uls/.edgerc",readonly uls:bats --section ${uls_section} --input eaa --feed access --output raw --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #[ "$status" -eq 0 ]
}

## RUN AN ETP TEST
@test "DOCKER ETP TEST" {
    run timeout ${uls_timeout_params} docker run --rm --name "uls-bats-test" --mount type=bind,source="${uls_edgerc}",target="/opt/akamai-uls/.edgerc",readonly uls:bats --section ${uls_section} --input etp --feed threat --output raw --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #[ "$status" -eq 0 ]
}

## RUN AN MFA TEST
@test "DOCKER MFA TEST" {
    run timeout ${uls_timeout_params} docker run --rm --name "uls-bats-test" --mount type=bind,source="${uls_edgerc}",target="/opt/akamai-uls/.edgerc",readonly uls:bats --section ${uls_section} --input mfa --feed event --output raw --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #[ "$status" -eq 0 ]
}

## RUN AN GC TEST
@test "DOCKER GC TEST" {
    run timeout ${uls_timeout_params} docker run --rm --name "uls-bats-test" --mount type=bind,source="${uls_edgerc}",target="/opt/akamai-uls/.edgerc",readonly uls:bats --section ${uls_section} --input gc --feed netlog --output raw --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #[ "$status" -eq 0 ]
}

## REMOVE the local DOCKER IMAGE
@test "DOCKER IMAGE BUILD" {
    docker image rm uls:bats
    [ "$status" -eq 0 ]
}