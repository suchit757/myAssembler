import Classes as C

datatypes = {"db" : 1, "dd" : 4, "dq" : 8,
             "resb" : 1, "resd" : 4, "resq" : 8,
             "extern" : "ExF", "global" : "GlF", None : None}

regop = {"eax" : '000', "ebx" : '011', "ecx" : '001', "edx" : '010', "ebp" : '101', "esp" : '110'}

opcode = {"mov" : {'REG32REG32':'89', 'SYMREG32':'88', 'REG32SYM':'88', 'SYMLIT':'C7',
                   "eax" : 'B8', "ebx" : 'BB', "ecx" : 'B9', "edx" : 'BA', "ebp" : 'BC', "esp" : 'BD'}}

data_arr = ["db", "dd", "dq"]

bss_arr = ["resb", "resd", "resq"]

reg32 = ["eax", "ebx", "ecx", "edx", "ebp", "esp"]

inst_1 = ["ret"]
inst_2 = ["jmp", "je", "jne", "jz", "jnz", "mul", "div"]
inst_3 = ["mov", "add", "sub"]
