#!/bin/bash

bin_path="/perm/rma1/ecrad/bin"
find $1 -type f \( -name "*.F90" ! -name "parkind1.F90" ! -name "yommp0.F90" \) -print0 | xargs -0 -I {} python3 "$bin_path/use.py" {}
#find $1 -type f -name "*.F90" -print0 | xargs -0 -I {} python3 "$bin_path/use.py" {}

