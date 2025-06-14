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


#  POSITIVE tests
## EAA
#@test "EAA - ACCESS" {
#    run timeout  --kill-after=$uls_kill_timeout --signal=2 --preserve-status $uls_test_timeout  $uls_bin --input eaa --feed access --output raw --edgerc $uls_edgerc --section $uls_section
#    assert_output --partial $eaa_access_assert
#    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
#    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
#    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 2 ]        #return value from uls when interrupted --> with --preserve status on timeout
#}

@test "EAA - ACCESS" {
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed access --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output --partial $eaa_access_assert
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

@test "EAA - ADMIN" {
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed admin --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output --partial ""
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}
@test "EAA - CONHEALTH" {
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed admin --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output ""
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]         #return value from uls when interrupted --> with --preserve status on timeout
}
@test "EAA - DEVINV" {
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed devinv --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output --partial $eaa_devinv_assert
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

@test "EAA - DIRHEALTH" {
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed dirhealth --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output --partial $eaa_devinv_assert
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}


## ETP
@test "ETP - THREAT" {
    run timeout ${uls_timeout_params} ${uls_bin} --input etp --feed threat --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output --partial $etp_assert
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

@test "ETP - AUP" {
    run timeout ${uls_timeout_params} ${uls_bin} --input etp --feed aup --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output --partial $etp_assert
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]         #return value from uls when interrupted --> with --preserve status on timeout
}

@test "ETP - DNS" {
    run timeout ${uls_timeout_params} ${uls_bin} --input etp --feed dns --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output --partial $etp_assert
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

@test "ETP - PROXY" {
    run timeout ${uls_timeout_params} ${uls_bin} --input etp --feed proxy --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output --partial $etp_assert
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

@test "ETP - NETCON" {
    run timeout ${uls_timeout_params} ${uls_bin} --input etp --feed netcon --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output --partial $etp_assert
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}


## SIA (ALIAS TO ETP)
@test "SIA - DNS" {
    run timeout ${uls_timeout_params} ${uls_bin} --input sia --feed dns --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output --partial $etp_assert
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

@test "SIA - THREAT" {
    run timeout ${uls_timeout_params} ${uls_bin} --input sia --feed threat --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

@test "SIA - AUP" {
    run timeout ${uls_timeout_params} ${uls_bin} --input sia --feed aup --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

#@test "SIA - PROXY" {
#    run timeout ${uls_timeout_params} ${uls_bin} --input sia --feed proxy --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
#    assert_line --partial "UlsInputCli - started PID"
#    refute_line --partial "was found stale -"
#    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
#}

@test "SIA - NETCON" {
    run timeout ${uls_timeout_params} ${uls_bin} --input sia --feed netcon --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

## MFA
@test "MFA - EVENT" {
    run timeout ${uls_timeout_params} ${uls_bin} --input mfa --feed event --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output ""
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

## GUARDICORE
@test "GC - NETLOG" {
    run timeout ${uls_timeout_params} ${uls_bin} --input gc --feed netlog --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output --partial $gc_assert
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]         #return value from uls when interrupted --> with --preserve status on timeout
}

@test "GC - INCIDENT" {
    run timeout ${uls_timeout_params} ${uls_bin} --input gc --feed incident --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]         #return value from uls when interrupted --> with --preserve status on timeout
}

@test "GC - AGENT" {
    run timeout ${uls_timeout_params} ${uls_bin} --input gc --feed agent --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]         #return value from uls when interrupted --> with --preserve status on timeout
}

@test "GC - SYSTEM" {
    run timeout ${uls_timeout_params} ${uls_bin} --input gc --feed system --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]         #return value from uls when interrupted --> with --preserve status on timeout
}

@test "GC - AUDIT" {
    run timeout ${uls_timeout_params} ${uls_bin} --input gc --feed audit --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]         #return value from uls when interrupted --> with --preserve status on timeout
}

## LINODE
@test "LINODE - AUDIT" {
    run timeout ${uls_timeout_params} ${uls_bin} --input linode --feed audit --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output --partial ""
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

@test "LINODE - UTILIZATION" {
    run timeout ${uls_timeout_params} ${uls_bin} --input linode --feed utilization --output raw --edgerc $uls_edgerc --section $uls_section --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

## ACC-LOGS
@test "ACC - EVENTS" {
    run timeout ${uls_timeout_params} ${uls_bin} --input acc --feed events --output raw --edgerc $uls_edgerc --loglevel info
    #assert_output --partial $gc_assert
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]         #return value from uls when interrupted --> with --preserve status on timeout
}

# --------------------
# End feed testes

#---------------------
# Functional Tests

## FILE OUTPUT
@test "FILE: ETP - THREAT" {
    run timeout ${uls_timeout_params} ${uls_bin} --input etp --feed threat --output file --filename "/tmp/uls_tmplogfile1.log" --edgerc $uls_edgerc --section $uls_section --loglevel info
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
    rm -fr /tmp/uls_tmplogfile.log
}

@test "FILEACTION: ETP - THREAT" {
    run timeout ${uls_timeout_params} ${uls_bin} --input etp --feed threat --output file --filename "/tmp/uls_tmplogfile2.log" --filebackup 1 --fileaction "/bin/zip '%s'" --edgerc $uls_edgerc --section $uls_section --loglevel info
    #assert_output --partial ""
    assert_line --partial "UlsInputCli - started PID"
    refute_line --partial "was found stale -"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]         #return value from uls when interrupted --> with --preserve status on timeout
    rm -fr /tmp/uls_tmplogfile.log
}

## Transformation
@test "TRANSFORM - MCAS" {
    run timeout ${uls_timeout_params} ${uls_bin} --input etp --feed dns --output raw --transformation mcas --edgerc $uls_edgerc --section $uls_section
    assert_output --partial "detection_time"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

@test "TRANSFORM - JMESPATH" {
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed access --output raw --transformation jmespath --transformationpattern '[geo_country, geo_state]' --edgerc $uls_edgerc --section $uls_section
    assert_output --partial $jmespath_assert
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ] || [ "$status" -eq 137 ]        #return value from uls when interrupted --> with --preserve status on timeout
}

## AUTORESUME
@test "AUTORESUME - Create File" {
    rm -f /tmp/uls_eaa_access.ckpt
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed access --output raw --edgerc $uls_edgerc --section $uls_section --autoresume --autoresumepath /tmp/
    assert_output --partial $eaa_access_assert
    #assert_output --partial " seems to be empty"
    #assert_output --partial "The specified directory tmp does not exist or privileges are missing - exiting"
    #[ "$status" -eq 124 ]      #return value from timeout without --preserve status
    [ "$status" -eq 100 ] || [ "$status" -eq 130 ]  || [ "$status" -eq 137 ]       #return value from uls when interrupted --> with --preserve status on timeout
    rm -f /tmp/uls_eaa_access.ckpt
}

## OUTPUTFORMAT SUBSITUTION
@test "OUTPUTFORMAT SUBSITUTION" {
    export BATS_VAR="BATSTEST123"
    run timeout ${uls_timeout_params} ${uls_bin} --input eaa --feed access --output tcp --host 127.0.0.1 --port 1234 --edgerc $uls_edgerc --section $uls_section --loglevel debug --tcpudpformat '$BATS_VAR - {api_hostname} %s'
    assert_output --partial "OS_ENV_VARS new TCPUDP output string: BATSTEST123 - manage.akamai-access.com %s"
    unset BATS_VAR
}

## JSON LOGGING
@test "JSON Logging test - unmodified logline" {
   run timeout 5 ${uls_bin} --section ${uls_section} --input etp --feed dns --output raw --loglevel debug --json-log
   assert_output --partial '"log_level": "DEBUG", "component": "ULS", "message": "UlsMonitoring monitoring thread started..."'
}

@test "JSON Logging test - modified logline" {
   run timeout 5 ${uls_bin} --section ${uls_section} --input etp --feed dns --output raw --loglevel debug --json-log --ulslogformat '{"timestamp": "%(asctime)s", "log_level": "%(levelname)s", "component": "%(name)s", "message": "%(message)s", "ulsrocks": "yes"}'
   assert_output --partial '"log_level": "DEBUG", "component": "ULS", "message": "UlsMonitoring monitoring thread started...", "ulsrocks": "yes"'
}

## Prometheus
@test "PROMETHEUS - starting test" {
   run timeout 5 ${uls_bin} --section ${uls_section} --input etp --feed dns --output raw --loglevel debug --prometheus
   assert_output --partial 'DEBUG UlsMonitoring Prometheus monitoring started...'
}

## CLIDEBUG
@test "CLIDEBUG - starting test" {
   run timeout 5 ${uls_bin} --section ${uls_section} --input etp --feed dns --output raw --loglevel debug --clidebug
   assert_output --partial 'CLIDEBUG has been enabled, beside the loglines, you will also see debug information from the underlying CLI'
}


## HELM LINT
@test "LINT the HELM CHART" {
    run helm lint docs/examples/kubernetes/helm/akamai-uls --strict
    assert_output --partial "0 chart(s) failed"
    [ "$status" -eq 0 ]       #return value for Chart Lint: 0
}

