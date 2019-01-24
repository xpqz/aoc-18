"""
day 19 of Advent of Code 2018
by Stefan Kruger
"""
import time
import re

class Instr:

    @staticmethod
    def addr(register, instr):
        (_op, A, B, C) = instr
        register[C] = register[A] + register[B]

    @staticmethod
    def addi(register, instr):
        (_op, A, B, C) = instr
        register[C] = register[A] + B

    @staticmethod
    def mulr(register, instr):
        (_op, A, B, C) = instr
        register[C] = register[A] * register[B]

    @staticmethod
    def muli(register, instr):
        (_op, A, B, C) = instr
        register[C] = register[A] * B

    @staticmethod
    def setr(register, instr):
        (_op, A, B, C) = instr
        register[C] = register[A]

    @staticmethod
    def seti(register, instr):
        (_op, A, B, C) = instr
        register[C] = A

    @staticmethod
    def gtrr(register, instr):
        (_op, A, B, C) = instr
        register[C] = int(register[A] > register[B])

    @staticmethod
    def eqrr(register, instr):
        (_op, A, B, C) = instr
        register[C] = int(register[A] == register[B])

    @staticmethod
    def symtable():
         return {
            "addr": Instr.addr, "addi": Instr.addi, "mulr": Instr.mulr, "muli": Instr.muli, 
            "setr": Instr.setr, "seti": Instr.seti, "gtrr": Instr.gtrr, "eqrr": Instr.eqrr
        }

def read_data(filename="data/input19.data"):
    with open(filename) as f:
        return f.read().splitlines()

def parse_data(lines):
    ip = int(lines[0][-1])
    code = []
    for line in lines[1:]:
        code.append([line[:4], *[int(n) for n in line[5:].split(" ")]])
    
    return ip, code


if __name__ == "__main__":
    lines = read_data()
 
    ip_reg, instructions = parse_data(lines)

    ip = 0
    register = [0, 0, 0, 0, 0, 0]
    opcodes = Instr.symtable() 

    while ip < len(instructions):

        # Fetch
        instr = instructions[ip]
        op = opcodes[instr[0]]

        # Copy IP into bound register
        register[ip_reg] = ip

        # Execute instruction
        op(register, instr)
        
        # Copy IP from bound register
        ip = register[ip_reg]

        # Next instruction
        ip += 1        

    print(f"Part1: {register[0]}")

    # Part2: starting with register = [1, 0, 0, 0, 0, 0] is a very
    # different proposition. There are two nested loops, the key one
    # the sectin at ip=3-11. In all it basically looks like this:
    #
    # reg = [0, 1, 10551432, 1, 1, 3] -- state when we enter loop
    # 
    # while reg[3] <= reg[2]:
    #     reg[1] = 1
    #     while reg[1] <= reg[2]:
    #         if reg[3] * reg[1] == reg[2]:
    #             reg[0] += reg[3]
    #         reg[1] += 1
    #     reg[3] += 1
    # 
    # so that's two nested loops to 10_551_432 -- too much to run.
    #
    # However, we can optimise away the inner loop completely, as shown
    # below, as it only modifies register[0] whenever register[3]
    # divides register[2]:

    register = [0, 1, 10551432, 1, 1, 3]

    while register[3] <= register[2]:
        if register[2] / register[3] == register[2] // register[3]:
            register[0] += register[3]
        register[3] += 1

    print(f"Part2: {register[0]}")
