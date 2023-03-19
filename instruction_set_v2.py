
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
1011  subb  d = d - s - c
1100  and   d = d and s
1101  or    d = d or s
1110  xor   d = d xor s
1111  not   d = not s
0100  asr   s = 0   arithmetic shift right d
0100  asl   s = 1   arithmetic shift left d
0101  ror   s = 0   rotate right d
0101  rol   s = 1   rotate left d
0110  inc   s = 0   increment d
0110  dec   s = 1   decrement d
0111  cmp   d - s   (no store)
0010  inp  s = 0   input to reg d from input port
0010  out  s = 1   output from reg d to output port
0011  
0011  
0001  mul   d/s = s * d  (high byte of result into d, low byte into 1-d)
0000  sec   sd = 11  set carry
0000  clc   sd = 10  clear carry
0000  ret   sd = 01  return from subroutine
0000  return no 
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

call instruction
p is reserved for a page bit (or could just be the high
bit of address).  12 bits of address provide a direct call
or jump to 4K of program memory (or 5 bits provide
access to 32 bytes of memory).

1 1 x a a a a d

load store from/to RAM (x = 0 is load, 1 is store)
3 bits provides access to 16 bytes of RAM
r is the destination or source register (0 or 1)
'''