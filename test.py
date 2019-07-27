from sys import argv

import Sym_Table as ST

script, filename, choice = argv

with open(filename,"r") as ifile:
    lno = 1
    for line in ifile.readlines():
        ST.parse(line,lno)
        lno += 1

if choice == '-s':
    ST.displayST()
elif choice == '-l':
    ST.displayLT()
elif choice == '-i':
    ST.displayIC()
elif choice == '-size':
    def size():
        print("\n\n\ntext\tdata\tbss\tdec\thex\tfilename\n")
        print("%d\t%d\t%d\t%d\t%s\t%s") %(ST.stext,ST.sdata,ST.sbss,(ST.sdata+ST.sbss+ST.stext),"{:02X}".format(ST.sdata+ST.sbss+ST.stext),filename[0:len(filename)-3]+'o')
    size()

