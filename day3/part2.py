import datetime

start_time = datetime.datetime.now()
f = open('input.txt')
lines = f.readlines()
wire1_path = lines[0].strip()
wire2_path = lines[1].strip()

wire1_paths = wire1_path.split(',')
wire2_paths = wire2_path.split(',')

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.point = (x, y)
    def __repr__(self):
        return(f'(X,Y) = ({self.x},{self.y})')
    def compute_manhattan_distance(self, other):
        delta_x = abs(self.x - other.x)
        delta_y = abs(self.y - other.y)
        return delta_x + delta_y

class LineSegment():
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.seg = (begin, end)
        self.x1 = begin.x
        self.y1 = begin.y
        self.x2 = end.x
        self.y2 = end.y
    def __repr__(self):
        return(f'({self.x1},{self.y1}) - ({self.x2},{self.y2})')

    def __len__(self):
        if self.x1 == self.x2:
            return abs(self.y2 - self.y1)
        elif self.y1 == self.y2:
            return abs(self.x2 - self.x1)

    def doesIntersect(self, otherLine):
        def orientation(A, B, C):
            value = ((B.y - A.y) * (C.x - B.x)) - ((B.x - A.x) * (C.y - B.y)) 
            if (value == 0):
                # print('colinear')
                return 0
            elif (value > 0):
                # print('clockwise')
                return 1
            elif (value < 0):
                # print('ccw')
                return 2

        l1o1 = orientation(self.begin, self.end, otherLine.begin)
        l1o2 = orientation(self.begin, self.end, otherLine.end)

        l2o1 = orientation(otherLine.begin, otherLine.end, self.begin)
        l2o2 = orientation(otherLine.begin, otherLine.end, self.end)

        does_intersect = (l1o1 != l1o2 and l2o2 != l2o1) or (l1o1 == 0 or l1o2 == 0 or l2o1 == 0 or l2o2 == 0)
        return does_intersect

    def doesIntersect2(self, otherLine):
        retdict = {}
        retdict['does_intersect'] = False
        retdict['point'] = None
        retdict['self_begin'] = self.begin
        retdict['self_end'] = self.end
        retdict['other_begin'] = otherLine.begin
        retdict['other_end'] = otherLine.end
        retdict['this_segment'] = self
        retdict['other_segment'] = otherLine
        retdict['length_from_self_beginning'] = 0
        retdict['length_from_other_beginning'] = 0
        if self.begin.y == self.end.y:
            horizontal_line_self = True
            vertical_line_self = False
        elif self.begin.x == self.end.x:
            horizontal_line_self = False
            vertical_line_self = True

        if otherLine.begin.y == otherLine.end.y:
            horizontal_line_other = True
            vertical_line_other = False
        elif otherLine.begin.x == otherLine.end.x:
            vertical_line_other = True 
            horizontal_line_other = False

        if horizontal_line_other == horizontal_line_self:
            # can't intersect
            return retdict
        elif vertical_line_other == vertical_line_self:
            # can't intersect
            return retdict
        else:

            if vertical_line_other:
                # print('This line = horizontal. Other line = vertical')
                x = otherLine.begin.x
                y = self.begin.y
                left_point = min([self.begin.x, self.end.x])
                right_point = max([self.begin.x, self.end.x])
                bottom_point = min([otherLine.begin.y, otherLine.end.y])
                top_point = max([otherLine.begin.y, otherLine.end.y])
                if x > left_point and x < right_point:
                    if y > bottom_point and y < top_point:
                        retdict['does_intersect'] = True
                        retdict['point'] = Point(x,y)
                        retdict['length_from_self_beginning'] = Point(x,y).compute_manhattan_distance(self.begin)
                        retdict['length_from_other_beginning'] = Point(x,y).compute_manhattan_distance(otherLine.begin)
                        return retdict
                    else:
                        return retdict
                else:
                    return retdict

            if vertical_line_self:
                # print('This line = vertical. Other line = horizontal')
                left_point = min([otherLine.begin.x, otherLine.end.x])
                right_point = max([otherLine.begin.x, otherLine.end.x])
                bottom_point = min([self.begin.y, self.end.y])
                top_point = max([self.begin.y, self.end.y])
                x = self.begin.x
                y = otherLine.begin.y
                if x > left_point and x < right_point:
                    if y > bottom_point and y < top_point:
                        retdict['does_intersect'] = True
                        retdict['point'] = Point(x,y)
                        retdict['length_from_self_beginning'] = Point(x,y).compute_manhattan_distance(self.begin)
                        retdict['length_from_other_beginning'] = Point(x,y).compute_manhattan_distance(otherLine.begin)
                        return retdict
                    else:
                        return retdict
                else:
                    return retdict


