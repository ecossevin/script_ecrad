#!/bin/bash

bin_path="/perm/rma1/ecrad/bin"
#find $1 -type f -name "*.F90" -print0 | xargs -0 -I {} python3 "$bin_path/acc.py" {}
excluded_files=("lacc_mod.F90" "rrtm_taumol1.F90" "rrtm_taumol10.F90" "rrtm_taumol11.F90" "rrtm_taumol12.F90" "rrtm_taumol14.F90" "rrtm_taumol13.F90" "rrtm_taumol15.F90" "rrtm_taumol16.F90" "rrtm_taumol2.F90" "rrtm_taumol3.F90" "rrtm_taumol7.F90" "rrtm_taumol6.F90" "rrtm_taumol8.F90" "rrtm_taumol5.F90" "rrtm_taumol4.F90" "rrtm_taumol9.F90")

find $1 -type f \( -name "*.F90" ! -name "lacc_mod.F90" ! -name "rrtm_taumol1.F90" ! -name "rrtm_taumol10.F90" ! -name "rrtm_taumol11.F90" ! -name "rrtm_taumol12.F90" ! -name "rrtm_taumol14.F90" ! -name "rrtm_taumol13.F90" ! -name "rrtm_taumol15.F90" ! -name "rrtm_taumol16.F90" ! -name "rrtm_taumol2.F90" ! -name "rrtm_taumol3.F90" ! -name "rrtm_taumol7.F90" ! -name "rrtm_taumol6.F90" ! -name "rrtm_taumol8.F90" ! -name "rrtm_taumol5.F90" ! -name "rrtm_taumol4.F90" ! -name "rrtm_taumol9.F90" \) -print0 | xargs -0 -I {} python3 "$bin_path/acc.py" {}
###

