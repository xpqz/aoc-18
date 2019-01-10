"""
day 16 of Advent of Code 2018
by Stefan Kruger
"""

from copy import copy
from collections import defaultdict
import json
import re

def addr(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = register[A] + register[B]
    return result

def addi(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = register[A] + B
    return result

def mulr(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = register[A] * register[B]
    return result

def muli(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = register[A] * B
    return result

def banr(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = register[A] & register[B]

    return result

def bani(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = register[A] & B
    return result

def borr(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = register[A] | register[B]
    return result

def bori(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = register[A] | B
    return result

def setr(register, instr):
    (_opcode, A, _B, C) = instr
    result = copy(register)
    result[C] = register[A]
    return result

def seti(register, instr):
    (_opcode, A, _B, C) = instr
    result = copy(register)
    result[C] = A
    return result

def gtir(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = int(A > register[B])
    return result

def gtri(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = int(register[A] > B)
    return result

def gtrr(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = int(register[A] > register[B])
    return result

def eqir(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = int(A == register[B])
    return result

def eqri(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = int(register[A] == B)
    return result

def eqrr(register, instr):
    (_opcode, A, B, C) = instr
    result = copy(register)
    result[C] = int(register[A] == register[B])
    return result

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
            
def analyse_sample(before, instruction, after):
    instructions = {
        # Addition
        "addr": addr, 
        "addi": addi, 

        # Multiplication
        "mulr": mulr, 
        "muli": muli, 

        # Bit-wise AND
        "banr": banr, 
        "bani": bani, 

        # Bit-wise OR
        "borr": borr, 
        "bori": bori, 

        # Assignment
        "setr": setr, 
        "seti": seti, 

        # Greater-than testing
        "gtir": gtir, 
        "gtri": gtri, 
        "gtrr": gtrr, 

        # Equality testing
        "eqri": eqri, 
        "eqir": eqir, 
        "eqrr": eqrr
    }
    return {
        opname
        for opname, op in instructions.items()
        if after == op(before, instruction)
    }
    
if __name__ == "__main__":
    lines = read_data()
    samples = parse_data(lines)

    count = 0
    for before, instruction, after in samples:
        if len(analyse_sample(before, instruction, after)) >= 3:
            count += 1
    
    print(f"Part1: {count}")



