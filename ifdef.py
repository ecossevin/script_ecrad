import re
import sys

def replace(string):
    to_replace=["#ifdef _OPENACC", "#else", "#endif"]
    for line in to_replace:
        string=string.replace(line,"")
    return(string)

def remove_blocs_ifdef(code):
    verbose=False
    # Motif de recherche pour le bloc ifdef
    pattern_ifdef = r'#ifdef\s+_OPENACC(.*?)#endif'

    code_new=code
    while True:
    # Recherche et remplacement des blocs ifdef
        match_ifdef = re.search(pattern_ifdef, code, re.DOTALL)
        if match_ifdef:
            # Vérifier si le code contient les mots "use" ou "procedure"
            bloc_ifdef = match_ifdef.group(0)
            if verbose: print("bloc_ifdef=", bloc_ifdef)
            if re.search(r'\b(use|procedure)\b', bloc_ifdef, re.IGNORECASE):
            #if re.search(r'\b(use|procedure|subroutine)\b', bloc_ifdef, re.IGNORECASE):
                if verbose: print("bloc_ifdef MATCH=", bloc_ifdef)
                new_ifdef=replace(bloc_ifdef)
                code_new = code_new.replace(match_ifdef.group(0), new_ifdef)
                code=code.replace(match_ifdef.group(0), "")
            else:
                code=code=code.replace(match_ifdef.group(0), "")

        else:
            break

    return code_new

input_file=sys.argv[1]
output_file=input_file
print("==>", input_file, "<==")
# Lecture du content du fichier d'entrée
with open(output_file, 'r') as f:
    content = f.read()

# Application de la fonction remove_blocs_ifdef
new_content = remove_blocs_ifdef(content)

# Écriture du content modifié dans un nouveau fichier de sortie
with open(input_file, 'w') as f:
    f.write(new_content)
