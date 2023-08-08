from programmer import *
from sim import *
from instruction_set import *

# multiply two number
program = '''
li $0 5
li $1 7
mul $0 $1
hlt
'''

if __name__ == "__main__":
    auto_program(program)
