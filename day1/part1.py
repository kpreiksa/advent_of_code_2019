import math

def compute_fuel_required_part1(mass):
    fuel_mass = math.floor(mass/3) - 2
    return fuel_mass

def compute_fuel_required_part2(mass):
    fuel_mass = math.floor(mass/3) - 2
    if(fuel_mass < 0):
        return 0
    else:
        fuel_mass += compute_fuel_required_part2(fuel_mass)
    return fuel_mass

fuel_required_part_1 = 0
fuel_required_part_2 = 0
f = open('input.txt')
lines = f.readlines()
for line in lines:
    mass = int(line)
    fuel_required_part_1 += compute_fuel_required_part1(mass)
    fuel_required_part_2 += compute_fuel_required_part2(mass)
print(f'Part 1: {fuel_required_part_1}')
print(f'Part 2: {fuel_required_part_2}')
