
from itertools import permutations

class ProgramTerminatedError(Exception):
    pass

class Opcode():
    def __init__(self, ints, pc):
        ''' Starting with an integer, generate the opcode obj '''
        self._raw_opcode = ints[pc]
        self._address = pc
        self._inst_string = f'{self._raw_opcode:#05}' # 5 = max number of digits for an instruction
        
    @property
    def opcode(self):
        return int(self._inst_string[-2:])

    @property
    def param1_addr(self):
        return self._address+1

    @property
    def param2_addr(self):
        return self._address+2

    @property
    def param3_addr(self):
        return self._address+3

    @property
    def param1_value(self, mem):
        if (self.param1_mode == 0):
            return mem[mem[self.param1_addr]]

        elif (self.param1_mode == 1): 
            return mem[self.param1_addr]

    @property
    def param2_value(self, mem):
        if (self.param2_mode == 0):
            return mem[mem[self.param2_addr]]

        elif (self.param2_mode == 1): 
            return mem[self.param2_addr]

    @property
    def param1_mode(self):
        return int(self._inst_string[-3])

    @property
    def param2_mode(self):
        return int(self._inst_string[-4])

    @property
    def address(self):
        return self._address


class IntCodeComputer():
    def __init__(self, phase, input_value):
        self.output = 0
        self.ints = self.load_memory('input.txt')
        self.pc = 0 # program counter
        self._input_instruction = 0
        self._phase = phase
        self._input_value = input_value
        self._opcodes = {
            1: self.oc_add,
            2: self.oc_mult,
            3: self.oc_input,
            4: self.oc_output,
            5: self.oc_jmpT,
            6: self.oc_jmpF,
            7: self.oc_lt,
            8: self.oc_eq,
            99:self.oc_halt,
        }

    def oc_add(self, oc):

        param1 = oc.param1_value
        if (oc.param1_mode == 0): # 0 is position mode
            param1 = self.ints[self.ints[self.pc + 1]]
        elif (oc.param1_mode == 1): # 1 is immediate mode
            param1 = self.ints[self.pc + 1]


        if (oc.param2_mode == 0): # 0 is position mode
            param2 = self.ints[self.ints[self.pc + 2]]
        elif (oc.param2_mode == 1): # 1 is immediate mode
            param2 = self.ints[self.pc + 2]

        param3 = self.ints[self.pc + 3] # always position mode
        self.ints[param3] = param1 + param2
        self.pc += 4

    def oc_mult(self, oc):

        if (oc.param1_mode == 0): # 0 is position mode
            param1 = self.ints[self.ints[self.pc + 1]] # dereference
        elif (oc.param1_mode == 1): # 1 is immediate mode
            param1 = self.ints[self.pc + 1]

        if (oc.param2_mode == 0): # 0 is position mode
            param2 = self.ints[self.ints[self.pc + 2]]
        elif (oc.param2_mode == 1): # 1 is immediate mode
            param2 = self.ints[self.pc + 2]

        param3 = self.ints[self.pc + 3] # always position mode
        self.ints[param3] = param1 * param2
        self.pc += 4


    def oc_input(self, oc):

        if (self._input_instruction == 0):
            input_value = self._phase
        elif (self._input_instruction == 1):
            input_value = self._input_value
        # input_value = input('Enter input')
        self._input_instruction += 1
        self.ints[self.ints[self.pc+1]] = int(input_value)
        self.pc += 2

    def oc_output(self, oc):
        if oc.param1_mode == 0:
            test_result = self.ints[self.ints[self.pc+1]]
        elif oc.param1_mode == 1:
            test_result = self.ints[self.pc+1]
        self.output = test_result
        # print(f'Test: {test_result}')
        self.pc += 2

    def oc_jmpT(self, oc):
        if (oc.param1_mode == 0): # 0 is position mode
            param1 = self.ints[self.ints[self.pc + 1]] # dereference
        elif (oc.param1_mode == 1): # 1 is immediate mode
            param1 = self.ints[self.pc + 1]

        if (oc.param2_mode == 0): # 0 is position mode
            param2 = self.ints[self.ints[self.pc + 2]]
        elif (oc.param2_mode == 1): # 1 is immediate mode
            param2 = self.ints[self.pc + 2]

        if param1 != 0:
            self.pc = param2
        else:
            self.pc += 2

    def oc_jmpF(self, oc):
        if (oc.param1_mode == 0): # 0 is position mode
            param1 = self.ints[self.ints[self.pc + 1]] # dereference
        elif (oc.param1_mode == 1): # 1 is immediate mode
            param1 = self.ints[self.pc + 1]

        if (oc.param2_mode == 0): # 0 is position mode
            param2 = self.ints[self.ints[self.pc + 2]]
        elif (oc.param2_mode == 1): # 1 is immediate mode
            param2 = self.ints[self.pc + 2]

        if param1 == 0:
            self.pc = param2
        else:
            self.pc += 3

    def oc_lt(self, oc):
        if (oc.param1_mode == 0): # 0 is position mode
            param1 = self.ints[self.ints[self.pc + 1]] # dereference
        elif (oc.param1_mode == 1): # 1 is immediate mode
            param1 = self.ints[self.pc + 1]

        if (oc.param2_mode == 0): # 0 is position mode
            param2 = self.ints[self.ints[self.pc + 2]]
        elif (oc.param2_mode == 1): # 1 is immediate mode
            param2 = self.ints[self.pc + 2]

        param3 = self.ints[self.pc+3]

        if param1 < param2:
            self. ints[param3] = 1
        else:
            self.ints[param3] = 0
        
        self.pc += 4

    def oc_eq(self, oc):
        if (oc.param1_mode == 0): # 0 is position mode
            param1 = self.ints[self.ints[self.pc + 1]] # dereference
        elif (oc.param1_mode == 1): # 1 is immediate mode
            param1 = self.ints[self.pc + 1]

        if (oc.param2_mode == 0): # 0 is position mode
            param2 = self.ints[self.ints[self.pc + 2]]
        elif (oc.param2_mode == 1): # 1 is immediate mode
            param2 = self.ints[self.pc + 2]

        param3 = self.ints[self.pc+3]

        if param1 == param2:
            self.ints[param3] = 1
        else:
            self.ints[param3] = 0
        
        self.pc += 4

    def oc_halt(self, oc):
        raise ProgramTerminatedError()


    def run_instruction(self):
        # returns length of instruction executed, or -1 to halt program execution
        oc = Opcode(self.ints, self.pc)
        self._opcodes[oc.opcode](oc)

    def run_to_end(self):
        while(self.pc < len(self.ints)):
            # print(f'Program Counter: {pc}')
            try:
                self.run_instruction()
            except ProgramTerminatedError:
                break


    def load_memory(self, file):
        f = open(file)
        line = f.readlines()[0].strip()
        ints_str = line.split(',')
        ints = [int(x) for x in ints_str]
        return ints

amp_settings = list(permutations(range(0, 5)))

outputs = []
for amp_setting in amp_settings:

    ampA = IntCodeComputer(amp_setting[0], 0)
    ampA.run_to_end()
    ampB = IntCodeComputer(amp_setting[1], ampA.output)
    ampB.run_to_end()
    ampC = IntCodeComputer(amp_setting[2], ampB.output)
    ampC.run_to_end()
    ampD = IntCodeComputer(amp_setting[3], ampC.output)
    ampD.run_to_end()
    ampE = IntCodeComputer(amp_setting[4], ampD.output)
    ampE.run_to_end()
    outputs.append(ampE.output)
    
max_output = [0,0]
for index, value in enumerate(outputs):
    if value > max_output[0]:
        max_output[0] = value
        max_output[1] = index
max_amp_settings = amp_settings[max_output[1]]
print(f'Max Output = {max_output[0]}. Using Settings: {max_amp_settings}')