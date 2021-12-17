#!/usr/bin/env bats


# Variables
    # ULS Binary
uls_bin=bin/uls.py

uls2_path="bin"
uls2_bin=uls.py

# Load support libs
load 'test/bats/bats-support/load.bash'
load 'test/bats/bats-assert/load.bash'

uls_bin=bin/uls.py
uls_edgerc=~/.edgerc
uls_section=default

# very basic tests
@test "uls.py w/o parametes" {
	run $uls_bin
	[ "$status" -eq 1 ]
}

@test "uls.py --version" {
	run $uls_bin --version
	assert_output --partial "Akamai Unified Log Streamer Version information"
	[ "$status" -eq 0 ]
}

@test "uls.py --help" {
	run $uls_bin --help
	assert_output --partial "usage: uls.py [-h]"
	[ "$status" -eq 0 ]
}

@test "uls.py --loglevel debug" {
	run $uls_bin --loglevel debug
	assert_output --partial "ULS D Logging initialized"
	[ "$status" -eq 1 ]
}
