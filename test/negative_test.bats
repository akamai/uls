#!/usr/bin/env bats


# Variables
    # ULS Binary
uls_bin=bin/uls.py


# Load support libs
load 'test/bats/bats-support/load.bash'
load 'test/bats/bats-assert/load.bash'



# Negative tests (failure responses expected)
## Basic negative testes
@test "Checking -i mfa standalone" {
    run  $uls_bin --input mfa
    assert_output --partial "Required argument / ENV var not set: OUTPUT"
    [ "$status" -eq 1 ]
}
@test "Checking --input eaa standalone" {
    run  $uls_bin --input eaa
    assert_output --partial "Required argument / ENV var not set: OUTPUT"
    [ "$status" -eq 1 ]
}
@test "Input / Feed mismatch" {
    run  $uls_bin --input eaa --feed auth -o raw
    assert_output --partial "Feed (AUTH) not available - Available: ['ACCESS', 'ADMIN', 'CONHEALTH']"
    [ "$status" -eq 1 ]
}
@test "Checking --feed and --intput etp" {
    run  $uls_bin --input etp --feed threat
    assert_output --partial "Required argument / ENV var not set: OUTPUT"
    [ "$status" -eq 1 ]
}
@test "Nonexistent edgerc" {
    run  $uls_bin  -i eaa -f access -o raw --edgerc /non/existent/edge/rc.rrrrcccc
    assert_output --partial "Config file '/non/existent/edge/rc.rrrrcccc' could not be loaded. - Exiting."
    [ "$status" -eq 1 ]
}
@test "Nonexistent edgerc section" {
    run  $uls_bin  -i eaa -f access -o raw --section definatelynonexitentsection
    assert_output --partial "not found. Available sections:"
    [ "$status" -eq 1 ]
}

## TCP
@test "TCP output failure (no host/no port)" {
    run  $uls_bin -i eaa -f access -o tcp
    assert_output --partial "Host or Port has not been set Host: None Port: 0"
    [ "$status" -eq 1 ]
}
@test "TCP output failure (no host)" {
    run  $uls_bin --input eaa -f access --output tcp --port 2222
    assert_output --partial "Host or Port has not been set Host: None Port: 2222"
    [ "$status" -eq 1 ]
}
@test "TCP output failure (no port)" {
    run  $uls_bin --input eaa -f access --output tcp --host 127.0.0.1
    assert_output --partial "Host or Port has not been set Host: 127.0.0.1 Port: 0"
    [ "$status" -eq 1 ]
}
@test "TCP output failure (tcp host / port unrrachable)" {
    run  $uls_bin  --input eaa -f access -o tcp --host 127.0.0.1 --port 7777
    assert_output --partial " UlsOutput not able to connect to 127.0.0.1:7777 - giving up after 10 retries."
    [ "$status" -eq 1 ]
}


## UDP
@test "UDP output failure (no host/no port)" {
    run  $uls_bin -i eaa -f access -o udp
    assert_output --partial "Host or Port has not been set Host: None Port: 0"
    [ "$status" -eq 1 ]
}
@test "UDP output failure (no host)" {
    run  $uls_bin --input eaa -f access --output udp --port 2222
    assert_output --partial "Host or Port has not been set Host: None Port: 2222"
    [ "$status" -eq 1 ]
}
@test "UDP output failure (no port)" {
    run  $uls_bin --input eaa -f access --output udp --host 127.0.0.1
    assert_output --partial "Host or Port has not been set Host: 127.0.0.1 Port: 0"
    [ "$status" -eq 1 ]
}
@test "UDP output failure (tcp host / port unreachable)" {
    # UDP won't fail as it is "stateless"
    skip "UDP won't fail as it is stateless"
    run  $uls_bin  --input eaa -f access -o udp --host 127.0.0.1 --port 7777
    assert_output --partial " UlsOutput not able to connect to 127.0.0.1:7777 - giving up after 10 retries."
    [ "$status" -eq 1 ]
}


## HTTP
@test "HTTP output failure (-o http)" {
    run  $uls_bin -i mfa -f auth --output http
    assert_output --partial "http_out_format http_out_auth_header http_url or http_insecure missing- exiting"
    [ "$status" -eq 1 ]
}
@test "HTTP output failure (httpurl unreachable)" {
    run  $uls_bin -i eaa -f access -o http --httpurl https://127.0.0.1:7777
    assert_output --partial " UlsOutput not able to connect to https://127.0.0.1:7777 - giving up after 10 retries."
    [ "$status" -eq 1 ]
}


## FILE
@test "FILE output failure (-o file)" {
    run  $uls_bin --input eaa --feed access -o file
    assert_output --partial "file-output was specified, but no file was specified. Please use --filename <filename> to specify a file"
    [ "$status" -eq 1 ]
}
@test "FILE output failure (-o file --filename /non/existent/dir/ec/tory/test.log )" {
    run  $uls_bin --input eaa --feed access -o file --filename /non/existent/dir/ec/tory/test.log
    assert_output --partial " The specified directory /non/existent/dir/ec/tory does not exist or privileges are missing - exiting."
    [ "$status" -eq 1 ]
}


## TRANSFORMATIONS
@test "TRANSFORM - MCAS wrong input" {
    run  $uls_bin --input eaa --feed dns --output raw --transformation mcas
    assert_output --partial "transformation Microsoft Cloud Applican Security [MCAS] specified, but wrong input/feed or format defined. MCAS only supports Input: ['ETP'] Feed: ['PROXY', 'DNS'] Cliformat: ['JSON'] - (exiting)"
    [ "$status" -eq 1 ]
}
@test "TRANSFORM - MCAS wrong feed" {
    run  $uls_bin --input etp --feed aup --output raw --transformation mcas
    assert_output --partial "transformation Microsoft Cloud Applican Security [MCAS] specified, but wrong input/feed or format defined. MCAS only supports Input: ['ETP'] Feed: ['PROXY', 'DNS'] Cliformat: ['JSON'] - (exiting)"
    [ "$status" -eq 1 ]
}
@test "TRANSFORM - MCAS wrong format (txt)" {
    run  $uls_bin --input etp --feed aup --output raw --transformation mcas --format text
    assert_output --partial "transformation Microsoft Cloud Applican Security [MCAS] specified, but wrong input/feed or format defined. MCAS only supports Input: ['ETP'] Feed: ['PROXY', 'DNS'] Cliformat: ['JSON'] - (exiting)"
    [ "$status" -eq 1 ]
}

@test "TRANSFORM - JMESPATH empty pattern" {
    run  $uls_bin --input eaa --feed access --output raw --transformation jmespath --transformationpattern ""
    assert_output --partial " transformation JMESPath https://jmespath.org/ [JMESPATH] specified, but wrong params given format defined. (Inputformat/pattern)JMESPath only supports Cliformat: ['JSON'] Transformation pattern given:  - (exiting)"
    [ "$status" -eq 1 ]
}

@test "TRANSFORM - JMESPATH TEXT format" {
    run  $uls_bin --input eaa --feed access --output raw --transformation jmespath --transformationpattern "asd" --format text
    assert_output --partial " transformation JMESPath https://jmespath.org/ [JMESPATH] specified, but wrong params given format defined. (Inputformat/pattern)JMESPath only supports Cliformat: ['JSON'] Transformation pattern given: asd - (exiting)"
    [ "$status" -eq 1 ]
}

### Autoresume
@test "AUTORESUME - inacessible path" {
    run  $uls_bin --input etp --feed threat --output raw --autoresume --autoresumepath /blabla/blabla
    assert_output --partial " [Errno 2] No such file or directory:"
    [ "$status" -eq 1 ]
}

