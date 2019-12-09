
from itertools import permutations 
import time


class IntCodeComputer():
    def __init__(self, phase, input_delegate, initial_input_value = None):
        self._output = 0
        self._output_available = False
        self.ints = self.load_memory('input.txt')
        self.pc = 0 # program counter
        self._input_instruction = 0
        self._phase = phase
        self._input_value = initial_input_value
        self._input_valid = False
        self.is_executing = False
        self._input_delegate = input_delegate
        self._execution_paused = False

    @property
    def output(self):
        self._output_available = False
        return self._output

    @property
    def output_available(self):
        return self._output_available

    def set_input_delegate(self, input_delegate):
        self._input_delegate = input_delegate
        print('New input provided')

    def execute(self):
        self.is_executing = True
        while(self.pc < len(self.ints)):
            # print(f'Program Counter: {pc}')
            return_value = self.run_instruction(self.pc, self.ints)
            if (return_value == -1):
                return -1
            elif (return_value == -2):
                self._execution_paused = True
                return -2
            else:
                self.pc = return_value
        return 0


    def run_instruction(self, ip, ints):
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
            if (self._input_instruction == 0):
                input_value = self._phase
            elif (self._input_instruction >= 1):
                input_value = self._input_delegate()
                if(input_value == None):
                    return -2
            # input_value = input('Enter input')
            self._input_instruction += 1
            ints[ints[ip+1]] = int(input_value)
            return ip+2

        elif (opcode == 4): #output
            param1_mode = int(inst_string[-3])
            if param1_mode == 0:
                test_result = ints[ints[ip+1]]
            elif param1_mode == 1:
                test_result = ints[ip+1]
            self._output = test_result
            self._output_available = True
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

    def load_memory(self, file):
        f = open(file)
        line = f.readlines()[0].strip()
        ints_str = line.split(',')
        ints = [int(x) for x in ints_str]
        return ints

amp_settings = list(permutations(range(5, 10)))

global ampA_ready, ampB_ready, ampC_ready, ampD_ready, ampE_ready
global ampE_called_prior
global ampA, ampB, ampC, ampD, ampE

ampE_called_prior = False
ampA_ready = False
ampB_ready = False
ampC_ready = False
ampD_ready = False
ampE_ready = False

def getOutputA():
    global ampA, ampA_ready

    if(ampA_ready):
        ampA_ready = False
        return ampA.output
    else:
        return None

def getOutputB():
    global ampB, ampB_ready
    if(ampB_ready):
        ampB_ready = False
        return ampB.output
    else:
        return None

def getOutputC():
    global ampC, ampC_ready
    if(ampC_ready):
        ampC_ready = False
        return ampC.output
    else:
        return None

def getOutputD():
    global ampD, ampD_ready
    if(ampD_ready):
        ampD_ready = False
        return ampD.output
    else:
        return None

def getOutputE():
    global ampE, ampE_ready
    global ampE_called_prior
    if (ampE_called_prior):
        ampE_called_prior = True
        if(ampE_ready):
            ampE_ready = False
            return ampE.output
        else:
            return None
    else:
        ampE_called_prior = True
        return 0


outputs = []
for amp_setting in amp_settings:

    ampA = IntCodeComputer(amp_setting[0], getOutputE)
    ampB = IntCodeComputer(amp_setting[1], getOutputA)
    ampC = IntCodeComputer(amp_setting[2], getOutputB)
    ampD = IntCodeComputer(amp_setting[3], getOutputC)
    ampE = IntCodeComputer(amp_setting[4], getOutputD)
    retcode = 0
    while(retcode != -1):
        # print('Running')
        retcode = ampA.execute()
        retcode = ampB.execute()
        retcode = ampC.execute()
        retcode = ampD.execute()
        retcode = ampE.execute()
        ampA_ready = ampA.output_available
        ampB_ready = ampB.output_available
        ampC_ready = ampC.output_available
        ampD_ready = ampD.output_available
        ampE_ready = ampE.output_available
        # print(f'A:{ampA_ready} B:{ampB_ready} C:{ampC_ready} D:{ampD_ready} E:{ampE_ready}')

    outputs.append(ampE.output)
    
max_output = [0,0]
for index, value in enumerate(outputs):
    if value > max_output[0]:
        max_output[0] = value
        max_output[1] = index
max_amp_settings = amp_settings[max_output[1]]
print(f'Max Output = {max_output[0]}. Using Settings: {max_amp_settings}')