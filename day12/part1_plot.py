import re
import matplotlib.pyplot as plt
import numpy as np


steps = 3000

class Moon():
    def __init__(self, x, y, z):
        self._x_pos = int(x)
        self._y_pos = int(y)
        self._z_pos = int(z)

        self._x_vel = 0
        self._y_vel = 0
        self._z_vel = 0

        self._x_grav = 0
        self._y_grav = 0
        self._z_grav = 0

    def __eq__(self, other):
        # return self._x_pos == other._x_pos and self._y_pos == other._y_pos and self._z_pos == other._z_pos
        return self.equalToOther(other)

    def equalToOther(self, other):
        positionsEqual = self._x_pos == other._x_pos and self._y_pos == other._y_pos and self._z_pos == other._z_pos
        velocitiesEqual = self._x_vel == other._x_vel and self._y_vel == other._y_vel and self._z_vel == other._z_vel
        return positionsEqual and velocitiesEqual

    def __repr__(self):
        retStr = f'Moon at position ({self._x_pos},{self._y_pos},{self._z_pos}) '
        retStr += f'with velocity ({self._x_vel},{self._y_vel},{self._z_vel}) '
        retStr += f'Energy = {self.getEnergy()}'
        return retStr

    def applyGravity(self, otherMoon):
        # print('Applying gravity')
        if (self._x_pos - otherMoon._x_pos) < 0:
            self._x_grav += 1
            otherMoon._x_grav -= 1
        elif (self._x_pos - otherMoon._x_pos) > 0:
            self._x_grav -= 1
            otherMoon._x_grav += 1

        if (self._y_pos - otherMoon._y_pos) < 0:
            self._y_grav += 1
            otherMoon._y_grav -= 1
        elif (self._y_pos - otherMoon._y_pos) > 0:
            self._y_grav -= 1
            otherMoon._y_grav += 1

        if (self._z_pos - otherMoon._z_pos) < 0:
            self._z_grav += 1
            otherMoon._z_grav -= 1
        elif (self._z_pos - otherMoon._z_pos) > 0:
            self._z_grav -= 1
            otherMoon._z_grav += 1

    def applyVelocity(self):
        self._x_vel = self._x_vel + self._x_grav
        self._y_vel = self._y_vel + self._y_grav
        self._z_vel = self._z_vel + self._z_grav

    def move(self):
        self._x_pos += self._x_vel
        self._y_pos += self._y_vel
        self._z_pos += self._z_vel

    def resetGravity(self):
        self._x_grav = 0
        self._y_grav = 0
        self._z_grav = 0


    def getEnergy(self):
        potEnergy = abs(self._x_pos) + abs(self._y_pos) + abs(self._z_pos)
        kinEnergy = abs(self._x_vel) + abs(self._y_vel) + abs(self._z_vel)
        return  potEnergy * kinEnergy



f = open('input.txt')
lines = f.readlines()

regex = r"<x=(?P<x>[0-9\-]+), y=(?P<y>[0-9\-]+), z=(?P<z>[0-9\-]+)>"

moons = []

for line in lines:
    moonRaw = line.strip()
    matches = re.search(regex, moonRaw, re.MULTILINE)
    moons.append(Moon(matches['x'], matches['y'], matches['z']))

moonPairs = []

for moon in moons:
    for secondMoon in moons:
        if moon != secondMoon:
            if (((moon, secondMoon) not in moonPairs) and (secondMoon, moon) not in moonPairs):
                moonPairs.append((moon,secondMoon))

initial_moons = []

for moon in moons:
    newmoon = Moon(moon._x_pos, moon._y_pos, moon._z_pos)
    newmoon._x_vel = moon._x_vel
    newmoon._y_vel = moon._y_vel
    newmoon._z_vel = moon._z_vel
    initial_moons.append(newmoon)

plot_data = []
# moon_matches_x_pos = {}
# moon_matches_y_pos = {}
# moon_matches_z_pos = {}

# moon_matches_x_vel = {}
# moon_matches_y_vel = {}
# moon_matches_z_vel = {}

