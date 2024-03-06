import sys
import os


def compte_blocs_openacc(filename):
    compteur = 0
    ncompteur = 0
    nb_do1=0
    nb_do2=0
        #fichier=code.split("\n")

    with open(filename, 'r') as fichier:
        inside_openacc = False
        inside_nopenacc = False
        for ligne in fichier:

            if inside_nopenacc:
                if nb_do1<0 or nb_do2<0:
                    if not is_ncompt: 
                        is_ncompt=True
                        ncompteur += 1 
            if inside_openacc:
                if nb_do1<0 or nb_do2<0:
                    if not is_compt: 
                        is_compt=True
                        compteur += 1 

            if "#ifndef _OPENACC" in ligne:
                inside_nopenacc = True
                is_ncompt=False
            if "#ifdef _OPENACC" in ligne:
                inside_openacc = True
                is_compt=False

            if "#ifndef _OPENACC" in ligne or "#ifdef _OPENACC" in ligne:
                nb_do1=0
                nb_do2=0
                bloc=1
            if "#else" in ligne:
                nb_do2=0
                bloc=2 
            if inside_openacc or inside_nopenacc:
                if (("do" in ligne or "DO" in ligne) and ("END" not in ligne and "end" not in ligne)):
                    if bloc==1 : nb_do1+=1
                    if bloc==2 : nb_do2+=1
                if "enddo" in ligne or "end do" in ligne or "ENDDO" in ligne or "END DO" in ligne:
                    if bloc==1 : nb_do1-=1
                    if bloc==2 : nb_do2-=1

            if "#endif" in ligne:
                if nb_do1 != 0 or nb_do2 !=0:
                    if inside_openacc and not compteur:
                        compteur += 1
                    if inside_nopenacc and not ncompteur:
                        ncompteur += 1
                inside_openacc = False
                inside_nopenacc = False
                nb_do1=0
                nb_do2=0
            
                

    return (compteur, ncompteur)

def parcourir_repertoire(repertoire):
    tot=0
    ntot=0 
    N=0

    # Parcours de tous les fichiers et répertoires dans le répertoire spécifié
    for nom_fichier in os.listdir(repertoire):
        chemin_fichier = os.path.join(repertoire, nom_fichier)
        if os.path.isdir(chemin_fichier):
            # Si c'est un répertoire, on le parcourt récursivement
            parcourir_repertoire(chemin_fichier)

        elif nom_fichier.endswith('.F90'):
            # Si c'est un fichier se terminant par .F90, on effectue une action
            
#            print("==>", chemin_fichier, "<==")
            nombre_blocs, nombre_nblocs = compte_blocs_openacc(chemin_fichier)
           
            if nombre_blocs!=0 or nombre_nblocs!=0:
                N=N+1
                tot=tot+nombre_blocs
                ntot=ntot+nombre_nblocs
                print("==========================")
                print(" file : ", chemin_fichier)
                print("Nombre de blocs #ifdef _OPENACC contenant 'do' ou 'DO':", nombre_blocs)
                print("Nombre de blocs #ifndef _OPENACC contenant 'do' ou 'DO':", nombre_nblocs)
                print("==========================")
    print("N =", N)
    print("tot =", tot)
    print("ntot =", ntot)
#nom_fichier = sys.argv[1]
#nombre_blocs, nombre_nblocs = compte_blocs_openacc(nom_fichier)
#print("Nombre de blocs #ifdef _OPENACC contenant 'do' ou 'DO':", nombre_blocs)
#print("Nombre de blocs #ifndef _OPENACC contenant 'do' ou 'DO':", nombre_nblocs)
#debug=True
debug=False
if not debug:
     # Chemin du répertoire racine à partir duquel commencer la recherche
    repertoire_racine = sys.argv[1]
    
    # Appel de la fonction pour parcourir récursivement les fichiers
    parcourir_repertoire(repertoire_racine)
    
if debug:


    code="""
#ifndef _OPENACC
    laytrop_min = MINVAL(k_laytrop(KIDIA:KFDIA))
    laytrop_max = MAXVAL(k_laytrop(KIDIA:KFDIA))
#else
    laytrop_min = HUGE(laytrop_min)
    laytrop_max = -HUGE(laytrop_max)
    !$ACC PARALLEL DEFAULT(NONE) ASYNC(1)
    !$ACC LOOP GANG VECTOR REDUCTION(min:laytrop_min) REDUCTION(max:laytrop_max)
    do iplon = KIDIA,KFDIA
      laytrop_min = MIN(laytrop_min, k_laytrop(iplon))
      laytrop_max = MAX(laytrop_max, k_laytrop(iplon))
    end do
    !$ACC END PARALLEL
#endif"""

    nombre_blocs, nombre_nblocs = compte_blocs_openacc(code)
    print("Nombre de blocs #ifdef _OPENACC contenant 'do' ou 'DO':", nombre_blocs)
    print("Nombre de blocs #ifndef _OPENACC contenant 'do' ou 'DO':", nombre_nblocs)
   
