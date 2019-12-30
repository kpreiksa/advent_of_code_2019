import datetime

range_to_check = range(372304, 847061)

def get_digit(digit, number):
    return int(str(number)[digit])

def get_num_digits(number):
    return len(str(number))

def digits_decrease(number):
    number_str = str(number)
    for i in range(1, len(number_str)):
        if number_str[i] < number_str[i-1]:
            return True
    return False

def adjacent_match(number):
    number_str = str(number)
    retval = False
    adjacent_counts_dict = {}
    for i in range(0, len(number_str)):
        adjacent_counts = 0
        for j in range(i, len(number_str)):
            if number_str[j] != number_str[i]:
                break
            adjacent_counts += 1
        if number_str[i] in adjacent_counts_dict:
            adjacent_counts_dict[number_str[i]].append(adjacent_counts)
        else:
            adjacent_counts_dict[number_str[i]] = [adjacent_counts]

    for key, values in adjacent_counts_dict.items():
        if (max(values) == 2):
            retval = True
        else:
            retval = False
        if retval:
            return True
    return retval

start_time = datetime.datetime.now()
matches = 0

for i in range_to_check:
    if ((not digits_decrease(i)) and adjacent_match(i)):
        matches += 1

end_time = datetime.datetime.now()
time_diff = end_time - start_time

print(f'Execution Time: {time_diff}')