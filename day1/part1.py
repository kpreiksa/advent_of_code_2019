import math

def compute_fuel_required(mass):
    fuel_mass = math.floor(mass/3) - 2
    return fuel_mass


fuel_required = 0
f = open('input.txt')
lines = f.readlines()
for line in lines:
    mass = int(line)
    fuel_required += compute_fuel_required(mass)
print(f'Part 1: {fuel_required}')
