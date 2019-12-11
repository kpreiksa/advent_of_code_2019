
from itertools import permutations

class ProgramTerminatedError(Exception):
    pass

class WaitingForInputError(Exception):
    pass

class Opcode():
    def __init__(self, ints, pc):
        ''' Starting with an integer, generate the opcode obj '''
        self._raw_opcode = ints[pc]
        self._address = pc
        self._inst_string = f'{self._raw_opcode:#05}' # 5 = max number of digits for an instruction
        self._params = [{'supported': False}] * 3

    def set_param_info(self, param_info):
        for index, value in enumerate(param_info):
            param_info = {}
            param_info['supported'] = True
            param_info['mode'] = 'UNKNOWN'
            param_info['addr'] = self._address + index + 1
            if value == 1:
                param_info['type'] = 'OUTPUT'
                mode = int(self._inst_string[-3 - index])
                if mode != 1: # don't allow immediate mode for output
                    param_info['mode'] = mode
                else:
                    param_info['mode'] = 0
            elif value == 0:
                param_info['type'] = 'INPUT'
                mode = int(self._inst_string[-3 - index])
                param_info['mode'] = mode
            
            self._params[index] = param_info

        
    @property
    def opcode(self):
        return int(self._inst_string[-2:])

    def param1_value(self, mem, mode = None):
        param_info = self._params[0]

        if (param_info['mode'] == 0 and param_info['type'] != 'OUTPUT'):
            return mem[mem[param_info['addr']]]

        else: # if mode is immediate OR param type is output... 
            return mem[param_info['addr']]

    def param2_value(self, mem, mode = None):
        param_info = self._params[1]
 
        if (param_info['mode'] == 0 and param_info['type'] != 'OUTPUT'):
            return mem[mem[param_info['addr']]]

        else: # if mode is immediate OR param type is output... 
            return mem[param_info['addr']]

    def param3_value(self, mem, mode = None):
        param_info = self._params[2]
        return mem[param_info['addr']]

    @property
    def address(self):
        return self._address


class IntCodeComputer():
    def __init__(self):
        self._output = 0
        self._output_available = False
        self.ints = self.load_memory('input.txt')
        self.pc = 0 # program counter
        self._input_instruction = 0
        self._input_value = None
        self._halted = False
        self._opcodes = {
            1: (self.oc_add, [0,0,1]),
            2: (self.oc_mult, [0,0,1]),
            3: (self.oc_input, [1]),
            4: (self.oc_output, [0]),
            5: (self.oc_jmpT, [0,0]),
            6: (self.oc_jmpF, [0,0]),
            7: (self.oc_lt, [0,0,1]),
            8: (self.oc_eq, [0,0,1]),
            99:(self.oc_halt, []),
        }

    def set_input(self, in_value):
        self._input_value = in_value

    @property
    def output(self):
        if self._output_available:
            return self._output
        else:
            return None

    @property
    def output_available(self):
        return self._output_available

    def oc_add(self, oc):
        param1 = oc.param1_value(self.ints)
        param2 = oc.param2_value(self.ints)
        param3 = oc.param3_value(self.ints)
        self.ints[param3] = param1 + param2
        self.pc += 4

    def oc_mult(self, oc):
        param1 = oc.param1_value(self.ints)
        param2 = oc.param2_value(self.ints)
        param3 = oc.param3_value(self.ints)
        self.ints[param3] = param1 * param2
        self.pc += 4

    def oc_input(self, oc):
        param1 = oc.param1_value(self.ints)
        if(self._input_value == None):
            raise WaitingForInputError()
        input_value = self._input_value
        self.ints[param1] = int(input_value)
        self._input_value = None
        self.pc += 2

    def oc_output(self, oc):
        param1 = oc.param1_value(self.ints)
        self._output = param1
        self._output_available = True
        self.pc += 2

    def oc_jmpT(self, oc):
        param1 = oc.param1_value(self.ints)
        param2 = oc.param2_value(self.ints)
        if param1 != 0:
            self.pc = param2
        else:
            self.pc += 2

    def oc_jmpF(self, oc):
        param1 = oc.param1_value(self.ints)
        param2 = oc.param2_value(self.ints)
        if param1 == 0:
            self.pc = param2
        else:
            self.pc += 3

    def oc_lt(self, oc):
        param1 = oc.param1_value(self.ints)
        param2 = oc.param2_value(self.ints)
        param3 = oc.param3_value(self.ints)
        if param1 < param2:
            self.ints[param3] = 1
        else:
            self.ints[param3] = 0
        self.pc += 4

    def oc_eq(self, oc):
        param1 = oc.param1_value(self.ints)
        param2 = oc.param2_value(self.ints)
        param3 = oc.param3_value(self.ints)
        if param1 == param2:
            self.ints[param3] = 1
        else:
            self.ints[param3] = 0
        self.pc += 4

    def oc_halt(self, oc):
        self._halted = True
        raise ProgramTerminatedError()

    def run_instruction(self):
        # returns length of instruction executed, or -1 to halt program execution
        oc = Opcode(self.ints, self.pc)

        oc_func = self._opcodes[oc.opcode][0]
        oc_info = self._opcodes[oc.opcode][1]
        oc.set_param_info(oc_info)
        
        oc_func(oc)

    def run_to_end(self):
        while(self.pc < len(self.ints) and not self._halted):
            self.run_instruction()
            # print(f'Program Counter: {pc}')
            # try:
            #     self.run_instruction()
            # except ProgramTerminatedError:
            #     return -1
            # except WaitingForInputError:
            #     return -2

    def load_memory(self, file):
        f = open(file)
        line = f.readlines()[0].strip()
        ints_str = line.split(',')
        ints = [int(x) for x in ints_str]
        return ints

amp_settings = list(permutations(range(0, 5)))

outputs = []
for amp_setting in amp_settings:

    ampA = IntCodeComputer()
    ampB = IntCodeComputer()
    ampC = IntCodeComputer()
    ampD = IntCodeComputer()
    ampE = IntCodeComputer()

    amps = [ampA, ampB, ampC, ampD, ampE]

    for index, amp in enumerate(amps):
        try:
            amp.set_input(amp_setting[index])
            amp.run_to_end()
        except WaitingForInputError:
            pass

    prev_out = 0
    for index, amp in enumerate(amps):
        try:
            amp.set_input(prev_out)
            amp.run_to_end()
        except:
            prev_out = amp.output

    outputs.append(ampE.output)
    
max_output = [0,0]
for index, value in enumerate(outputs):
    if value > max_output[0]:
        max_output[0] = value
        max_output[1] = index
max_amp_settings = amp_settings[max_output[1]]
print(f'Max Output = {max_output[0]}. Using Settings: {max_amp_settings}')