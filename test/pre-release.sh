#!/bin/bash

# Run this before every relaese to verify versions are inline
echo -ne "CONFIG: \t\t"
cat bin/config/global_config.py | grep "__version__ =" | cut -d " " -f 3
echo -ne "CHANGELOG: \t\t"
cat docs/CHANGELOG.md | grep "##" | head -n 1 | cut -d "v" -f 2
echo -ne "HELM App Version: \t"
cat docs/examples/kubernetes/helm/akamai-uls/Chart.yaml | grep "appVersion:" | cut -d " " -f 2
echo -ne "HELM Chart Version: \t"
cat docs/examples/kubernetes/helm/akamai-uls/Chart.yaml | grep "version:" | cut -d " " -f 2
echo -ne "K8s deployment Version: \t"
cat docs/examples/kubernetes/helm/akamai-uls/values.yaml | egrep "^\W+tag:"