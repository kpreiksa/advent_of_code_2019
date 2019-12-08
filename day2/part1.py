def run_instruction(ip, ints):
    # returns length of instruction executed, or -1 to halt program execution
    inst = ints[ip]
    print(inst)
    if (inst == 1):
        print('Add')
        param1 = ints[ip + 1]
        param2 = ints[ip + 2]
        param3 = ints[ip + 3]
        ints[param3] = ints[param1] + ints[param2]
        return 4

    elif (inst == 2):
        # multiply
        print('Multiply')
        param1 = ints[ip + 1]
        param2 = ints[ip + 2]
        param3 = ints[ip + 3]
        ints[param3] = ints[param1] * ints[param2]
        return 4
    elif (inst == 99):
        # halt
        print('Halt')
        return -1


f = open('input.txt')
line = f.readlines()[0].strip()
ints_str = line.split(',')
ints = [int(x) for x in ints_str]
pc = 0 # program counter
while(pc < len(ints)):
    print(f'Program Counter: {pc}')
    return_value = run_instruction(pc, ints)
    if (return_value == -1):
        break
    else:
        pc += return_value
print('Done.')



