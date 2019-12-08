orbits = {}
f = open('day6_input.txt')
lines = f.readlines()
total_orbits = 0
for line in lines:
    split_line = line.strip().split(')')
    if len(split_line) == 2:
        object_being_orbited = split_line[0]
        object_orbiting = split_line[1]
        if object_being_orbited in orbits:
            orbits[object_being_orbited].append(object_orbiting)
        else:
            orbits[object_being_orbited] = [object_orbiting]
    else:
        raise ValueError('Expected 2 objects')

def compute_orbits(object_to_check):
    # print(f'Checking orbits for {object_to_check}')
    orbits_for_object = 0
    if(object_to_check in orbits):
        orbits_for_object += len(orbits[object_to_check])
        # print(f'{object_to_check} has {len(orbits[object_to_check])} orbits. Recursing.')
        for next_object in orbits[object_to_check]:
            orbits_for_object += compute_orbits(next_object)
        # print(f'Object: {object_to_check} has {orbits_for_object} direct and indirect orbits')
        return orbits_for_object
    else:
        return 0

for k in orbits.keys():
    total_orbits += compute_orbits(k)

print(total_orbits)

