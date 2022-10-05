# ULS test scripts

## BATS

We decided to go with [bats](https://bats-core.readthedocs.io/en/stable/) as it provides everything we need for automated cli testing.  
### 20221004
Added "Bats" parallel jobs funktion (requires GNU prallel to work) in order to speed up testes 



The bats job needs to get run from the GIT ULS root directory:
```bash
bash test/test.sh
```
For better testing stability, we packed the required dependencies into the test dir as well.

### Requirements

- [bats](https://bats-core.readthedocs.io/en/stable/) version 1.6 min
  ```
  bats --version
  Bats 1.6.0
  ```
- [bats-assert](https://github.com/ztombol/bats-assert.git) checked out under `bats` directory
- [bats-support](https://github.com/ztombol/bats-support.git) checked out under `bats` directory
- `timeout` command is available
- "GNU parallel" --> `brew install parallel`
- ULS and the CLI's are installed
- working (fully fledged `.edgerc` file - or the inline MOCKED one) 
  - mocked edgerc is currently failing with EAA
- helm isntallation (linting)


## Installation

```
cd test
mkdir bats
git clone https://github.com/ztombol/bats-assert.git
git clone https://github.com/ztombol/bats-support.git
```
