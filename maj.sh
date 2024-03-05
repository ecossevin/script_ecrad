#!/bin/bash

find $1 -type f -name "*.F90" -exec bash -c '
    apply_maj() {
    input_file=$1
    temp_file=$(mktemp)  
    echo "==> $1 <=="
    while IFS= read -r line || [[ -n $line ]]; do
        if [[ "$line" =~ \!\$acc ]]; then
            echo "${line^^}" >> "$temp_file"
        else
            echo "$line" >> "$temp_file"
        fi
    done < "$input_file"
    
    mv "$temp_file" "$input_file"
    }
    apply_maj "$0"
' {} \; 
