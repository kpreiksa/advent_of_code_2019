import math

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.point = (x, y)
    def __repr__(self):
        return(f'(X,Y) = ({self.x},{self.y})')

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def getLineToOther(self, other):
        ls = LineSegment(self, other)
        return ls

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

    def angle(self, offset = 0):
        rise = self.end.y - self.begin.y
        run = self.end.x - self.begin.x
        theta_radians = math.atan2(rise, run)
        theta_degrees = theta_radians * (180 / math.pi)
        if (theta_degrees < 0):
            theta_degrees = 180 + abs(abs(theta_degrees) - 180)
        
        theta_degrees = theta_degrees - offset
        if (theta_degrees < 0):
            theta_degrees = abs(abs(theta_degrees) - 360)
        # else:
        #     theta_degrees = theta_degrees + offset
        return theta_degrees

    def PassesThroughPoint(self, point):
        a = self.begin
        b = self.end
        c = point
        crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

        # compare versus epsilon for floating point values, or != 0 if using integers
        if abs(crossproduct) > 0.000001:
            return False

        dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
        if dotproduct < 0:
            return False

        squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
        if dotproduct > squaredlengthba:
            return False

        return True


f = open('input.txt')
lines = f.readlines()
lines = [line.strip() for line in lines]
line_lengths = [len(line) for line in lines]

if len(list(set(line_lengths))) != 1:
    raise ValueError('Line Lengths not equal')

asteroids = []
all_lines_to_others = []
destruction_index = []

for row_index, row in enumerate(lines):
    for col_index, value in enumerate(row):
        if value == '#':
            asteroids.append(Point(col_index,row_index))
            all_lines_to_others.append(None)
            destruction_index.append(999999999999)

# FIND BEST STATION - START

for index, asteroid in enumerate(asteroids):
    lines_to_others = []
    for asteroid2 in asteroids:
        if asteroid2 != asteroid:
            lines_to_others.append(asteroid.getLineToOther(asteroid2))

    valid_lines = []
    for line_to_other in lines_to_others:
        line_obscured = False
        for asteroid3 in asteroids:
            if asteroid3 != line_to_other.begin and asteroid3 != line_to_other.end:
                if line_to_other.PassesThroughPoint(asteroid3):
                    line_obscured = True
        if not line_obscured:
            valid_lines.append(line_to_other)
    all_lines_to_others[index] = valid_lines

max_visible = [0,0, None]
for index, asteroid in enumerate(asteroids):
    if len(all_lines_to_others[index]) > max_visible[1]:
        max_visible[0] = asteroid
        max_visible[1] = len(all_lines_to_others[index])
        max_visible[2] = all_lines_to_others[index]

blast_station = max_visible[0]

# FIND BEST STATION - END

# USE BEST STATION - START

# blast_station = Point(17,22)

# USE BEST STATION - END

blast_station_lines = []

destruction_count = 0

_200th_destroyed = 0

while len(asteroids) > 1:

    lines_to_others = []
    for asteroid in asteroids:
        if asteroid != blast_station:
            lines_to_others.append(blast_station.getLineToOther(asteroid))

    valid_lines = []
    for line_to_other in lines_to_others:
        line_obscured = False
        for asteroid in asteroids:
            if asteroid != line_to_other.begin and asteroid != line_to_other.end:
                if line_to_other.PassesThroughPoint(asteroid):
                    line_obscured = True
        if not line_obscured:
            valid_lines.append(line_to_other)
    blast_station_lines = valid_lines

    angle = 270

    current_asteroid_paths = blast_station_lines
    current_asteroid_paths = sorted(current_asteroid_paths, key= lambda path: path.angle(angle))  
    for index, current_asteroid_path in enumerate(current_asteroid_paths):
        print(f'Removing asteroid at {current_asteroid_path.end}')
        destruction_count += 1
        if destruction_count == 200:
            _200th_destroyed = (current_asteroid_path.end.x * 100) + current_asteroid_path.end.y

        asteroids.remove(current_asteroid_path.end) # KILL IT
    