moon_matches_x_pos = {}
moon_matches_y_pos = {}
moon_matches_z_pos = {}

moon_matches_x_vel = {}
moon_matches_y_vel = {}
moon_matches_z_vel = {}

moon_match_x = 0
moon_match_y = 0
moon_match_z = 0

moon_matches_x = [[],[],[],[]]
moon_matches_y = [[],[],[],[]]
moon_matches_z = [[],[],[],[]]

i = 0
allMatched = False
while not allMatched:
    # step_data = {}
    for moonPair in moonPairs:
        moonPair[0].applyGravity(moonPair[1])

    for index, moon in enumerate(moons):
        moon.applyVelocity()
        moon.move()
        moon.resetGravity()
        # if moon._x_pos == initial_moons[index]._x_pos:
        #     if not index in moon_matches_x_pos:
        #         print('x_pos match')
        #         moon_matches_x_pos[index] = i+1

        # if moon._y_pos == initial_moons[index]._y_pos:
        #     if not index in moon_matches_y_pos:
        #         print('y_pos match')
        #         moon_matches_y_pos[index] = i+1

        # if moon._z_pos == initial_moons[index]._z_pos:
        #     if not index in moon_matches_z_pos:
        #         print('z_pos match')
        #         moon_matches_z_pos[index] = i+1

        # if moon._x_vel == initial_moons[index]._x_vel:
        #     if not index in moon_matches_x_vel:
        #         print('x_vel match')
        #         moon_matches_x_vel[index] = i+1

        # if moon._y_vel == initial_moons[index]._y_vel:
        #     if not index in moon_matches_y_vel:
        #         print('y_vel match')
        #         moon_matches_y_vel[index] = i+1

        # if moon._z_vel == initial_moons[index]._z_vel:
        #     if not index in moon_matches_z_vel:
        #         print('z_vel match')
        #         moon_matches_z_vel[index] = i+1
    m0_x_eq = moons[0]._x_pos == initial_moons[0]._x_pos and moons[0]._x_vel == initial_moons[0]._x_vel
    m1_x_eq = moons[1]._x_pos == initial_moons[1]._x_pos and moons[1]._x_vel == initial_moons[1]._x_vel
    m2_x_eq = moons[2]._x_pos == initial_moons[2]._x_pos and moons[2]._x_vel == initial_moons[2]._x_vel
    m3_x_eq = moons[3]._x_pos == initial_moons[3]._x_pos and moons[3]._x_vel == initial_moons[3]._x_vel

    if m0_x_eq:
        moon_matches_x[0].append(i+1)
    if m1_x_eq:
        moon_matches_x[1].append(i+1)
    if m2_x_eq:
        moon_matches_x[2].append(i+1)
    if m3_x_eq:
        moon_matches_x[3].append(i+1)

    if m0_x_eq and m1_x_eq and m2_x_eq and m3_x_eq and moon_match_x == 0:
        moon_match_x = i+1
        print(f'X eq at index {i+1}')

    m0_y_eq = moons[0]._y_pos == initial_moons[0]._y_pos and moons[0]._y_vel == initial_moons[0]._y_vel
    m1_y_eq = moons[1]._y_pos == initial_moons[1]._y_pos and moons[1]._y_vel == initial_moons[1]._y_vel
    m2_y_eq = moons[2]._y_pos == initial_moons[2]._y_pos and moons[2]._y_vel == initial_moons[2]._y_vel
    m3_y_eq = moons[3]._y_pos == initial_moons[3]._y_pos and moons[3]._y_vel == initial_moons[3]._y_vel

    if m0_y_eq:
        moon_matches_y[0].append(i+1)
    if m1_y_eq:
        moon_matches_y[1].append(i+1)
    if m2_y_eq:
        moon_matches_y[2].append(i+1)
    if m3_y_eq:
        moon_matches_y[3].append(i+1)

    if m0_y_eq and m1_y_eq and m2_y_eq and m3_y_eq and moon_match_y == 0:
        moon_match_y = i+1
        print(f'Y eq and index {i+1}')

    m0_z_eq = moons[0]._z_pos == initial_moons[0]._z_pos and moons[0]._z_vel == initial_moons[0]._z_vel
    m1_z_eq = moons[1]._z_pos == initial_moons[1]._z_pos and moons[1]._z_vel == initial_moons[1]._z_vel
    m2_z_eq = moons[2]._z_pos == initial_moons[2]._z_pos and moons[2]._z_vel == initial_moons[2]._z_vel
    m3_z_eq = moons[3]._z_pos == initial_moons[3]._z_pos and moons[3]._z_vel == initial_moons[3]._z_vel

    if m0_z_eq:
        moon_matches_z[0].append(i+1)
    if m1_z_eq:
        moon_matches_z[1].append(i+1)
    if m2_z_eq:
        moon_matches_z[2].append(i+1)
    if m3_z_eq:
        moon_matches_z[3].append(i+1)

    if m0_z_eq and m1_z_eq and m2_z_eq and m3_z_eq and moon_match_z == 0:
        moon_match_z = i+1
        print(f'Z eq at index {i+1}')
    # print(f'Step {i+1}:')
    # step_data['step'] = i+1

    moons_data = []
    for moon in moons:
        data = {}
        data['x_pos'] = moon._x_pos
        data['y_pos'] = moon._y_pos
        data['z_pos'] = moon._z_pos
        data['x_vel'] = moon._x_vel
        data['y_vel'] = moon._y_vel
        data['z_vel'] = moon._z_vel
        data['energy'] = moon.getEnergy()
        moons_data.append(data)
        # print(moon)
    plot_data.append(moons_data)
    i = i + 1
    # if len(moon_matches_x_pos) == 4 and len(moon_matches_y_pos) == 4 and len(moon_matches_z_pos) == 4 and len(moon_matches_x_vel) == 4 and len(moon_matches_y_vel) == 4 and len(moon_matches_z_vel) == 4:
    #     allMatched = True
    #     break
    if moon_match_x > 0 and moon_match_y > 0 and moon_match_z > 0:
        allMatched = True
        break
    # step_data['moons'] = moons_data
    # plot_data.append(step_data)

