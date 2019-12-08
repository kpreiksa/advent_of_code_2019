
def run_instruction(ip, ints):
    # returns length of instruction executed, or -1 to halt program execution
    inst = ints[ip]
    inst_string = f'{inst:#05}' # 5 = max number of digits for an instruction
    opcode = int(inst_string[-2:])
    if (opcode == 1): # addition. 3 parameters
        # print('Add')
        param1_mode = int(inst_string[-3])
        param2_mode = int(inst_string[-4])
        inst_str = 'Add'
        # param3_mode = inst_string[-5] Don't need this since it's the output

        if (param1_mode == 0): # 0 is position mode
            param1 = ints[ints[ip + 1]]
            inst_str += f' ({ints[ip +1]}) -> {ints[ints[ip+1]]}'
        elif (param1_mode == 1): # 1 is immediate mode
            param1 = ints[ip + 1]
            inst_str += f' {ints[ip+1]}'

        if (param2_mode == 0): # 0 is position mode
            param2 = ints[ints[ip + 2]]
            inst_str += f' + ({ints[ip +2]}) -> {ints[ints[ip+2]]}'
        elif (param2_mode == 1): # 1 is immediate mode
            param2 = ints[ip + 2]
            inst_str += f' + {ints[ip+2]}'

        param3 = ints[ip + 3] # always position mode
        inst_str += f' => ({param3})'
        ints[param3] = param1 + param2
        return ip+4

    elif (opcode == 2): # multiplication. 3 parameters
        # multiply
        # print('Multiply')
        param1_mode = int(inst_string[-3])
        param2_mode = int(inst_string[-4])
        # param3_mode = inst_string[-5] Don't need this since it's the output

        if (param1_mode == 0): # 0 is position mode
            param1 = ints[ints[ip + 1]] # dereference
        elif (param1_mode == 1): # 1 is immediate mode
            param1 = ints[ip + 1]

        if (param2_mode == 0): # 0 is position mode
            param2 = ints[ints[ip + 2]]
        elif (param2_mode == 1): # 1 is immediate mode
            param2 = ints[ip + 2]

        param3 = ints[ip + 3] # always position mode
        ints[param3] = param1 * param2
        return ip+4

    elif (opcode == 3): #input
        input_value = input('Enter input')
        ints[ints[ip+1]] = int(input_value)
        return ip+2

    elif (opcode == 4): #output
        param1_mode = int(inst_string[-3])
        if param1_mode == 0:
            test_result = ints[ints[ip+1]]
        elif param1_mode == 1:
            test_result = ints[ip+1]
        print(f'Test: {test_result}')
        return ip+2

    elif (opcode == 5): # jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        param1_mode = int(inst_string[-3])
        param2_mode = int(inst_string[-4])
        if (param1_mode == 0): # 0 is position mode
            param1 = ints[ints[ip + 1]] # dereference
        elif (param1_mode == 1): # 1 is immediate mode
            param1 = ints[ip + 1]

        if (param2_mode == 0): # 0 is position mode
            param2 = ints[ints[ip + 2]]
        elif (param2_mode == 1): # 1 is immediate mode
            param2 = ints[ip + 2]

        if param1 != 0:
            return param2
        else:
            return ip+3

    elif (opcode == 6): # jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
        param1_mode = int(inst_string[-3])
        param2_mode = int(inst_string[-4])
        if (param1_mode == 0): # 0 is position mode
            param1 = ints[ints[ip + 1]] # dereference
        elif (param1_mode == 1): # 1 is immediate mode
            param1 = ints[ip + 1]

        if (param2_mode == 0): # 0 is position mode
            param2 = ints[ints[ip + 2]]
        elif (param2_mode == 1): # 1 is immediate mode
            param2 = ints[ip + 2]

        if param1 == 0:
            return param2
        else:
            return ip+3

    elif (opcode == 7): # less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        param1_mode = int(inst_string[-3])
        param2_mode = int(inst_string[-4])
        if (param1_mode == 0): # 0 is position mode
            param1 = ints[ints[ip + 1]] # dereference
        elif (param1_mode == 1): # 1 is immediate mode
            param1 = ints[ip + 1]

        if (param2_mode == 0): # 0 is position mode
            param2 = ints[ints[ip + 2]]
        elif (param2_mode == 1): # 1 is immediate mode
            param2 = ints[ip + 2]

        param3 = ints[ip+3]

        if param1 < param2:
            ints[param3] = 1
        else:
            ints[param3] = 0
        
        return ip + 4

    elif (opcode == 8): # equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        param1_mode = int(inst_string[-3])
        param2_mode = int(inst_string[-4])
        if (param1_mode == 0): # 0 is position mode
            param1 = ints[ints[ip + 1]] # dereference
        elif (param1_mode == 1): # 1 is immediate mode
            param1 = ints[ip + 1]

        if (param2_mode == 0): # 0 is position mode
            param2 = ints[ints[ip + 2]]
        elif (param2_mode == 1): # 1 is immediate mode
            param2 = ints[ip + 2]

        param3 = ints[ip+3]

        if param1 == param2:
            ints[param3] = 1
        else:
            ints[param3] = 0
        
        return ip + 4
    elif (opcode == 99):
        # halt
        # print('Halt')
        return -1
    else:
        print(f'Invalid instruction: {inst}')

def load_memory(file):
    f = open(file)
    line = f.readlines()[0].strip()
    ints_str = line.split(',')
    ints = [int(x) for x in ints_str]
    return ints


ints = load_memory('input.txt')
pc = 0 # program counter
while(pc < len(ints)):
    # print(f'Program Counter: {pc}')
    return_value = run_instruction(pc, ints)
    if (return_value == -1):
        break
    else:
        pc = return_value
