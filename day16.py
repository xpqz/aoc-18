"""
day 16 of Advent of Code 2018
by Stefan Kruger
"""

from copy import copy
from collections import defaultdict
import re

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

def analyse_sample(before, instruction, after):
    return {
        opname
        for opname, op in Instr.symtable().items()
        if after == op(before, instruction)
    }

def read_data(filename="data/input16-1.data"):
    with open(filename) as f:
        return f.read().splitlines()

def parse_data(lines):
    """
    Before, Instruction, After
    """
    result = []
    for l in range(0, len(lines), 4):
        op = []
        for data in [lines[l], lines[l+1], lines[l+2]]:
            op.append([int(n) for n in re.findall(r"-?\d+", data)])
        result.append(op)

    return result

def parse_data_part2(lines):
    """
    opcode A B C
    """
    return [
        [int(n) for n in re.findall(r"-?\d+", line)]
        for line in lines
    ]
            
def find_opcodes(samples):
    by_opcode = defaultdict(set)

    for before, instruction, after in samples:
        by_opcode[instruction[0]].update(analyse_sample(before, instruction, after))

    singles = set()

    while True:
        before = len(singles)
        for _op, match in by_opcode.items():
            if len(match) > 1:
                match -= singles
            
            if len(match) == 1:
                singles.add(next(iter(match)))

        if len(singles) == before:
            break

    sym = Instr.symtable()

    return {
        opcode: sym[next(iter(opname_set))]
        for opcode, opname_set in by_opcode.items()
    }


if __name__ == "__main__":
    lines = read_data()
    samples = parse_data(lines)

    count = 0
    for before, instruction, after in samples:
        if len(analyse_sample(before, instruction, after)) >= 3:
            count += 1
    
    print(f"Part1: {count}")

    opcodes = find_opcodes(samples)
 
    lines = read_data(filename="data/input16-2.data")
    instructions = parse_data_part2(lines)

    register = [0, 0, 0, 0]
    for instr in instructions:
        op = opcodes[instr[0]]
        register = op(register, instr)

    print(f"Part2: {register[0]}")


