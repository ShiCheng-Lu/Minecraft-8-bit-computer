from programmer import *
from sim import *
from instruction_set import *

# multiply two number
program = '''
li $0 3     #
str $0 10    #
li $0 1     #
str $0 8    #
ldr $0 10    #
ldr $1 8    #
hlt
'''

if __name__ == "__main__":
    auto_program(instruction_set.fib_program)
    # sim(program)
    # print(bin(int("1111111", base=2) * int("11111111", base=2)))

    pass
