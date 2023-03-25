import keyboard
import time
from instruction_set import *
from textwrap import wrap


def write(start, end, bit):
    start_loc = f"~{start[0]}~{start[1]}~{start[2]}"
    end_loc = f"~{end[0]}~{end[1]}~{end[2]}"

    fill = "air" if bit == '0' else "redstone_block"
    replace = "redstone_block" if bit == '0' else "air"

    time.sleep(0.5)
    keyboard.write("\n")
    time.sleep(0.5)
    keyboard.write(f"/fill {start_loc} {end_loc} {fill} [] replace {replace}")
    time.sleep(0.5)
    keyboard.write("\n")

def write_byte(data: str, x: int, y: int, z: int):
    start = None
    end = None
    
    for idx, bit in enumerate(data.strip()):
        if bit == '0':
            # write
            if start != None:
                write(start, end, '1')
            start = None
            end = None
        else:
            if start == None:
                start = (x, y - 2 * idx, z)
            end = (x, y - 2 * idx, z)

    if start != None:
        write(start, end, '1')


def write_section(data, dx, dz):
    # clear section
    write((dx, 1, dz), (dx * 33, -13, dz * 33), '0')
    for idx, byte in enumerate(wrap(data, 8)):
        write_byte(byte, dx + idx * 2 * dx, 1, dz + idx * 2 * dz)


def main():
    while True:
        keyboard.wait('/')
        parse = keyboard.get_typed_strings(keyboard.record('enter'))

        args = next(parse).split(' ')
        if args[0] == "program":
            dx = 1 if ('x' in args[1]) else 0
            dz = 1 if ('z' in args[1]) else 0
            if ('-' in args[1]):
                dx *= -1
                dz *= -1

            data = convert_program(fib_program.strip())
            data = ''.join(filter(lambda x: x == '0' or x == '1', data))
            
            for idx, section in enumerate(wrap(data, 8 * 16)):
                if idx != 0:
                    time.sleep(0.5)
                    keyboard.write("\n")
                    time.sleep(0.5)
                    keyboard.write(f"Written {idx} section, continue (n)?")
                    time.sleep(0.5)
                    keyboard.write("\n")
                    keyboard.wait('n')
                write_section(section, dx, dz)

if __name__ == "__main__":
    main()