moon_matches_x_pos_list = [0]*4
for index, value in moon_matches_x_pos.items():
    moon_matches_x_pos_list[index] = value

moon_matches_y_pos_list = [0]*4
for index, value in moon_matches_y_pos.items():
    moon_matches_y_pos_list[index] = value

moon_matches_z_pos_list = [0]*4
for index, value in moon_matches_z_pos.items():
    moon_matches_z_pos_list[index] = value

moon_matches_x_vel_list = [0]*4
for index, value in moon_matches_x_vel.items():
    moon_matches_x_vel_list[index] = value

moon_matches_y_vel_list = [0]*4
for index, value in moon_matches_y_vel.items():
    moon_matches_y_vel_list[index] = value

moon_matches_z_vel_list = [0]*4
for index, value in moon_matches_z_vel.items():
    moon_matches_z_vel_list[index] = value


print("Moon Matches:")

print('X Position:')
print (moon_matches_x_pos_list)

print('Y Position:')
print (moon_matches_y_pos_list)

print('Z Position:')
print (moon_matches_z_pos_list)

print('X Velocity:')
print (moon_matches_x_vel_list)

print('Y Velocity:')
print (moon_matches_y_vel_list)

print('Z Velocity:')
print (moon_matches_z_vel_list)

all_list = moon_matches_x_pos_list + moon_matches_y_pos_list + moon_matches_z_pos_list + moon_matches_x_vel_list + moon_matches_y_vel_list + moon_matches_z_vel_list

x_pos_list1 = []
y_pos_list1 = []
z_pos_list1 = []

x_pos_list2 = []
y_pos_list2 = []
z_pos_list2 = []

x_pos_list3 = []
y_pos_list3 = []
z_pos_list3 = []

