import re
import sys


def dernier_caractere_non_espace(chaine):
    match = re.search(r' [ \n]*[^ \n]', chaine[::-1])
    #match = re.search(r'[^ \n](?=[ \n]*$)', chaine[::-1])
    if match:
        return match.group()
    else:
        return None



#chaine = "aaab d &  \n"
#print(chaine[::-1])
#dernier = dernier_caractere_non_espace(chaine)
#if dernier:
#    print("Le dernier caractère non espace ou retour à la ligne est :", dernier)
#else:
#    print("Il n'y a pas de dernier caractère non espace ou retour à la ligne dans la chaîne.")
#
   
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
            line="IF(LACC) THEN\n"
            inside_openacc_block = True
            modified_lines.append(line)
            continue

        if "#else" in line and inside_openacc_block:
            line="ELSE\n"
            modified_lines.append(line)
            continue

        
        if "#if" in line and inside_openacc_block:
            print("================================================")
            print("if nested inside open acc ifdef")
            print("================================================")

        if "#endif" in line and inside_openacc_block:
            line="END IF\n"
            inside_openacc_block = False
            modified_lines.append(line)
            continue
        
        num_pragma=0
        if not inside_openacc_block:
            for pragma in pragmas:
                if ("!$OMP" not in line and "!$ACC" in line):
#                if "!$OMP" not in line:
                    if (pragma in line and not ("LACC" in line or "END" in line or "IF(" in line or "from PROF" in line)): #not LACC = not LACC and not LLACC
                        if "LOOP" in line:
                            line = line.replace("\n", " IF(LACC)\n")
#                            line.replace(
                        else:
                            line = line.replace(pragma, pragma+" IF(LACC)")
#                        if verbose: print("line =", line)
#                        num_pragma=num_pragma+1
#                        if num_pragma>1:
#                            print("more than one pragma item on that line")
#                        last_char = dernier_caractere_non_espace(line)
#                        if last_char == "&":
#                            line = line.replace("\n", "")
#                            line = line.replace("&", " IF(LACC)\n")
#                        else:
#                            line = line.replace("\n", " IF(LACC)\n")
#                    #    line = line + " IF(LACC)"

        modified_lines.append(line)

    with open(output_file, 'w') as f_out:
        f_out.writelines(modified_lines)

input_file=sys.argv[1]
#output_file=sys.argv[2]
output_file=input_file
modify_acc_to_acc_if(input_file, output_file)
#remove_ifdef_contains(input_file, output_file)

#with open("test.cpp", "r") as file:
#    lines = file.readlines()
#    code = extract_code_between_directives(lines)
#    for line in code:
#        print(line)
