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
    for i in range(1, len(number_str)):
        if number_str[i] == number_str[i-1]:
            return True
    return False

matches = 0

for i in range_to_check:
    if ((not digits_decrease(i)) and adjacent_match(i)):
        matches += 1
