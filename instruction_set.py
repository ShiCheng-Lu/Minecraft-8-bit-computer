'''
Modified from
https://electronics.stackexchange.com/questions/139651/how-to-implement-an-8-bit-cpu

register-register instructions:

0 0 x x x x s d

where x x x x is the opcode,
d is the destination register 0 or 1,
and s is the source register 0 or 1

opcodes field:

1000  add   d = d + s
1001  adc   d = d + s + c
1010  sub   d = d - s
1011  sbb   d = d - s - c
1100  and   d = d and s
1101  or    d = d or s
1110  xor   d = d xor s
1111  not   d = not s
0100  sar   s = 0    arithmetic shift right d
0100  sal   s = 1    arithmetic shift left d
0101  ror   s = 0    rotate right d
0101  rol   s = 1    rotate left d
0110  inc   s = 0    increment d
0110  dec   s = 1    decrement d
0111  inp   s = 0    input to reg d from input port
0111  out   s = 1   output from reg d to output port
0010  cmp   d - s    (no store)
0011  mul   d/s = s * d  (high byte of result into d, low byte into 1-d)
0001  cmb   s = 0    combine d = d | (1-d) << 4 li full 8 bit
0001  sec   sd = 11  set carry
0001  clc   sd = 10  clear carry
0000  call  sd = 11  save pc + 1 to stack (before jmp for call)
0000  ret   sd = 10  return from subroutine
0000  wait  sd = 01  wait for interrupt
0000  hlt   sd = 00  halt

0 1 0 0 n n n n

brn - unconditional branch negative -n bytes (up to -16),
used for branching back at end of a short loop after a skip
instruction
(program pointer += 1 n n n n)

0 1 0 1 b b i i

skip instructions, where
    b b is type of branch
    i i = # of bytes to skip typically 1 or 2, latter for
    skipping over jump/call)

b b field:

00  scs skip i bytes if carry set
01  scc skip i bytes if carry clear
10  szs skip i bytes if zero bit set
11  szc skip i bytes if zero bit clear

0 1 1 n n n n d

load immediate to register r (0 or 1) signed value nnnn
+15 to -16

1 0 a a a a a a

jmp instruction
6 bits provide access to 64 bytes of memory.
use (save next pc to stack) for call

1 1 x a a a a d

load store from/to RAM (x = 0 is load, 1 is store)
3 bits provides access to 16 bytes of RAM
r is the destination or source register (0 or 1)
'''

instructions = {
    "add":  "00.1000.s.d",
    "adc":  "00.1001.s.d",
    "sub":  "00.1010.s.d",
    "sbb":  "00.1011.s.d",
    "and":  "00.1100.s.d",
    "or":   "00.1101.s.d",
    "xor":  "00.1110.s.d",
    "not":  "00.1111.s.d",
    "sar":  "00.0100.0.d",
    "sal":  "00.0100.1.d",
    "ror":  "00.0101.0.d",
    "rol":  "00.0101.1.d",
    "inc":  "00.0110.0.d",
    "dec":  "00.0110.1.d",
    "inp":  "00.0111.0.d",
    "out":  "00.0111.1.d",
    "cmp":  "00.0010.s.d",
    "mul":  "00.0011.s.d",
    "cmb":  "00.0001.0.d",
    "sec":  "00.0001.1.1",
    "clc":  "00.0001.1.0",

    "call": "00.0000.11",
    "ret":  "00.0000.10",
    "wait": "00.0000.01",
    "hlt":  "00.0000.00",

    "brn":  "0100.nnnn",
    "bic":  "0101.00.nn",
    "bnc":  "0101.01.nn",
    "biz":  "0101.10.nn",
    "bnz":  "0101.11.nn",

    "li":   "011.nnnn.d",
    "jmp":  "10.nnnnnn",
    "ldr":  "110.nnnn.d",
    "str":  "111.nnnn.d",
}

fib_program = '''
li $0 3     #
str $0 10    #
li $0 1     #
str $0 8    #
str $0 9    #
ldr $0 9    # add two prev
ldr $1 8    #
add $0 $1   #
str $0 8    #
str $1 9    #
ldr $0 10    # check if this is the n-th
dec $0      #
szs 2       #
str $0 10    #
brn -9       # jmp 5 or brn -9
ldr $0 8    #
ldr $1 8    #
hlt         #
'''

