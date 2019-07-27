import Classes as C
import Data_Structs as DS
import re

Symbol_Table = []
Lit_Table = []
Inter_Code = []

curr_pos, sym_no, lit_no = 0, 0, 1

addr, baddr, taddr = 0, 0, 0
sdata, sbss, stext = 0, 0, 0

def myIsDigit(s):
  return re.search("[^0-9]", s) is None


def data_parse(line, lno, curr_pos):
    global sym_no, addr, sdata
    line = line.split()
    
    if(line[0] not in DS.data_arr and line[1] in DS.data_arr):
        
        if(line[1] == "dd" or line[1] == "dq"):
            ddline = list(filter(lambda a: a != "" ,re.split(" |,",line[2])))
            size = DS.datatypes[line[1]] * len(ddline)
            val = DS.datatypes[line[1]] * len(ddline)
            sym_no += 1
            s = C.SymTab(sym_no,line[0],len(ddline),
                         size,"SDEF",0,lno,"DATA",addr)
            sdata += size
                        
        elif(line[0] not in DS.data_arr and line[1] == "db"):
            msg = ''.join(line[2:len(line)])
            size  = (DS.datatypes[line[1]] * len(msg)-5)
            sym_no += 1
            val = (DS.datatypes[line[1]] * len(msg)-5)
            s = C.SymTab(sym_no,line[0],size,
                         size,"SDEF",0,lno,"DATA",addr)
            sdata += size
            
        Symbol_Table.append(s)
        addr = int(addr) + val
        
def bss_parse(line, lno, curr_pos):
    global sym_no, baddr, sbss
    line = line.split()

    if (line[0] not in DS.bss_arr and line[1] in DS.bss_arr):
        size = DS.datatypes[line[1]] * int(line[2])
        sym_no += 1
        val = DS.datatypes[line[1]] * len(line[2])
        s = C.SymTab(sym_no,line[0],line[2],
                     size,"SDEF",0,lno,"BSS",baddr)
        Symbol_Table.append(s)
        baddr = int(baddr) + val
        sbss = sbss + size
        
def updateSym(sym,lno):
    global sym_no, use, taddr
    sym_no += 1
    s = C.SymTab(sym_no,sym,"-",
                 "-","LDEF",0,lno,"TEXT",taddr)
    Symbol_Table.append(s)
    taddr += 1


def updateLiteral(sym):
    global lit_no
    flag = 0
    for i in Lit_Table:
      if i.name == sym:
        flag = 1
    if flag == 0:
      if (myIsDigit(sym)):
        val = int(sym)
        l = C.Literal(lit_no,sym,val)
      else:
        l = C.Literal(lit_no,sym,ord(sym))
      lit_no += 1
      Lit_Table.append(l)


def checkSym(sym,lno):
    global use
    flag = 0

    if sym.startswith("\'") and sym.endswith("\'"):
        sym = sym[1:-1]
        flag = 1
        updateLiteral(sym)
        
    elif(myIsDigit(sym)):
        flag = 1
        updateLiteral(sym)
        
    else:

        for i in Symbol_Table:
          if i.name == sym:
            i.use += 1
            flag = 1
            
    if flag == 0:
      updateSym(sym,lno)


def returnaddr(sym):
  for i in Symbol_Table:
    if i.name == sym:
      return ("SYM",i.addr), 1
    else:
      pass
    
  if sym.startswith("\'") and sym.endswith("\'"):
    sym = sym[1:-1]

  for i in Lit_Table:
    if i.name == sym:
      return ("LIT",i.val), 0

