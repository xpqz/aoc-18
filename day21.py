"""
day 21 of Advent of Code 2018
by Stefan Kruger
"""

# Part1: looking at the data, we see that line 28 is the
# exit condition we need to trigger. Run the program until
# the first time line 28 is hit, and the answer is the value
# in register[2]
#
#
# ip--inst-------A--------B-C
# ---------------------------
# 0:  seti     123        0 2		
# 1:  bani       2      456 2
# 2:  eqri       2       72 2   COND reg[2] == 72
# 3:  addr       2        1 1
# 4:  seti       0        0 1	GOTO 1
# 5:  seti       0        3 2		
# 6:  bori       2    65536 5   REG 5 = REG 2 | 65536
# 7:  seti 4843319        1 2		
# 8:  bani       5      255 4
# 9:  addr       2        4 2
# 10: bani       2 16777215 2     
# 11: muli       2    65899 2		
# 12: bani       2 16777215 2
# 13: gtir     256        5 4	COND 256 > reg[5]
# 14: addr       4        1 1
# 15: addi       1        1 1
# 16: seti      27        4 1	GOTO 28
# 17: seti       0        7 4		
# 18: addi       4        1 3
# 19: muli       3      256 3
# 20: gtrr       3        5 3	COND reg[3] > reg[5]
# 21: addr       3        1 1
# 22: addi       1        1 1
# 23: seti      25        0 1	GOTO 26
# 24: addi       4        1 4
# 25: seti      17        0 1	GOTO 18
# 26: setr       4        1 5   REG 5 = REG 4 
# 27: seti       7        3 1	GOTO 8
# 28: eqrr       2        0 4  	COND reg[2] == reg[0]		Only place reg[0] is consulted
# 29: addr       4        1 1
# 30: seti       5        3 1	GOTO 6

class Instr:

    @staticmethod
    def addr(register, instr):
        (_opcode, A, B, C) = instr
        register[C] = register[A] + register[B]

    @staticmethod
    def addi(register, instr):
        (_opcode, A, B, C) = instr
        register[C] = register[A] + B

    @staticmethod
    def muli(register, instr):
        (_opcode, A, B, C) = instr
        register[C] = register[A] * B

    @staticmethod
    def setr(register, instr):
        (_opcode, A, _B, C) = instr
        register[C] = register[A]

    @staticmethod
    def seti(register, instr):
        (_opcode, A, _B, C) = instr
        register[C] = A

    @staticmethod
    def gtrr(register, instr):
        (_opcode, A, B, C) = instr
        register[C] = int(register[A] > register[B])

    @staticmethod
    def bani(register, instr):
        (_opcode, A, B, C) = instr
        register[C] = register[A] & B

    @staticmethod
    def bori(register, instr):
        (_opcode, A, B, C) = instr
        register[C] = register[A] | B

    @staticmethod
    def gtir(register, instr):
        (_opcode, A, B, C) = instr
        register[C] = int(A > register[B])

    @staticmethod
    def eqri(register, instr):
        (_opcode, A, B, C) = instr
        register[C] = int(register[A] == B)

    @staticmethod
    def eqrr(register, instr):
        (_opcode, A, B, C) = instr
        register[C] = int(register[A] == B)

    @staticmethod
    def symtable():
         return {
            "addr": Instr.addr, "addi": Instr.addi, 
            "muli": Instr.muli,  
            "bani": Instr.bani, "bori": Instr.bori, 
            "setr": Instr.setr, "seti": Instr.seti, 
            "gtir": Instr.gtir, "gtrr": Instr.gtrr, 
            "eqri": Instr.eqri, "eqrr": Instr.eqrr
        }

def read_data(filename="data/input21.data"):
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

    solutions = set()
    candidate = None

    while ip < len(instructions):
        # Fetch
        instr = instructions[ip]
        op = opcodes[instr[0]]

        # Copy IP into bound register
        register[ip_reg] = ip

        # Execute instruction
        op(register, instr)

        if ip == 28:
            break
        
        # Copy IP from bound register
        ip = register[ip_reg]

        # Next instruction
        ip += 1

    print(f"Part1: {register[2]}")

    
    # For part 2 we keep track of all solutions until
    # they start to repeat. The last value of the cycle
    # is the one we want

    solutions = set()
    candidate = None

    ip = 0
    register = [0, 0, 0, 0, 0, 0]

    while ip < len(instructions):
        # Fetch
        instr = instructions[ip]
        op = opcodes[instr[0]]

        # Copy IP into bound register
        register[ip_reg] = ip

        # Execute instruction
        op(register, instr)

        if ip == 28:
            if register[2] in solutions:
                break
            candidate = register[2]
            solutions.add(register[2])
    
        
        # Copy IP from bound register
        ip = register[ip_reg]

        # Next instruction
        ip += 1

    print(f"Part2: {candidate}")

