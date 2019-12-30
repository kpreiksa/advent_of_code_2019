import math
import datetime

def compute_fuel_required(mass):
    fuel_mass = math.floor(mass/3) - 2
    return fuel_mass

start_time = datetime.datetime.now()
fuel_required = 0
f = open('input.txt')
lines = f.readlines()
for line in lines:
    mass = int(line)
    fuel_required += compute_fuel_required(mass)
print(f'Part 1: {fuel_required}')


end_time = datetime.datetime.now()
time_diff = end_time - start_time

print(f'Execution Time: {time_diff}')