wire1_verticies = [Point(0, 0)]
wire2_verticies = [Point(0, 0)]

for path in wire1_paths:
    if(path.startswith('U')):
        up = int(path.strip('U'))
        previous_point = wire1_verticies[-1]
        wire1_verticies.append(Point(previous_point.x, previous_point.y + up))
    elif(path.startswith('D')):
        down = int(path.strip('D'))
        previous_point = wire1_verticies[-1]
        wire1_verticies.append(
            Point(previous_point.x, previous_point.y - down))
    elif(path.startswith('L')):
        left=int(path.strip('L'))
        previous_point=wire1_verticies[-1]
        wire1_verticies.append(
            Point(previous_point.x - left, previous_point.y))
    elif(path.startswith('R')):
        right=int(path.strip('R'))
        previous_point=wire1_verticies[-1]
        wire1_verticies.append(
            Point(previous_point.x + right, previous_point.y))


for path in wire2_paths:
    if(path.startswith('U')):
        up=int(path.strip('U'))
        previous_point=wire2_verticies[-1]
        wire2_verticies.append(Point(previous_point.x, previous_point.y + up))
    elif(path.startswith('D')):
        down=int(path.strip('D'))
        previous_point=wire2_verticies[-1]
        wire2_verticies.append(
            Point(previous_point.x, previous_point.y - down))
    elif(path.startswith('L')):
        left=int(path.strip('L'))
        previous_point=wire2_verticies[-1]
        wire2_verticies.append(
            Point(previous_point.x - left, previous_point.y))
    elif(path.startswith('R')):
        right=int(path.strip('R'))
        previous_point=wire2_verticies[-1]
        wire2_verticies.append(
            Point(previous_point.x + right, previous_point.y))

wire1_line_segments=[]
wire2_line_segments=[]
for vertex_index in range(0, len(wire1_verticies) - 1):
    line_segment=LineSegment(
        wire1_verticies[vertex_index], wire1_verticies[vertex_index+1])
    wire1_line_segments.append(line_segment)

for vertex_index in range(0, len(wire2_verticies) - 1):
    line_segment = LineSegment(
        wire2_verticies[vertex_index], wire2_verticies[vertex_index+1])
    wire2_line_segments.append(line_segment)


intersections = []
for line_segment_1 in wire1_line_segments:
    for line_segment_2 in wire2_line_segments:
        intersection = line_segment_1.doesIntersect2(line_segment_2)
        if intersection['does_intersect'] != False:
            print(intersection)
            intersections.append(intersection)

for intersection in intersections:
    distance_to_origin = intersection['point'].compute_manhattan_distance(Point(0,0))
    print(f'Distance to origin: {distance_to_origin}')


for intersection in intersections:
    length_traveled_1 = 0
    length_traveled_2 = 0
    index_of_intersecting_segment_1 = wire1_line_segments.index(intersection['this_segment'])
    for segment in wire1_line_segments[0:index_of_intersecting_segment_1]:
        length_traveled_1 += len(segment)
    length_traveled_1 += intersection['length_from_self_beginning']
    index_of_intersecting_segment_2 = wire2_line_segments.index(intersection['other_segment'])
    for segment in wire2_line_segments[0:index_of_intersecting_segment_2]:
        length_traveled_2 += len(segment)
    length_traveled_2 += intersection['length_from_other_beginning']
    intersection['length_from_origin_1'] = length_traveled_1
    intersection['length_from_origin_2'] = length_traveled_2
# for intersection in intersections:
    
minimum_total_distance = [9999999999999999, 0]
for index, intersection in enumerate(intersections):
    total_distance = intersection['length_from_origin_1'] + intersection['length_from_origin_2']
    if total_distance < minimum_total_distance[0]:
        minimum_total_distance[0] = total_distance
        minimum_total_distance[1] = index

print(minimum_total_distance)

end_time = datetime.datetime.now()
time_diff = end_time - start_time

print(f'Execution Time: {time_diff}')

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
