import math
import datetime

def compute_fuel_required(mass):
    fuel_mass = math.floor(mass/3) - 2
    if(fuel_mass < 0):
        return 0
    else:
        fuel_mass += compute_fuel_required(fuel_mass)
    return fuel_mass

start_time = datetime.datetime.now()
fuel_required = 0
f = open('input.txt')
lines = f.readlines()
for line in lines:
    mass = int(line)
    fuel_required += compute_fuel_required(mass)
print(f'Part 2: {fuel_required}')

end_time = datetime.datetime.now()
time_diff = end_time - start_time

print(f'Execution Time: {time_diff}')