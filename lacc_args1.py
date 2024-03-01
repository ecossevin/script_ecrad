import re
#SUBROUTINE\s+([a-zA-Z_0-9&]+)
#sub_name=match.group(1)
#sub_body=
#
pattern_sub="SUBROUTINE(.*?)END SUBROUTINE"
pattern_name="SUBROUTINE[\s&]+([a-zA-Z_0-9&]+)\("
#pattern_new="SUBROUTINE[\s&]+[a-zA-Z0-9_]*(\([a-zA-Z0-9_%&\s:,\(\)]*\))"
pattern_new="SUBROUTINE[\s&]+[a-zA-Z0-9_]*(\((?:(?!(END SUBROUTINE|USE|IMPLICIT NONE))[a-zA-Z0-9_%&\s:,\(\)])*\))"

def is_sub_lacc(code):
    verbose=True
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
             


#loop file
debug=True
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

    SUBROUTINE &
    & A(DSFFDSD, SDF SDFSFSFS )

    totD KFDSNKJDFSDKJBF SJHDBF

    END SUBROUTINE


    """
    sub_lacc=[]
    sub_lacc, code_new=is_sub_lacc(content)
    print(sub_lacc)
    print(code_new)
