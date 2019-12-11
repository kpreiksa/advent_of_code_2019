
from itertools import permutations 
import time

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
        for index in range(0,3):
            param_info = {}
            param_info['supported'] = True
            mode = int(self._inst_string[-3 - index])
            param_info['mode'] = mode
            param_info['addr'] = self._address + index + 1            
            self._params[index] = param_info
        
    @property
    def opcode(self):
        return int(self._inst_string[-2:])

    @property
    def address(self):
        return self._address

    def get_param(self, index, mem, rel_base, mode = None):
        param_info = self._params[index]
        if not mode:
            mode = param_info['mode']
        if (mode == 0):
            return mem[mem[param_info['addr']]]
        elif (mode == 1): # if mode is immediate OR param type is output... 
            return mem[param_info['addr']]
        else:
            return mem[mem[param_info['addr']] + rel_base]

    def set_param(self, index, mem, value, rel_base):
        param_info = self._params[index]
        if(param_info['mode'] == 0):
            mem[mem[param_info['addr']]] = value
        elif(param_info['mode'] == 1):
            raise ValueError('Got immediate mode for output')
        else:
            mem[mem[param_info['addr']] + rel_base] = value

class IntCodeMemory():
    def __init__(self, file):
        self._mem_dict = {}
        self.load(file)

    def __len__(self):
        return len(self._mem_dict)

    def _get_max_addr(self):
        return max(self._mem_dict.keys())

    def __setitem__(self, key, item):
        self._mem_dict[key] = item
        for i in range(0,self._get_max_addr() + 1):
            if i not in self._mem_dict.keys():
                self._mem_dict[i] = 0 

    def __getitem__(self, key):
        if key in self._mem_dict:
            return self._mem_dict[key]
        else:
            return 0

    def load(self, file):
        f = open(file)
        line = f.readlines()[0].strip()
        ints_str = line.split(',')
        ints = [int(x) for x in ints_str]
        self._mem_dict = {index: initial_value for index, initial_value in enumerate(ints)}

class IntCodeComputer():
    def __init__(self):
        self._output = 0
        self._output_available = False
        self.pc = 0 # program counter
        self._rel_base = 0
        self._input_instruction = 0
        self._input_value = None
        self._halted = False
        self._opcodes = {
            1: self.oc_add,
            2: self.oc_mult,
            3: self.oc_input,
            4: self.oc_output,
            5: self.oc_jmpT,
            6: self.oc_jmpF,
            7: self.oc_lt,
            8: self.oc_eq,
            9: self.oc_arb,
            99:self.oc_halt,
        }
        self.mem = IntCodeMemory('input.txt')

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
        param1 = oc.get_param(0, self.mem, self._rel_base)
        param2 = oc.get_param(1, self.mem, self._rel_base)
        oc.set_param(2, self.mem, param1 + param2, self._rel_base)
        self.pc += 4

    def oc_mult(self, oc):
        param1 = oc.get_param(0, self.mem, self._rel_base)
        param2 = oc.get_param(1, self.mem, self._rel_base)
        oc.set_param(2, self.mem, param1 * param2, self._rel_base)
        self.pc += 4

    def oc_input(self, oc):
        if(self._input_value == None):
            raise WaitingForInputError()
        input_value = self._input_value
        oc.set_param(0, self.mem, int(input_value), self._rel_base)
        self._input_value = None
        self.pc += 2

    def oc_output(self, oc):
        param1 = oc.get_param(0, self.mem, self._rel_base)
        self._output = param1
        print(f'Output: {param1}')
        self._output_available = True
        self.pc += 2

    def oc_jmpT(self, oc):
        param1 = oc.get_param(0, self.mem, self._rel_base)
        param2 = oc.get_param(1, self.mem, self._rel_base)
        if param1 != 0:
            self.pc = param2
        else:
            self.pc += 3

    def oc_jmpF(self, oc):
        param1 = oc.get_param(0, self.mem, self._rel_base)
        param2 = oc.get_param(1, self.mem, self._rel_base)
        if param1 == 0:
            self.pc = param2
        else:
            self.pc += 3

    def oc_lt(self, oc):
        param1 = oc.get_param(0, self.mem, self._rel_base)
        param2 = oc.get_param(1, self.mem, self._rel_base)
        if param1 < param2:
            oc.set_param(2, self.mem, 1, self._rel_base)
        else:
            oc.set_param(2, self.mem, 0, self._rel_base)
        self.pc += 4

    def oc_eq(self, oc):
        param1 = oc.get_param(0, self.mem, self._rel_base)
        param2 = oc.get_param(1, self.mem, self._rel_base)
        if param1 == param2:
            oc.set_param(2, self.mem, 1, self._rel_base)
        else:
            oc.set_param(2, self.mem, 0, self._rel_base)
        self.pc += 4

    def oc_arb(self, oc):
        param1 = oc.get_param(0, self.mem, self._rel_base)
        self._rel_base += param1
        self.pc += 2

    def oc_halt(self, oc):
        self._halted = True
        raise ProgramTerminatedError()

    def run_instruction(self):
        # returns length of instruction executed, or -1 to halt program execution
        oc = Opcode(self.mem, self.pc)
        oc_func = self._opcodes[oc.opcode]
        oc_func(oc)

    def run_to_end(self):
        while(self.pc < len(self.mem) and not self._halted):
            self.run_instruction()
            # print(f'Program Counter: {pc}')
            # try:
            #     self.run_instruction()
            # except ProgramTerminatedError:
            #     return -1
            # except WaitingForInputError:
            #     return -2


boost = IntCodeComputer()
boost.set_input(2)
try:
    boost.run_to_end()
except ProgramTerminatedError:
    print(boost.output)