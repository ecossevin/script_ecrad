      
debug = True

code = """
Afgdbffgd
dfgfdgfgdfgd
implicit none

dsd

ddd
IMPLICIT NONE 
dsffsdfs
"""


#code="""
#1
#IMPLICIT NONE
#2
#"""

debug=True

def add_use(code):
    line_num=0
    num_implicit=0
    lines=code.split("\n")
    print("lines =", lines)
    new_lines=lines
    verbose=True
    verbose=False
    for line in lines:
        print("line =", line)
        if ("implicit none" in line or "IMPLICIT NONE" in line):
            if verbose: print("line_num = ", line_num)
            if verbose: print("num_implicit = ", num_implicit)
            new_lines=new_lines[:line_num+num_implicit+1]+["USE MODACC"]+new_lines[line_num+num_implicit+1:]
            num_implicit+=1
    
    
        line_num+=1
    #new_code=new_lines.join('\n')
    new_code='\n'.join(new_lines)
    return(new_code) 

if debug:
    new_code=add_use(code)
    print("code = ", code)
    print("************************************************")
    print("new_code = ", new_code)
