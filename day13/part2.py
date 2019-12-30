
from itertools import permutations 
import time
from PIL import Image
from pynput import keyboard
import datetime

class Tile():

    class TileType():
        EmptyTile = 0
        WallTile = 1
        BlockTile = 2
        HorizontalPaddleTile = 3
        BallTile = 4

    def __init__(self):
        # print('Creating Tile')
        self._type = 0 

    def __repr__(self):
        if self._type == Tile.TileType.EmptyTile:
            return ' '
        elif self._type == Tile.TileType.WallTile:
            return '|'
        elif self._type == Tile.TileType.BlockTile:
            return '#'
        elif self._type == Tile.TileType.HorizontalPaddleTile:
            return '_'
        elif self._type == Tile.TileType.BallTile:
            return 'O'
        else:
            return '?'

    def __str__(self):
        return self.__repr__()

    def setType(self, newType):
        self._type = newType

    def getType(self):
        return self._type

class Screen():
    def __init__(self, x, y):
        self._width = x
        self._height = y

        self._tiles = []
        
        for row in range(0, y):
            row_tiles = []
            for col in range(0, x):
                row_tiles.append(Tile())
            self._tiles.append(row_tiles)

    def __repr__(self):
        str_repr = ''
        for row in self._tiles:
            for panel in row:
                str_repr += str(panel)
            str_repr += '\n'
        return str_repr

    def countTiles(self, typeToCheck):
        countTiles = 0
        for row in self._tiles:
            for col in row:
                if col._type == typeToCheck:
                    countTiles += 1
        return countTiles

    def getBallX(self):
        for indexY, row in enumerate(self._tiles):
            for indexX, col in enumerate(row):
                if col.getType() == Tile.TileType.BallTile:
                    return indexX

    def getPaddleX(self):
        for indexY, row in enumerate(self._tiles):
            for indexX, col in enumerate(row):
                if col.getType() == Tile.TileType.HorizontalPaddleTile:
                    return indexX

    def addTile(self, x, y, tileType):
        tileTypeStr = ''
        if tileType == Tile.TileType.EmptyTile:
            tileTypeStr = 'Empty Tile'
        elif tileType == Tile.TileType.BallTile:
            tileTypeStr = 'Ball Tile'
        elif tileType == Tile.TileType.BlockTile:
            tileTypeStr = 'Block Tile'
        elif tileType == Tile.TileType.HorizontalPaddleTile:
            tileTypeStr = 'Horizonal Paddle Tile'
        elif tileType == Tile.TileType.WallTile:
            tileTypeStr = 'Wall Tile'

        # print(f'Adding {tileTypeStr} at x:{x} y:{y}')

        if len(self._tiles) > y:
            if len(self._tiles[y]) > x:
                self._tiles[y][x].setType(tileType)
            else:
                # have to add columns
                cols_to_add = x - len(self._tiles[y]) + 1
                for col in range(0, cols_to_add):
                    self._tiles[y].append(Tile())
                self._tiles[y][x].setType(tileType)
        else:
            # print('Adding Tiles')
            rows_to_add = y - len(self._tiles) + 1
            for row in range(0, rows_to_add):
                width = len(self._tiles[-1])
                col_tiles = []
                for col in range(0, width + 1):
                    col_tiles.append(Tile())
                self._tiles.append(col_tiles)
            self._tiles[y][x].setType(tileType)

    def toImage(self, filename):
        image_raw_data = []
        for row in self._tiles:
            for panel in row:
                if(panel.color == 0):
                    image_raw_data.append((0,0,0)) # black
                else:
                    image_raw_data.append((255,255,255)) # white
        im= Image.new('RGB', (self._width, self._height))
        im.putdata(image_raw_data)
        im.save(filename)


class ProgramTerminatedError(Exception):
    pass

class WaitingForInputError(Exception):
    pass

class OutputReadyError(Exception):
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
        # Previously, I would resize the memory every time it was written to.
        # This was incredibly slow (see profiler results)
        
        # for i in range(0,self._get_max_addr() + 1):
        #     if i not in self._mem_dict.keys():
        #         self._mem_dict[i] = 0 

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
        self.mem = IntCodeMemory('input_play.txt')

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
        self._output_available = True
        self.pc += 2
        raise OutputReadyError()


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


start_time = datetime.datetime.now()

icc = IntCodeComputer()
arcadeScreen = Screen(10,10)
paddle_known = False
paddle_x = 0

outputs_ready = 0
outputs_buffer = {}
move_counter = 0
total_score = 0
while True:
    try:
        icc.run_to_end()
    except OutputReadyError:
        outputs_buffer[outputs_ready] = icc.output
        outputs_ready += 1
        if outputs_ready == 3:
            # print(f'{outputs_buffer[0]} {outputs_buffer[1]} {outputs_buffer[2]}')
            outputs_ready = 0
            if outputs_buffer[0] == -1 and outputs_buffer[1] == 0:
                score = outputs_buffer[2]
                # print(f'Score: {score}')
                # print(arcadeScreen)
                total_score = score
            else:
                arcadeScreen.addTile(outputs_buffer[0], outputs_buffer[1], outputs_buffer[2])
            outputs_buffer = {}
    except WaitingForInputError:
        # print(f'Score: {score}')
        # print(arcadeScreen)
        ball_x = arcadeScreen.getBallX()
        if not paddle_known:
            paddle_x = arcadeScreen.getPaddleX()
            paddle_known = True
        
        # print(f'Ball is at: {arcadeScreen.getBallX()}. Paddle is at: {arcadeScreen.getPaddleX()}')

        if ball_x < paddle_x:
            # move left
            # print('moving left')
            paddle_x = paddle_x - 1
            icc.set_input(-1)
        elif ball_x > paddle_x:
            # move right
            # print('moving right')
            paddle_x = paddle_x + 1
            icc.set_input(1)
        else:
            icc.set_input(0)
        move_counter += 1

        
        # key_pressed = input()
        # if key_pressed == 'a':
        #     icc.set_input(-1)
        # elif key_pressed == 'd':
        #     icc.set_input(1)
        # else:
        #     icc.set_input(0)


        # while True:
        #     if keyboard.read_key() == "a":
        #         print("You pressed a")
        #         icc.set_input(-1)
        #         break
        #     if keyboard.read_key() == "d":
        #         print("You pressed d")
        #         icc.set_input(1)
        #         break
        #     if keyboard.read_key() == 's':
        #         print("You pressed s")
        #         icc.set_input(0)
        #         break
    except ProgramTerminatedError:
        break

end_time = datetime.datetime.now()
time_diff = end_time - start_time

print(f'Completed game in {time_diff} with score of {total_score} in {move_counter} moves')
        