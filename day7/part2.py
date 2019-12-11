
from itertools import permutations 
import time


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

    def param1_value(self, mem, mode = None):
        if not mode:
            mode = self.param1_mode

        if (mode == 0):
            return mem[mem[self.param1_addr]]

        elif (mode == 1): 
            return mem[self.param1_addr]

    def param2_value(self, mem, mode = None):
        if not mode:
            mode = self.param2_mode

        if (mode == 0):
            return mem[mem[self.param2_addr]]

        elif (mode == 1): 
            return mem[self.param2_addr]

    def param3_value(self, mem, mode = None):
        return mem[self.param3_addr]

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
    def __init__(self):
        self._output = 0
        self._output_available = False
        self.ints = self.load_memory('input.txt')
        self.pc = 0 # program counter
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
            99:self.oc_halt,
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
        param3 = oc.param3_value(self.ints, mode = 1)
        self.ints[param3] = param1 + param2
        self.pc += 4

    def oc_mult(self, oc):
        param1 = oc.param1_value(self.ints)
        param2 = oc.param2_value(self.ints)
        param3 = oc.param3_value(self.ints, mode = 1)
        self.ints[param3] = param1 * param2
        self.pc += 4

    def oc_input(self, oc):
        param1 = oc.param1_value(self.ints, mode = 1)
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
        param3 = oc.param3_value(self.ints, mode = 1)
        if param1 < param2:
            self.ints[param3] = 1
        else:
            self.ints[param3] = 0
        self.pc += 4

    def oc_eq(self, oc):
        param1 = oc.param1_value(self.ints)
        param2 = oc.param2_value(self.ints)
        param3 = oc.param3_value(self.ints, mode = 1)
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
        self._opcodes[oc.opcode](oc)

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


amp_settings = list(permutations(range(5, 10)))

outputs = []

# amp_setting = amp_settings[0]

# amp_settings = []
# amp_settings.append(amp_setting)


for amp_setting_index, amp_setting in enumerate(amp_settings):
    print('Running Iteration')
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
            print(f'Done setting up amp {index}')

    retcode = 0
    prev_out = 0

    while (retcode == 0):
        for index, amp in enumerate(amps):
            try:
                amp.set_input(prev_out)
                amp.run_to_end()
            except WaitingForInputError:
                pass
            except ProgramTerminatedError:
                retcode = -1
            finally:
                out = amp.output
                print(f'Final output = {out}')
                prev_out = out

        outputs.append((amp_setting_index, ampE.output))
        
max_output = [0,0]
for value in outputs:
    if value[1] > max_output[1]:
        max_output[1] = value[1]
        max_output[0] = value[0]

print(f'Max output = [{max_output[1]}] using amplifier settings: {amp_settings[max_output[0]]}')