x_pos_list4 = []
y_pos_list4 = []
z_pos_list4 = []

time_list = list(range(0,steps))

x_vel_list1 = []
y_vel_list1 = []
z_vel_list1 = []

x_vel_list2 = []
y_vel_list2 = []
z_vel_list2 = []

x_vel_list3 = []
y_vel_list3 = []
z_vel_list3 = []

x_vel_list4 = []
y_vel_list4 = []
z_vel_list4 = []


energy_list1 = []
energy_list2 = []
energy_list3 = []
energy_list4 = []

energy_list = []

for index, item in enumerate(plot_data):
    x_pos_list1.append(item[0]['x_pos'])
    y_pos_list1.append(item[0]['y_pos'])
    z_pos_list1.append(item[0]['z_pos'])

    x_pos_list2.append(item[1]['x_pos'])
    y_pos_list2.append(item[1]['y_pos'])
    z_pos_list2.append(item[1]['z_pos'])

    x_pos_list3.append(item[2]['x_pos'])
    y_pos_list3.append(item[2]['y_pos'])
    z_pos_list3.append(item[2]['z_pos'])

    x_pos_list4.append(item[3]['x_pos'])
    y_pos_list4.append(item[3]['y_pos'])
    z_pos_list4.append(item[3]['z_pos'])

    x_vel_list1.append(item[0]['x_vel'])
    y_vel_list1.append(item[0]['y_vel'])
    z_vel_list1.append(item[0]['z_vel'])

    x_vel_list2.append(item[1]['x_vel'])
    y_vel_list2.append(item[1]['y_vel'])
    z_vel_list2.append(item[1]['z_vel'])

    x_vel_list3.append(item[2]['x_vel'])
    y_vel_list3.append(item[2]['y_vel'])
    z_vel_list3.append(item[2]['z_vel'])

    x_vel_list4.append(item[3]['x_vel'])
    y_vel_list4.append(item[3]['y_vel'])
    z_vel_list4.append(item[3]['z_vel'])

    energy_list1.append(item[0]['energy'])
    energy_list2.append(item[1]['energy'])
    energy_list3.append(item[2]['energy'])
    energy_list4.append(item[3]['energy'])

    energy = item[0]['energy'] + item[1]['energy'] + item[2]['energy'] + item[3]['energy']

    energy_list.append(energy)

# plt.plot(time_list, x_pos_list1)
# plt.show()
# import numpy as np


# Y = np.fft.fft(energy_list)
# N = int(len(Y)/2+1)
# ziplist = list(zip(time_list, np.abs(Y[:N])))  
# sortedlist = sorted(ziplist, key = lambda x: x[1])[-1]    
# print(sortedlist)

# plt.plot(time_list, Y)
# plt.show()

totalEnergy = 0
for moon in moons:
    totalEnergy += moon.getEnergy()

# print(totalEnergy)

matchlist = []
matchlist.append(moon_match_x)
matchlist.append(moon_match_y)
matchlist.append(moon_match_z)

print(np.lcm.reduce(matchlist))

moon_matches_x_sets = []

for match in moon_matches_x:
    moon_matches_x_sets.append(set(match))

moon_matches_y_sets = []

for match in moon_matches_y:
    moon_matches_y_sets.append(set(match))

moon_matches_z_sets = []

for match in moon_matches_z:
    moon_matches_z_sets.append(set(match))

moon_match_x_set = moon_matches_x_sets[0] & moon_matches_x_sets[1] & moon_matches_x_sets[2] & moon_matches_x_sets[3]
moon_match_y_set = moon_matches_y_sets[0] & moon_matches_y_sets[1] & moon_matches_y_sets[2] & moon_matches_y_sets[3]
moon_match_z_set = moon_matches_z_sets[0] & moon_matches_z_sets[1] & moon_matches_z_sets[2] & moon_matches_z_sets[3]

min_x = min(moon_match_x_set)
min_y = min(moon_match_y_set)
min_z = min(moon_match_z_set)


print(np.lcm.reduce([min_x, min_y, min_z]))