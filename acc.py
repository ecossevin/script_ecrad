import re
import sys



#def extract_code_between_directives(lines):
#    in_region = False
#    extracted_code = []
#
#    for line in lines:
#        if "#ifdef _OPENAC" in line:
#            in_region = True
#        elif "#else" in line:
#            in_region = False
#        elif "#endif" in line:
#            in_region = False
#        elif in_region:
#            extracted_code.append(line.strip())
#
#    return extracted_code

def remove_ifdef_contains(input_file, output_file):
#    pattern = r'^\s*contains\s*$'
    verbose=False
#    number_contains=0
    with open(input_file, 'r') as f_in:
        lines = f_in.readlines()
#    for line in lines:
#        #if "contains" in line:
#        if re.match(pattern, line):
#            number_contains+=1 
#            if verbose: print(line)
#        if number_contains    

    for line in lines:
        if "#ifdef _OPENACC" in line:
            inside_openacc_block = True
        if inside_openacc_block and "use" in line:
            if verbose: print(line)
        if inside_openacc_block and "procedure" in line:
            if verbose: print(line)
        
    
def modify_acc_to_acc_if(input_file, output_file):
#https://www.openacc.org/sites/default/files/inline-files/OpenACC_2_0_specification.pdf
    verbose=False
    #verbose=True
    pragmas=["PARALLEL","KERNELS","DATA","UPDATE"]
    print("==>", input_file, "<==")
    with open(input_file, 'r') as f_in:
        lines = f_in.readlines()

    modified_lines = []

    inside_openacc_block = False

    for line in lines:
        if "#ifdef _OPENACC" in line:
            line="IF(LACC) THEN"
            inside_openacc_block = True
            modified_lines.append(line)
            continue

        if "#else" in line and inside_openacc_block:
            line="ELSE"
            modified_lines.append(line)
            continue

        
        if "#if" in line and inside_openacc_block:
            print("================================================")
            print("if nested inside open acc ifdef")
            print("================================================")

        if "#endif" in line:
            line="END IF"
            inside_openacc_block = False
            modified_lines.append(line)
            continue
        
        num_pragma=0
        if not inside_openacc_block:
            for pragma in pragmas:
                if pragma in line:
                    if verbose: print("line =", line)
                    num_pragma=num_pragma+1
                    if num_pragma>1:
                        print("more than one pragma item on that line")
                    line = line.replace(pragma, pragma+" IF(LACC)")

        modified_lines.append(line)

    with open(output_file, 'w') as f_out:
        f_out.writelines(modified_lines)

input_file=sys.argv[1]
#output_file=sys.argv[2]
output_file=input_file
#modify_acc_to_acc_if(input_file, output_file)
remove_ifdef_contains(input_file, output_file)

#with open("test.cpp", "r") as file:
#    lines = file.readlines()
#    code = extract_code_between_directives(lines)
#    for line in code:
#        print(line)