def inst_parse(line,lno):
    if(line[0] in DS.inst_1):
        pass
    
    elif(line[0] in DS.inst_2):
        #First operand is reg
        if(line[1] in DS.reg32):
            pass
          
        #First operand is mem
        elif(line[1].startswith("dword[") or line[1].startswith("qword[")):
          sym = list(line[1])
          sym = sym[6:-1]
          line[1] = str(sym[0])
          checkSym(line[1],lno)
                        
    elif(line[0] in DS.inst_3):
      op = line[0]
      #First operand is reg
      if(line[1] in DS.reg32):
      
        #Second operand is reg
        if(line[2] in DS.reg32):
          oper2 = ("REG32",line[2])
          ic = C.Inter_Code(lno,line[0],'REG32REG32',("REG32",line[1]),oper2,'11')
          Inter_Code.append(ic)
        
        #Second operand is mem
        elif(line[2].startswith("dword[") or line[2].startswith("qword[")):
          sym = list(line[2])
          sym = sym[6:-1]
          line[2] = ''.join(map(str, sym))
          if(line[2] in DS.reg32):
            oper2 = ("SYM",line[2])
            ic = C.Inter_Code(lno,line[0],'REG32SYM',("REG32",line[1]),oper2,'00')
          else:
            checkSym(line[2],lno)
            oper2 = returnaddr(line[2])
            ic = C.Inter_Code(lno,line[0],'REG32SYM',("REG32",line[1]),oper2[0],'00')
          
          Inter_Code.append(ic)
          
        #Second operand is immediate value or symbol
        else:
          checkSym(line[2],lno)
          oper2 = returnaddr(line[2])
          if oper2[1] == 1:
            ic = C.Inter_Code(lno,line[0],'REG32SYM',("REG32",line[1]),oper2[0],'00')
          elif oper2[1] == 0:
            ic = C.Inter_Code(lno,line[0],line[1],("REG32",line[1]),oper2[0],None)
          Inter_Code.append(ic)
        
      #First operand is mem
      elif(line[1].startswith("dword[") or line[1].startswith("qword[")):
        sym = list(line[1])
        sym = sym[6:-1]
        line[1] = ''.join(map(str, sym))
        if(line[1] in DS.reg32):
            oper1 = ("SYM",line[1])
        else:
          checkSym(line[1],lno)
          oper = returnaddr(line[1])
          oper1 = oper[0]
          
        #Second operand is reg
        if(line[2] in DS.reg32):
          oper2 = ("REG32",line[2])
          ic = C.Inter_Code(lno,line[0],'SYMREG32',oper1,oper2,'00')
          Inter_Code.append(ic)
          
        #Second operand is immediate value
        else:
          checkSym(line[2],lno)
          oper2 = returnaddr(line[2])
          ic = C.Inter_Code(lno,line[0],'SYMLIT',oper1,oper2[0],None)
          Inter_Code.append(ic)

def text_parse(line, lno, curr_pos):
    global sym_no, use, taddr, stext
    flag = 0
    if(line == "section .text"):
        pass
    
    else:
        line = list(filter(lambda a: a != "" ,re.split(" |\t|,",line)))
        #For external function calling
        if(line[0] == "global" or line[0] == "extern"):
            #line = list(filter(lambda a: a != "" ,re.split(" |,",line[1])))
            for i in range(1,len(line)):
                sym_no += 1
                s = C.SymTab(sym_no,line[i],"-",
                             "-","LDEF",0,lno,"TEXT",taddr)
                Symbol_Table.append(s)
        #From main
        elif(len(line) == 1):
            if(line[0].endswith(":")):
                line[0] = line[0].replace(":","")
                checkSym(line[0],lno)
                
        elif(len(line) >= 2):
            if(line[0].endswith(":")):
                line[0] = line[0].replace(":","")
                checkSym(line[0],lno)
                inst_parse(line[1:4],lno)
                
            else:
                inst_parse(line[0:3],lno)
    taddr += 1
    stext += 2

def parse(line, lno):
    global curr_pos
    line = line.strip()
    if line != "":
        if(line == "section .data"):
            curr_pos = 1
            
        elif(line == "section .bss"):
            curr_pos = 2
            
        elif(line == "section .text"):
            curr_pos = 3
            
        elif(line.startswith(";;") or line.startswith(";")):
            curr_pos = 0
        
        if(curr_pos == 1):
            data_parse(line,lno,curr_pos)
            
        elif(curr_pos == 2):
            bss_parse(line,lno,curr_pos)
            
        elif(curr_pos == 3):
            text_parse(line,lno,curr_pos)


def displayST():
    print("""
\t\t\t\t\tSYMBOL TABLE:\n
Symbol no\tSymbol Name\tCount\tTotal Size\tStatus\t\tUse\tLine no\t\tSection\t\tAddress""")
    for i in Symbol_Table:
        print("%s\t\t%s\t\t%s\t\t%s\t%s\t\t%s\t\t%s\t%s\t\t%s"
        %(i.symno, i.name, i.count, i.size,
          i.status, i.use, i.lineno, i.section, i.addr))


def displayLT():
  print("""\n\n\n\t    LITERAL TABLE:\n
Literal no\tLiteral Name\tHex Value""")
  for i in Lit_Table:
    print("%d\t\t%s\t\t%s" %(i.litno,i.name,i.val))


def displayIC():
  print("\n\n\n\t\t\t\t\tINTERMEDIATE CODE:\n")
  for i in Inter_Code:
    print("%s\t%s\t%s\t\t%s\t\t%s" %(i.lno,i.instop,i.oper1,i.oper2,i.rm_mod))

def size():
  print("\n\n\ndata\tbss\ttext\tdec\thex\n")
  print("%d\t%d\t%d\t%d\t%s") %(sdata,sbss,stext,(sdata+sbss+stext),"{:02X}".format(sdata+sbss+stext))
