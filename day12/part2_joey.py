import re
import matplotlib.pyplot as plt
import numpy as np

import datetime

start_time = datetime.datetime.now()

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


moon_matches_x = [[],[],[],[]]
moon_matches_y = [[],[],[],[]]
moon_matches_z = [[],[],[],[]]

def joeysshitsucks(moon_matches):
    temp_list_of_sets = []

    for match in moon_matches:
        temp_list_of_sets.append(set(match))

    temp_set = temp_list_of_sets[0] & temp_list_of_sets[1] & temp_list_of_sets[2] & temp_list_of_sets[3]
    return len(temp_set)


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

    m0_x_eq = moons[0]._x_pos == initial_moons[0]._x_pos and moons[0]._x_vel == initial_moons[0]._x_vel
    m1_x_eq = moons[1]._x_pos == initial_moons[1]._x_pos and moons[1]._x_vel == initial_moons[1]._x_vel
    m2_x_eq = moons[2]._x_pos == initial_moons[2]._x_pos and moons[2]._x_vel == initial_moons[2]._x_vel
    m3_x_eq = moons[3]._x_pos == initial_moons[3]._x_pos and moons[3]._x_vel == initial_moons[3]._x_vel

    if m0_x_eq:
        moon_matches_x[0].append(i+1)
        if joeysshitsucks(moon_matches_x) > 0 and joeysshitsucks(moon_matches_y) > 0 and joeysshitsucks(moon_matches_z) > 0:
            allMatched = True
            break
    if m1_x_eq:
        moon_matches_x[1].append(i+1)
        if joeysshitsucks(moon_matches_x) > 0 and joeysshitsucks(moon_matches_y) > 0 and joeysshitsucks(moon_matches_z) > 0:
            allMatched = True
            break
    if m2_x_eq:
        moon_matches_x[2].append(i+1)
        if joeysshitsucks(moon_matches_x) > 0 and joeysshitsucks(moon_matches_y) > 0 and joeysshitsucks(moon_matches_z) > 0:
            allMatched = True
            break
    if m3_x_eq:
        moon_matches_x[3].append(i+1)
        if joeysshitsucks(moon_matches_x) > 0 and joeysshitsucks(moon_matches_y) > 0 and joeysshitsucks(moon_matches_z) > 0:
            allMatched = True
            break

    m0_y_eq = moons[0]._y_pos == initial_moons[0]._y_pos and moons[0]._y_vel == initial_moons[0]._y_vel
    m1_y_eq = moons[1]._y_pos == initial_moons[1]._y_pos and moons[1]._y_vel == initial_moons[1]._y_vel
    m2_y_eq = moons[2]._y_pos == initial_moons[2]._y_pos and moons[2]._y_vel == initial_moons[2]._y_vel
    m3_y_eq = moons[3]._y_pos == initial_moons[3]._y_pos and moons[3]._y_vel == initial_moons[3]._y_vel

    if m0_y_eq:
        moon_matches_y[0].append(i+1)
        if joeysshitsucks(moon_matches_x) > 0 and joeysshitsucks(moon_matches_y) > 0 and joeysshitsucks(moon_matches_z) > 0:
            allMatched = True
            break
    if m1_y_eq:
        moon_matches_y[1].append(i+1)
        if joeysshitsucks(moon_matches_x) > 0 and joeysshitsucks(moon_matches_y) > 0 and joeysshitsucks(moon_matches_z) > 0:
            allMatched = True
            break
    if m2_y_eq:
        moon_matches_y[2].append(i+1)
        if joeysshitsucks(moon_matches_x) > 0 and joeysshitsucks(moon_matches_y) > 0 and joeysshitsucks(moon_matches_z) > 0:
            allMatched = True
            break
    if m3_y_eq:
        moon_matches_y[3].append(i+1)
        if joeysshitsucks(moon_matches_x) > 0 and joeysshitsucks(moon_matches_y) > 0 and joeysshitsucks(moon_matches_z) > 0:
            allMatched = True
            break


    m0_z_eq = moons[0]._z_pos == initial_moons[0]._z_pos and moons[0]._z_vel == initial_moons[0]._z_vel
    m1_z_eq = moons[1]._z_pos == initial_moons[1]._z_pos and moons[1]._z_vel == initial_moons[1]._z_vel
    m2_z_eq = moons[2]._z_pos == initial_moons[2]._z_pos and moons[2]._z_vel == initial_moons[2]._z_vel
    m3_z_eq = moons[3]._z_pos == initial_moons[3]._z_pos and moons[3]._z_vel == initial_moons[3]._z_vel

    if m0_z_eq:
        moon_matches_z[0].append(i+1)
        if joeysshitsucks(moon_matches_x) > 0 and joeysshitsucks(moon_matches_y) > 0 and joeysshitsucks(moon_matches_z) > 0:
            allMatched = True
            break
    if m1_z_eq:
        moon_matches_z[1].append(i+1)
        if joeysshitsucks(moon_matches_x) > 0 and joeysshitsucks(moon_matches_y) > 0 and joeysshitsucks(moon_matches_z) > 0:
            allMatched = True
            break
    if m2_z_eq:
        moon_matches_z[2].append(i+1)
        if joeysshitsucks(moon_matches_x) > 0 and joeysshitsucks(moon_matches_y) > 0 and joeysshitsucks(moon_matches_z) > 0:
            allMatched = True
            break
    if m3_z_eq:
        moon_matches_z[3].append(i+1)
        if joeysshitsucks(moon_matches_x) > 0 and joeysshitsucks(moon_matches_y) > 0 and joeysshitsucks(moon_matches_z) > 0:
            allMatched = True
            break

    i = i + 1
    # if joeysshitsucks(moon_matches_x) > 0 and joeysshitsucks(moon_matches_y) > 0 and joeysshitsucks(moon_matches_z) > 0:
    #     allMatched = True
    #     break


moon_matches_x_sets = [set(match) for match in moon_matches_x]
moon_matches_y_sets = [set(match) for match in moon_matches_y]
moon_matches_z_sets = [set(match) for match in moon_matches_z]

moon_match_x_set = moon_matches_x_sets[0] & moon_matches_x_sets[1] & moon_matches_x_sets[2] & moon_matches_x_sets[3]
moon_match_y_set = moon_matches_y_sets[0] & moon_matches_y_sets[1] & moon_matches_y_sets[2] & moon_matches_y_sets[3]
moon_match_z_set = moon_matches_z_sets[0] & moon_matches_z_sets[1] & moon_matches_z_sets[2] & moon_matches_z_sets[3]

min_x = min(moon_match_x_set)
min_y = min(moon_match_y_set)
min_z = min(moon_match_z_set)

print('Everything is the same at... ')
print(np.lcm.reduce([min_x, min_y, min_z]))

end_time = datetime.datetime.now()
time_diff = end_time - start_time
print(time_diff)