# ULS test scripts
## BATS
We decided to go with [bats](https://bats-core.readthedocs.io/en/stable/) as it provides everything we need for automated cli testing.
The bats job needs to get run from the git root directory:
```bash
bash test/test.sh
```
For better testing stability, we packed the required dependencies into the test dir as well.

### Requirements
- [bats](https://bats-core.readthedocs.io/en/stable/)
- timeout command is available
- uls and the cli's are installed
- working (fully fledged .edgerc file - not necessarily providing logs)