import re

class Reaction():
    def __init__(self, string):
        self._inputs = []
        self._output = None

        lineSplit = line.split('=>',1)
        inputs = lineSplit[0].strip()
        inputs_list = inputs.split(',')
        inputs_list = [x.strip() for x in inputs_list]
        for next_input in inputs_list:
            quantity_and_chemical = next_input.split(' ') # split on space
            this_input = (quantity_and_chemical[0], quantity_and_chemical[1])
            self._inputs.append(this_input)
    
        outputs = lineSplit[1].strip()
        quantity_and_chemical = outputs.split(' ') # split on space
        this_output = (quantity_and_chemical[0], quantity_and_chemical[1])
        self._output = this_output

    def __repr__(self):
        return f'{self._inputs} => {self._output}'

    @property
    def output(self):
        return self._output

    @property
    def inputs(self):
        return self._inputs


f = open('input.txt')
lines = f.readlines()

reactions = []

for line in lines:
    reactions.append(Reaction(line))

# Find the reaction for fuel
fuel_reaction = [x for x in reactions if x.output[1] == 'FUEL'][0]

inputs_needed = fuel_reaction.inputs