program = '''

'''


def register(register: str):
    match register:
        case '$0':
            return 0
        case '$1':
            return 1
        case _:
            raise ValueError("invalid register", register)


def branch(lines: str):
    lines_int = int(lines)
    if lines_int < -16 or lines_int >= 0:
        raise ValueError("branch amount must be -16 <= x < 0")
    return number(16 + lines_int, 4)


def skip(lines: str):
    lines_int = int(lines)
    if lines_int >= 4:
        raise ValueError("skip amount must be 0 <= x < 4")
    return format(lines_int, 'b')


def number(num: str, digits: int):
    num_int = int(num)
    if num_int >= (2 ** digits):
        raise ValueError(f"value must be < {(2 ** digits)}")
    return format(num_int, f'0{digits}b')


def convert(instruction: str):
    if (instruction == ''):
        return ''
    args = instruction.split(' ')
    match args[0].lower():
        case 'add':
            return f'001000{register(args[2])}{register(args[1])}'
        case 'adc':
            return f'001001{register(args[2])}{register(args[1])}'
        case 'sub':
            return f'001010{register(args[2])}{register(args[1])}'
        case 'subb':
            return f'001011{register(args[2])}{register(args[1])}'
        case 'and':
            return f'001100{register(args[2])}{register(args[1])}'
        case 'or':
            return f'001101{register(args[2])}{register(args[1])}'
        case 'xor':
            return f'001110{register(args[2])}{register(args[1])}'
        case 'not':
            return f'001111{register(args[2])}{register(args[1])}'
        case 'asr':
            return f'0001000{register(args[1])}'
        case 'asl':
            return f'0001001{register(args[1])}'
        case 'ror':
            return f'0001010{register(args[1])}'
        case 'rol':
            return f'0001011{register(args[1])}'
        case 'inc':
            return f'0001100{register(args[1])}'
        case 'dec':
            return f'0001101{register(args[1])}'
        case 'inp':
            raise NotImplementedError(args[0])
            return f'0001110{register(args[1])}'
        case 'out':
            raise NotImplementedError(args[0])
            return f'0001111{register(args[1])}'
        case 'cmp':
            return f'000010{register(args[2])}{register(args[1])}'
        case 'mul':
            raise NotImplementedError(args[0])
            return f'000011{register(args[2])}{register(args[1])}'
        case 'cmd':
            return f'0000010{register(args[1])}'
        case 'sec':
            return f'00000111'
        case 'clc':
            return f'00000110'
        case 'call':
            return f'00000011'
        case 'ret':
            return f'00000010'
        case 'wait':
            return f'00000001'
        case 'hlt':
            return f'00000000'
        case 'brn':
            return f'0111{branch(args[1])}'
        case 'scs':
            return f'011000{skip(args[1])}'
        case 'scc':
            return f'011001{skip(args[1])}'
        case 'szs':
            return f'011010{skip(args[1])}'
        case 'szc':
            return f'011011{skip(args[1])}'
        case 'li':
            return f'010{number(args[2], 4)}{register(args[1])}'
        case 'jmp':
            return f'10{number(args[1], 6)}'
        case 'ldr':
            return f'110{number(args[2], 4)}{register(args[1])}'
        case 'str':
            return f'111{number(args[2], 4)}{register(args[1])}'
        case _:
            raise ValueError("invalid instruction", instruction)


def convert_program(program: str, debug=False):
    result = ''
    for line in program.split('\n'):
        result += f'{convert(line)}  {line if debug == True else ""}\n'
    return result


def to_redstone_shape(program: str, debug=False):
    result = []
    for idx, line in enumerate(program.split('\n')):
        cmd = convert(line)
        if cmd != '':
            result.append(cmd)

        if idx % 16 == 0 and len(result) != 0:
            for i in range(0, 8):
                for cmd in result:
                    print("X " if cmd[i] == '1' else "_ ", end='')
                print('')
            result = []
            print('\n')
    
    if len(result) != 0:
        for i in range(0, 8):
            for cmd in result:
                print("X " if cmd[i] == '1' else "_ ", end='')
            print('')
        result = []
    


if __name__ == "__main__":
    to_redstone_shape(fib_program)
    print('')
    print(convert_program(fib_program, debug=True))
