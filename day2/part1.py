def run_instruction(pc, ints):
    inst = ints[pc]
    print(inst)
    if (inst == 1):
        print('Multiplying')
        param1_loc = ints[pc + 1]
        param2_loc = ints[pc + 2]
        out_loc = ints[pc + 3]
        ints[out_loc] = ints[param1_loc] + ints[param2_loc]
        return 0

    elif (inst == 2):
        # multiply
        print('Multiplying')
        param1_loc = ints[pc + 1]
        param2_loc = ints[pc + 2]
        out_loc = ints[pc + 3]
        ints[out_loc] = ints[param1_loc] * ints[param2_loc]
        return 0
    elif (inst == 99):
        # halt
        print('Halting')
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
        pc += 4
print('Done.')



