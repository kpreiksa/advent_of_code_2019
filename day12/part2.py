import re
import matplotlib.pyplot as plt
import numpy as np

import datetime

start_time = datetime.datetime.now()


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


moon_match_x = 0
moon_match_y = 0
moon_match_z = 0

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

    if m0_x_eq and m1_x_eq and m2_x_eq and m3_x_eq and moon_match_x == 0:
        moon_match_x = i+1

    m0_y_eq = moons[0]._y_pos == initial_moons[0]._y_pos and moons[0]._y_vel == initial_moons[0]._y_vel
    m1_y_eq = moons[1]._y_pos == initial_moons[1]._y_pos and moons[1]._y_vel == initial_moons[1]._y_vel
    m2_y_eq = moons[2]._y_pos == initial_moons[2]._y_pos and moons[2]._y_vel == initial_moons[2]._y_vel
    m3_y_eq = moons[3]._y_pos == initial_moons[3]._y_pos and moons[3]._y_vel == initial_moons[3]._y_vel

    if m0_y_eq and m1_y_eq and m2_y_eq and m3_y_eq and moon_match_y == 0:
        moon_match_y = i+1

    m0_z_eq = moons[0]._z_pos == initial_moons[0]._z_pos and moons[0]._z_vel == initial_moons[0]._z_vel
    m1_z_eq = moons[1]._z_pos == initial_moons[1]._z_pos and moons[1]._z_vel == initial_moons[1]._z_vel
    m2_z_eq = moons[2]._z_pos == initial_moons[2]._z_pos and moons[2]._z_vel == initial_moons[2]._z_vel
    m3_z_eq = moons[3]._z_pos == initial_moons[3]._z_pos and moons[3]._z_vel == initial_moons[3]._z_vel

    if m0_z_eq and m1_z_eq and m2_z_eq and m3_z_eq and moon_match_z == 0:
        moon_match_z = i+1

    i = i + 1
    if moon_match_x > 0 and moon_match_y > 0 and moon_match_z > 0:
        allMatched = True
        break

matchlist = []
matchlist.append(moon_match_x)
matchlist.append(moon_match_y)
matchlist.append(moon_match_z)

answer = np.lcm.reduce(matchlist)

end_time = datetime.datetime.now()
time_diff = end_time - start_time
print(f'Everything is the same at [{answer}]. Solution took [{time_diff}]. Iterations = [{i}]')