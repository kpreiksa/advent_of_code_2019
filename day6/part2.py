orbits = {}
f = open('example_data_santa.txt')
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

def find_all_orbiting_object(object_to_check):
    orbiting_objects = []
    if(object_to_check in orbits):
        objects_in_orbit = orbits[object_to_check]
        for next_object in objects_in_orbit:
            if (isinstance(next_object, list)):
                orbiting_objects.extend(next_object)
            else:
                orbiting_objects.append(next_object)
            next_level = find_all_orbiting_object(next_object)
            if (isinstance(next_level, list)):
                orbiting_objects.extend(next_level)
            else:
                orbiting_objects.append(next_level)

    return orbiting_objects

def find_all_orbiting_objects_nested(object_to_check):
    orbiting_objects = []
    if(object_to_check in orbits):
        objects_in_orbit = orbits[object_to_check]
        for next_object in objects_in_orbit:
            if (isinstance(next_object, list)):
                orbiting_objects.append(next_object)
            else:
                orbiting_objects.append(next_object)
            next_level = find_all_orbiting_objects_nested(next_object)
            if (isinstance(next_level, list)):
                orbiting_objects.append(next_level)
            else:
                orbiting_objects.append(next_level)

    return orbiting_objects

def find_first_level_orbiting_objects(object_to_check):
    orbiting_objects = []
    if(object_to_check in orbits):
        objects_in_orbit = orbits[object_to_check]
        for next_object in objects_in_orbit:
            if (isinstance(next_object, list)):
                orbiting_objects.extend(next_object)
            else:
                orbiting_objects.append(next_object)

    return orbiting_objects

def isValueOrbiting(object_to_check, name):
    if name in find_all_orbiting_object(object_to_check):
        return True
    else:
        return False

def find_parent(obj_name):
    for k,v in orbits.items():
        if obj_name in v:
            return k


parent = find_parent('YOU')
retVal = isValueOrbiting(parent, 'SAN')
orbit_steps = 0
while retVal == False:
    parent = find_parent(parent)
    orbit_steps += 1
    retVal = isValueOrbiting(parent, 'SAN')
    print(retVal)
common_parent = parent
all_objs = find_all_orbiting_objects_nested(common_parent)


orbit_all = {}
for k in orbits.keys():
    orbit_all[k] = find_all_orbiting_object(k)
    total_orbits += compute_orbits(k)

print(total_orbits)