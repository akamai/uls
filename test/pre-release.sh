#!/bin/bash
echo -ne "CONFIG: \t\t"
cat bin/config/global_config.py | grep "__version__ =" | cut -d " " -f 3
echo -ne "CHANGELOG: \t\t"
cat docs/CHANGELOG.md | grep "##" | head -n 1 | cut -d "v" -f 2
