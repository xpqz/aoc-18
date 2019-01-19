"""
day 19 of Advent of Code 2018
by Stefan Kruger
"""

from copy import copy

class Instr:

    @staticmethod
    def addr(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = register[A] + register[B]
        return result

    @staticmethod
    def addi(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = register[A] + B
        return result

    @staticmethod
    def mulr(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = register[A] * register[B]
        return result

    @staticmethod
    def muli(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = register[A] * B
        return result

    @staticmethod
    def banr(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = register[A] & register[B]
        return result

    @staticmethod
    def bani(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = register[A] & B
        return result

    @staticmethod
    def borr(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = register[A] | register[B]
        return result

    @staticmethod
    def bori(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = register[A] | B
        return result

    @staticmethod
    def setr(register, instr):
        (_opcode, A, _B, C) = instr
        result = copy(register)
        result[C] = register[A]
        return result

    @staticmethod
    def seti(register, instr):
        (_opcode, A, _B, C) = instr
        result = copy(register)
        result[C] = A
        return result

    @staticmethod
    def gtir(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = int(A > register[B])
        return result

    @staticmethod
    def gtri(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = int(register[A] > B)
        return result

    @staticmethod
    def gtrr(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = int(register[A] > register[B])
        return result

    @staticmethod
    def eqir(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = int(A == register[B])
        return result

    @staticmethod
    def eqri(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = int(register[A] == B)
        return result

    @staticmethod
    def eqrr(register, instr):
        (_opcode, A, B, C) = instr
        result = copy(register)
        result[C] = int(register[A] == register[B])
        return result

    @staticmethod
    def symtable():
         return {
            "addr": Instr.addr, "addi": Instr.addi, 
            "mulr": Instr.mulr, "muli": Instr.muli, 
            "banr": Instr.banr, "bani": Instr.bani, 
            "borr": Instr.borr, "bori": Instr.bori, 
            "setr": Instr.setr, "seti": Instr.seti, 
            "gtir": Instr.gtir, "gtri": Instr.gtri, "gtrr": Instr.gtrr, 
            "eqri": Instr.eqri, "eqir": Instr.eqir, "eqrr": Instr.eqrr
        }

def read_data(filename="data/input19.data"):
    with open(filename) as f:
        return f.read().splitlines()

def parse_data(lines):
    """
    opcode A B C
    """
    ip = int(lines[0][-1])
    code = []
    for line in lines[1:]:
        code.append([line[:4], *[int(n) for n in line[5:].split(" ")]])
    
    return ip, code

if __name__ == "__main__":
    lines = read_data()
    # lines = [
    #     "#ip 0",
    #     "seti 5 0 1",
    #     "seti 6 0 2",
    #     "addi 0 1 0",
    #     "addr 1 2 3",
    #     "setr 1 0 0",
    #     "seti 8 0 4",
    #     "seti 9 0 5"
    # ]

    ip_reg, instructions = parse_data(lines)

    register = [0, 0, 0, 0, 0, 0]
    ip = 0
    opcodes = Instr.symtable()
    while ip < len(instructions):
        instr = instructions[ip]
        op = opcodes[instr[0]]
        register[ip_reg] = ip
        print(ip, register, instr[0], " ", end="")
        register = op(register, instr)
        ip = register[ip_reg]
        ip += 1
        print(register)
        


