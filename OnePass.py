import Sym_Table as ST

with open("input.asm","r") as ifile:
    lno = 1
    for line in ifile.readlines():
        ST.parse(line,lno)
        lno += 1

ST.displayST()
ST.displayLT()
ST.displayIC()
ST.size()
