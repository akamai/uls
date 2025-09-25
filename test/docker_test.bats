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

REPO_NAME="uls-bats"
TAG_DEBIAN="debian"
TAG_ALPINE="alpine"

# Stop potentially running containers
#docker stop uls-bats-test-debian-eaa || docker stop uls-bats-test-debian-etp || docker stop uls-bats-test-debian-mfa || docker stop uls-bats-test-debian-gc || true
#docker stop uls-bats-test-alpine-eaa || docker stop uls-bats-test-alpine-etp || docker stop uls-bats-test-alpine-mfa || docker stop uls-bats-test-alpine-gc || true

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
    for id in $(docker ps -f name=uls-bats-test -q) ; do docker stop $id ; done
    for id in $(docker image ls -f ${REPO_NAME} -q) ; do docker image rm $id ; done
    return 0
}


## Make sure, versions allign
@test "[BOTH] Check Version allignment in both dockerfiles" {
    run diff <(cat Dockerfile | grep "ARG" | grep "VERSION") <(cat Dockerfile_debian | grep "ARG" | grep "VERSION")
    [ "$status" -eq 0 ]
}

# --- DEBIAN from here downwards

## CREATE a local DOCKER IMAGE (DEBIAN)
@test "[DEBIAN] DOCKER IMAGE BUILD - DEBIAN" {
    run docker build --pull -t ${REPO_NAME}:${TAG_DEBIAN} --file Dockerfile_debian .
    [ "$status" -eq 0 ]
}

## Test container security posture
@test "[DEBIAN] DOCKER SECURITY SCAN 1 (scout)" {
    run docker scout cves --only-fixed ${REPO_NAME}:${TAG_DEBIAN}
    [ "$status" -eq 0 ]
}

## Test container security posture
@test "[DEBIAN] DOCKER SECURITY SCAN 2 (trivy)" {
    run trivy image ${REPO_NAME}:${TAG_DEBIAN} --ignore-unfixed
    [ "$status" -eq 0 ]
}

## RUN AN EAA TEST
@test "[DEBIAN] DOCKER EAA TEST" {
    run timeout ${uls_timeout_params} docker run --rm --name "uls-bats-test-debian-eaa" --mount type=bind,source="${uls_edgerc}",target="/opt/akamai-uls/.edgerc",readonly ${REPO_NAME}:${TAG_DEBIAN} --section ${uls_section} --input eaa --feed access --output raw --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #[ "$status" -eq 0 ]
}

## RUN AN ETP TEST
@test "[DEBIAN] DOCKER ETP TEST" {
    run timeout ${uls_timeout_params} docker run --rm --name "uls-bats-test-debian-etp" --mount type=bind,source="${uls_edgerc}",target="/opt/akamai-uls/.edgerc",readonly ${REPO_NAME}:${TAG_DEBIAN} --section ${uls_section} --input etp --feed threat --output raw --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #[ "$status" -eq 0 ]
}

## RUN AN MFA TEST
@test "[DEBIAN] DOCKER MFA TEST" {
    run timeout ${uls_timeout_params} docker run --rm --name "uls-bats-test-debian-mfa" --mount type=bind,source="${uls_edgerc}",target="/opt/akamai-uls/.edgerc",readonly ${REPO_NAME}:${TAG_DEBIAN} --section ${uls_section} --input mfa --feed event --output raw --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #[ "$status" -eq 0 ]
}

## RUN AN GC TEST
@test "[DEBIAN] DOCKER GC TEST" {
    run timeout ${uls_timeout_params} docker run --rm --name "uls-bats-test-debian-gc" --mount type=bind,source="${uls_edgerc}",target="/opt/akamai-uls/.edgerc",readonly ${REPO_NAME}:${TAG_DEBIAN} --section ${uls_section} --input gc --feed netlog --output raw --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #[ "$status" -eq 0 ]
}

## STOP potentially running images
#@test "[DEBIAN] Stopping everything" {
#    run docker stop uls-bats-test-debian-eaa ; docker stop uls-bats-test-debian-etp ; docker stop uls-bats-test-debian-mfa ; docker stop uls-bats-test-debian-gc
#    #[ "$status" -eq 0 ]
#}

## REMOVE the local DOCKER IMAGE
@test "[DEBIAN] DOCKER IMAGE DELETE" {
    run docker image rm ${REPO_NAME}:${TAG_DEBIAN}
    [ "$status" -eq 0 ]
}


# --- ALPINE from here downwards

## CREATE a local DOCKER IMAGE (ALPINE)
@test "[ALPINE] DOCKER IMAGE BUILD - " {
    run docker build --pull -t ${REPO_NAME}:${TAG_ALPINE} -f Dockerfile .
    [ "$status" -eq 0 ]
}

## Test container security posture
@test "[ALPINE] DOCKER SECURITY SCAN 1 (scout)" {
    run docker scout cves --only-fixed ${REPO_NAME}:${TAG_ALPINE}
    [ "$status" -eq 0 ]
}

## Test container security posture
@test "[ALPINE] DOCKER SECURITY SCAN 2 (trivy)" {
    run trivy image ${REPO_NAME}:${TAG_ALPINE} --ignore-unfixed
    [ "$status" -eq 0 ]
}

## RUN AN EAA TEST
@test "[ALPINE] DOCKER EAA TEST" {
    run timeout ${uls_timeout_params} docker run --rm --name "uls-bats-test-alpine-eaa" --mount type=bind,source="${uls_edgerc}",target="/opt/akamai-uls/.edgerc",readonly ${REPO_NAME}:${TAG_ALPINE} --section ${uls_section} --input eaa --feed access --output raw --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #[ "$status" -eq 0 ]
}

## RUN AN ETP TEST
@test "[ALPINE] DOCKER ETP TEST" {
    run timeout ${uls_timeout_params} docker run --rm --name "uls-bats-test-alpine-etp" --mount type=bind,source="${uls_edgerc}",target="/opt/akamai-uls/.edgerc",readonly ${REPO_NAME}:${TAG_ALPINE} --section ${uls_section} --input etp --feed threat --output raw --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #[ "$status" -eq 0 ]
}

## RUN AN MFA TEST
@test "[ALPINE] DOCKER MFA TEST" {
    run timeout ${uls_timeout_params} docker run --rm --name "uls-bats-test-alpine-mfa" --mount type=bind,source="${uls_edgerc}",target="/opt/akamai-uls/.edgerc",readonly ${REPO_NAME}:${TAG_ALPINE} --section ${uls_section} --input mfa --feed event --output raw --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #[ "$status" -eq 0 ]
}

## RUN AN GC TEST
@test "[ALPINE] DOCKER GC TEST" {
    run timeout ${uls_timeout_params} docker run --rm --name "uls-bats-test-alpin-gc" --mount type=bind,source="${uls_edgerc}",target="/opt/akamai-uls/.edgerc",readonly ${REPO_NAME}:${TAG_ALPINE} --section ${uls_section} --input gc --feed netlog --output raw --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #[ "$status" -eq 0 ]
}

## REMOVE the local DOCKER IMAGE
@test "[ALPINE] DOCKER IMAGE DELETE" {
    run docker image rm ${REPO_NAME}:${TAG_ALPINE}
    [ "$status" -eq 0 ]
}