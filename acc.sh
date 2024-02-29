#!/bin/bash

bin_path="/perm/rma1/ecrad/bin"
find $1 -type f -name "*.F90" -print0 | xargs -0 -I {} python3 "$bin_path/acc.py" {}

