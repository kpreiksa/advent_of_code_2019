import re


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


for i in range(0,1000):
    for moonPair in moonPairs:
        moonPair[0].applyGravity(moonPair[1])

    for moon in moons:
        moon.applyVelocity()
        moon.move()
        moon.resetGravity()

    print(f'Step {i+1}:')
    for moon in moons:
        print(moon)


totalEnergy = 0
for moon in moons:
    totalEnergy += moon.getEnergy()

print(totalEnergy)
