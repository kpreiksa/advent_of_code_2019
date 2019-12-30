import datetime

start_time = datetime.datetime.now()
f = open('input.txt')
line = f.readlines()[0].strip()

image_width = 25
image_height = 6

layer_size = image_height * image_width

num_layers = int(len(line) / layer_size)

starting_offset = 0

layers = []
for layer in range(0, num_layers):
    rows = []
    for row in range(0, image_height):
        # print(f'Offset:')
        row_values = [int(x) for x in line[starting_offset:starting_offset+25]]
        # print(f'Row{row}. Values = {row_values}')
        rows.append(row_values)
        starting_offset += 25
    layers.append(rows)

count_zeros = []
for layer_index in range(0,len(layers)):
    count_zeros_layer = 0
    rows = layers[layer_index]
    for row in rows:
        for value in row:
            if value == 0:
                count_zeros_layer += 1
    count_zeros.append(count_zeros_layer)

layer_with_least_zeros = 0
for index,number_of_zeros in enumerate(count_zeros):
    if number_of_zeros < count_zeros[layer_with_least_zeros]:
        layer_with_least_zeros = index

layer_to_analyze = layers[layer_with_least_zeros]
number_of_ones = 0
number_of_twos = 0
for row in layer_to_analyze:
    for integer_value in row:
        if integer_value == 1:
            number_of_ones += 1
        elif integer_value == 2:
            number_of_twos += 1
    
print(f'Number of 1s: {number_of_ones}. Number of 2s: {number_of_twos}. Total = {number_of_ones * number_of_twos}')

end_time = datetime.datetime.now()
time_diff = end_time - start_time

print(f'Execution Time: {time_diff}')