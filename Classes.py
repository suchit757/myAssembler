import Data_Structs as DS

class SymTab:
    def __init__(self, symno, name, count,
                 size, status, use, lineno, section, addr):
        self.symno = symno
        self.name = name
        self.count = count
        self.size = size
        self.status = status
        self.use = use
        self.lineno = lineno
        self.section = section
        self.addr = SymTab.getAddr(self,addr)

    def getAddr(self,addr):
        return ("{:08X}".format(addr))


class Literal:
    def __init__(self, litno, name, val):
        self.litno = litno
        self.name = name
        self.val = Literal.getLit(self,val)

    def getLit(self,val):
        return ("{:08X}".format(val))


class Inter_Code:
    def __init__(self, lno, instop, val, oper1, oper2, rm_mod):
        self.lno = lno
        self.instop = DS.opcode[instop][val]
        self.oper1 = oper1
        self.oper2 = oper2
        self.rm_mod = rm_mod
