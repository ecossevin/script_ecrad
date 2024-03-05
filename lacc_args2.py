import re

#pattern_name="CALL[\s]+"+sub_name
def process_call(lines, sub_lacc):
    compt=-1
    verbose=True
    is_call=False
    for line in lines:
        print("line =", line)
        for call_name in sub_lacc: 
            if call_name in line:
                if verbose: print("call_name in ", line)
                is_call=True

        if is_call==True:

            call.append(line)
            pos=0
            for char in line:
                if char== '(':
                    compt+=1
                elif char == ')':
                    compt-=1
                if compt<0:
                    new_line=line[:pos]+", LACC"+line[pos:]
                    line=new_line
                    is_call=False
                pos+=1
                

debug=True     
if debug:                
sub_lacc=["coucou", "toto"]
    code="""
    CALL toto(A, a(:,:,1), &
    & dfff(fjfjf, 4, :)
    ffgfggf
    ddddd()
    sdsd
    """
    process_call(code, sub_lacc)
    print("code = ", code)
    

if not debug:
    with open("sub_lacc.txt", "r") as file:
        sub_lacc=file.readlines()
#    for sub in sub_lacc:
#        file.write("%s\n" % item)
    sub_lacc=[sub.strip for sub in sub_lacc]
    if verbose: print(lacc_sub)
    
    process_call(code, sub_lacc)
