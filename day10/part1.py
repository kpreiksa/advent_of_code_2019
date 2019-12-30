import datetime

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

start_time = datetime.datetime.now()
f = open('input.txt')
lines = f.readlines()
lines = [line.strip() for line in lines]
line_lengths = [len(line) for line in lines]

if len(list(set(line_lengths))) != 1:
    raise ValueError('Line Lengths not equal')

asteroids = []

for row_index, row in enumerate(lines):
    for col_index, value in enumerate(row):
        if value == '#':
            asteroids.append([Point(col_index,row_index), 0])


for asteroid in asteroids:
    lines_to_others = []
    for asteroid2 in asteroids:
        if asteroid2[0] != asteroid[0]:
            lines_to_others.append(asteroid[0].getLineToOther(asteroid2[0]))

    valid_lines = []
    for line_to_other in lines_to_others:
        line_obscured = False
        for asteroid3 in asteroids:
            if asteroid3[0] != line_to_other.begin and asteroid3[0] != line_to_other.end:
                if line_to_other.PassesThroughPoint(asteroid3[0]):
                    line_obscured = True
        if not line_obscured:
            valid_lines.append(line_to_other)
    asteroid[1] = len(valid_lines)

max_visible = [0,0]
for asteroid in asteroids:
    if asteroid[1] > max_visible[1]:
        max_visible = asteroid
        
print(f'Maximum visible asteroids = {max_visible[1]} from location {max_visible[0]}')

end_time = datetime.datetime.now()
time_diff = end_time - start_time

print(f'Execution Time: {time_diff}')
