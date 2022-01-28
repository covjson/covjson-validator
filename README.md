# CoverageJSON Validator (Work In Progress)

This repo contains JSON schema and associated Python code for validating [CoverageJSON](https://covjson.org) documents.

## Setup
 1. Install a Python environment with pip (version x or above), e.g. using conda (`conda create -n covjson-validator pip`)
 2. Install requirements (`pip install -r requirements.txt`)

N.B. Make sure to install requirements via `pip`, not `conda` (at the time of writing the version of `jsonschema` in conda was too old to run the tests).

## Running the validator


## Testing the validator
```
pytest
```

A more thorough (and slow) test mode can be enabled by passing `--exhaustive` to pytest. For some tests, this increases the number of parameterizations against which a test is run. This mode is also used in Continuous Integration testing via GitHub Actions.

## Contents of this repository