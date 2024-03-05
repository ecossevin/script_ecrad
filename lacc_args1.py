import re
import os
import sys

#SUBROUTINE\s+([a-zA-Z_0-9&]+)
#sub_name=match.group(1)
#sub_body=

pattern_sub="SUBROUTINE(.*?)END SUBROUTINE"
pattern_name="SUBROUTINE[\s&]+([a-zA-Z_0-9&]+)\("
#pattern_new="SUBROUTINE[\s&]+[a-zA-Z0-9_]*(\([a-zA-Z0-9_%&\s:,\(\)]*\))"
pattern_new="SUBROUTINE[\s&]+[a-zA-Z0-9_]*(\((?:(?!(END SUBROUTINE|USE|IMPLICIT NONE))[a-zA-Z0-9_%&\s:,\(\)])*\))"

def is_sub_lacc(code):
    verbose=True
#    verbose=False
    code_new=code
    while True:
        match_sub=re.search(pattern_sub, code, re.DOTALL)
        if match_sub: 
            sub=match_sub.group(0)
            sub_body=match_sub.group(1)
            if verbose: print("sub_body = ", sub_body)
            if verbose: print("sub = ", sub)
            if re.search(r'(ACC|OPENACC)', sub_body, re.IGNORECASE): #!$ACC or #ifdef _OPENACC 
                sub_name=re.search(pattern_name, sub, re.IGNORECASE).group(1)
                sub_param=re.search(pattern_new, sub, re.IGNORECASE|re.DOTALL).group(1)
                sub_param_new=sub_param[:-1]+", LACC)"
                code_new=code_new.replace(sub_param, sub_param_new)   #we assume that # two diff subroutines same args
                if verbose: print("sub_param = ", sub_param)
                if verbose: print("sub_name = ", sub_name)
#                sub_new=re.replace(sub,
                sub_lacc.append(sub_name)      
            if verbose: print("match sub body = ", sub_body)
            code=code.replace(sub, "")
        else:
            break
    
    return(sub_lacc, code_new)
def is_sub_lacc(code):
    verbose=True
    for line in code:
        

             
def process_file(input_file):
    print("==>", input_file, "<==")
    with open(input_file, 'r') as f:
        content=f.read()

    sub_lacc, code_new=is_sub_lacc(content)
    new_content=code_new 
    with open(input_file, 'w') as f:
        f.write(new_content)
    


def parcourir_repertoire(repertoire):
    # Parcours de tous les fichiers et répertoires dans le répertoire spécifié
    for nom_fichier in os.listdir(repertoire):
        chemin_fichier = os.path.join(repertoire, nom_fichier)
        if os.path.isdir(chemin_fichier):
            # Si c'est un répertoire, on le parcourt récursivement
            parcourir_repertoire(chemin_fichier)

        elif nom_fichier.endswith('.F90'):
            # Si c'est un fichier se terminant par .F90, on effectue une action
            
#            print("==>", chemin_fichier, "<==")
            process_file(chemin_fichier)



#loop file
debug=True
#debug=False
#
if debug:
#    input_file=
#    print("==>", input_file, "<==")
#    with open(input_file, 'r') as f:
#        content=f.read()
    content="""
    SUBROUTINE &
    & A(DSFFDSD, SDF SDFSFSFS )

    ACC

    END SUBROUTINE
    TEST()

    SUBROUTINE &
    & A(DSFFDSD, SDF SDFSFSFS )

    totD KFDSNKJDFSDKJBF SJHDBF

    END SUBROUTINE


    """
    sub_lacc=[]
    sub_lacc, code_new=is_sub_lacc(content)
    print(sub_lacc)
    print(code_new)
    with open("sub_lacc.txt", "w") as file:
        for sub in sub_lacc:
            file.write("%s\n" % item)
if not debug:
     # Chemin du répertoire racine à partir duquel commencer la recherche
    repertoire_racine = sys.argv[1]
    
    # Appel de la fonction pour parcourir récursivement les fichiers
    parcourir_repertoire(repertoire_racine)
    
   
