#!/usr/bin/env bats

#BATS_NO_PARALLELIZE_WITHIN_FILE=true

# Variables
    # ULS Binary
uls_bin="bin/uls.py"

uls2_path="bin"
uls2_bin="uls.py"

# Load support libs
load 'bats/bats-support/load.bash'
load 'bats/bats-assert/load.bash'

uls_bin="bin/uls.py"
uls_edgerc=~/.edgerc
uls_section=default

current_version=$(cat docs/CHANGELOG.md | grep "##" | head -n 1 | sed 's/.* v//')


# very basic tests
@test "uls.py w/o parameters" {
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
	assert_output --partial "ULS DEBUG Logging initialized"
	[ "$status" -eq 1 ]
}

@test "uls.py --version - Version output should be ($current_version) according to CHANGELOG" {
	run $uls_bin --version
	assert_output --partial $current_version
	[ "$status" -eq 0 ]
}

@test "cat bin/config/global - Version output should be ($current_version) according to CHANGELOG" {
	run echo $(cat bin/uls_config/global_config.py | grep "__version__ =" | cut -d " " -f 3)
	assert_output --partial "$current_version"
	[ "$status" -eq 0 ]
}

#@test "cat docs/examples/kubernetes/helm/akamai-uls/Chart.yaml - Version output should be ($current_version) according to CHANGELOG" {
#	run echo $(cat docs/examples/kubernetes/helm/akamai-uls/Chart.yaml | egrep "^version:" | cut -d " " -f 2)
#	assert_output --partial "$current_version"
#	[ "$status" -eq 0 ]
#}

@test "cat docs/examples/kubernetes/helm/akamai-uls/Chart.yaml - appVersion output should be ($current_version) according to CHANGELOG" {
	run echo $(cat docs/examples/kubernetes/helm/akamai-uls/Chart.yaml | egrep "^appVersion:" | cut -d " " -f 2)
	assert_output --partial "$current_version"
	[ "$status" -eq 0 ]
}

@test "Helm Lint akamai-uls" {
  run helm lint docs/examples/kubernetes/helm/akamai-uls
  assert_output --partial "1 chart(s) linted, 0 chart(s) failed"
  [ "$status" -eq 0 ]
}

@test "Verify Docker file (hadolint)" {
  run hadolint Dockerfile
  [ "$status" -eq 0 ]
}