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

decoded_image = [[2 for x in range(0,image_width)] for x in range(0,image_height)]  # start with fully transparent layer
for layer in range(0, num_layers):
    for row in range(0, image_height):
        for current_value in range(0, image_width):
            if decoded_image[row][current_value] == 2:
                decoded_image[row][current_value] = layers[layer][row][current_value]


image_raw_data = []
for row in decoded_image:
    for current_value in row:
        if(current_value == 0):
            image_raw_data.append((0,0,0)) # black
        else:
            image_raw_data.append((255,255,255)) # white

from PIL import Image
im= Image.new('RGB', (25, 6))
im.putdata(image_raw_data)
im.save('test.png')

end_time = datetime.datetime.now()
time_diff = end_time - start_time

print(f'Execution Time: {time_diff}')