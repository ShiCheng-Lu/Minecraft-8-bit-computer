from programmer import *
from sim import *
from instruction_set import *

# multiply two number
program = '''
li $1 14
li $0 14
mul $0 $1
hlt
'''

if __name__ == "__main__":
    # auto_program(program)
    sim(program)
    # print(bin(int("1111111", base=2) * int("11111111", base=2)))

    pass
