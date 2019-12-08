
f = open('input.txt')
lines = f.readlines()
wire1_path = lines[0].strip()
wire2_path = lines[1].strip()

wire1_paths = wire1_path.split(',')
wire2_paths = wire2_path.split(',')

wire1_points_occupied = [(0,0)]
wire2_points_occupied = [(0,0)]

for path in wire1_paths:
    if(path.startswith('U')):
        up = int(path.strip('U'))
        previous_point = wire1_points_occupied[-1]
        for i in range(0,up+1):
            wire1_points_occupied.append((previous_point[0], previous_point[1] + i))
    elif(path.startswith('D')):
        down = int(path.strip('D'))
        previous_point = wire1_points_occupied[-1]
        for i in range(0,down+1):
            wire1_points_occupied.append((previous_point[0], previous_point[1] - i))
    elif(path.startswith('L')):
        left = int(path.strip('L'))
        previous_point = wire1_points_occupied[-1]
        for i in range(0,left+1):
            wire1_points_occupied.append((previous_point[0]-i, previous_point[1]))
    elif(path.startswith('R')):
        right = int(path.strip('R'))
        previous_point = wire1_points_occupied[-1]
        for i in range(0,right+1):
            wire1_points_occupied.append((previous_point[0]+i, previous_point[1]))


for path in wire2_paths:
    if(path.startswith('U')):
        up = int(path.strip('U'))
        previous_point = wire2_points_occupied[-1]
        for i in range(0,up+1):
            wire2_points_occupied.append((previous_point[0], previous_point[1] + i))
    elif(path.startswith('D')):
        down = int(path.strip('D'))
        previous_point = wire2_points_occupied[-1]
        for i in range(0,down+1):
            wire2_points_occupied.append((previous_point[0], previous_point[1] - i))
    elif(path.startswith('L')):
        left = int(path.strip('L'))
        previous_point = wire2_points_occupied[-1]
        for i in range(0,left+1):
            wire2_points_occupied.append((previous_point[0]-i, previous_point[1]))
    elif(path.startswith('R')):
        right = int(path.strip('R'))
        previous_point = wire2_points_occupied[-1]
        for i in range(0,right+1):
            wire2_points_occupied.append((previous_point[0]+i, previous_point[1]))

x_values_1 = list(set([point[0] for point in wire1_points_occupied])) 
min_x_value_1 = min(x_values_1)
max_x_value_1 = max(x_values_1)

x_values_2 = list(set([point[0] for point in wire2_points_occupied])) 
min_x_value_2 = min(x_values_2)
max_x_value_2 = max(x_values_2)

min_x_value = min([min_x_value_1, min_x_value_2])
max_x_value = max([max_x_value_1, max_x_value_2])

y_values = list(set([point[1] for point in wire1_points_occupied])) 
min_y_value_1 = min(y_values)
max_y_value_1 = max(y_values)

y_values_2 = list(set([point[0] for point in wire2_points_occupied])) 
min_y_value_2 = min(y_values_2)
max_y_value_2 = max(y_values_2)

min_y_value = min([min_y_value_1, min_y_value_2])
max_y_value = max([max_y_value_1, max_y_value_2])

wire1_x_points_occupied = [point[0] for point in wire1_points_occupied]
wire1_y_points_occupied = [point[1] for point in wire1_points_occupied]

wire2_x_points_occupied = [point[0] for point in wire2_points_occupied]
wire2_y_points_occupied = [point[1] for point in wire2_points_occupied]

wire1_unique_points_occupied = list(set(wire1_points_occupied))
wire2_unique_points_occupied = list(set(wire2_points_occupied))

x_intersections = []
iterations = 0

def slope(x1,y1,x2,y2):
    rise = y2-y1
    run = x2-x1
    return (rise/run)

# import time

# previous_time = time.time()

# for point in wire1_unique_points_occupied:
#     iterations += 1
#     current_time = time.time()
#     elapsed_time = current_time-previous_time
#     remaining_time = (len(wire1_unique_points_occupied) - iterations) * elapsed_time
#     print(f'Iteration {iterations}/{len(wire1_unique_points_occupied)}')
#     print(f'Time for last iteration: {elapsed_time}')
#     print(f'Estimated time remaining: {remaining_time}')
#     previous_time = time.time()
#     for point2 in wire2_unique_points_occupied:
#         if point[0] == point2[0] and point[1] == point2[1]:
#             x_intersections.append(point[0])
        
