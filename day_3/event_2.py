import re
from os.path import join

verbose = False
example_file = False
folder_name = 'day_3'


def parse_input(example=False):
    file_name = 'input_1{}.txt'.format('_example' if example else '')
    file_content = []
    with open(join(folder_name, file_name)) as f:
        for line in f:
            line = line.strip('\n')
            file_content.append([c for c in line])
            if verbose:
                print([c for c in line])
                if len(file_content) == 10:
                    break
    return file_content


file_content = parse_input(example_file)
dimensions = len(file_content), len(file_content[0])


digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
blank = '.'

def find_symbols(file_content):
    unique = set([el for row in file_content for el in row])
    return [e for e in unique if (e not in digits) and (e != blank)]

symbols = find_symbols(file_content=file_content)

number_pattern = re.compile('\d+')
asterix_pattern = re.compile('\*')

def check_positions(pos_0, pos_1, min_0=0, min_1=0, max_0=dimensions[0], max_1=dimensions[1]):
    if (pos_0 < min_0) or (pos_0 == max_0):
        return False
    if (pos_1 < min_1) or (pos_1 == max_1):
        return False
    return True


def available_positions(pos_0, pos_1_b, pos_1_e, min_0=0, min_1=0, max_0=dimensions[0], max_1=dimensions[1]):
    positions = []
    if pos_1_b > min_1:
        positions.append((pos_0, pos_1_b - 1))
        if check_positions(pos_0 - 1, pos_1_b, max_0=max_0, max_1=max_1):
            positions.append((pos_0 - 1, pos_1_b - 1))
        if check_positions(pos_0 + 1, pos_1_b, max_0=max_0, max_1=max_1):
            positions.append((pos_0 + 1, pos_1_b - 1))
    if pos_1_e < max_1:
        positions.append((pos_0, pos_1_e))
        if check_positions(pos_0 - 1, pos_1_e, max_0=max_0, max_1=max_1):
            positions.append((pos_0 - 1, pos_1_e))
        if check_positions(pos_0 + 1, pos_1_e, max_0=max_0, max_1=max_1):
            positions.append((pos_0 + 1, pos_1_e))
    for p in range(pos_1_b, pos_1_e):
        if check_positions(pos_0 - 1, p, max_0=max_0, max_1=max_1):
            positions.append((pos_0 - 1, p))
        if check_positions(pos_0 + 1, p, max_0=max_0, max_1=max_1):
            positions.append((pos_0 + 1, p))
    return positions


def find_all_numbers(file_content) -> tuple[int, tuple[int, int], int]:
    all_matches = []
    for i, line in enumerate(file_content):
        string = ''.join(line)
        matches = number_pattern.finditer(string)
        for m in matches:
            pos_1 = m.span()
            all_matches.append((i, pos_1, int(m.group(0))))
    return all_matches


def find_all_asterix(file_content) -> tuple[int, tuple[int, int], str]:
    all_matches = []
    for i, line in enumerate(file_content):
        string = ''.join(line)
        matches = asterix_pattern.finditer(string)
        for m in matches:
            pos_1 = m.span()
            all_matches.append((i, pos_1, m.group(0)))
    return all_matches


def check_asterix(p0, p1, file_content) -> bool:
    if file_content[p0][p1] == '*':
        return True
    return False


def check_number(p0, p1, all_numbers) -> tuple[int, tuple[int, int], int] | None:
    for y, (b, e), num in all_numbers:
        if (p0 == y) and (p1 >= b) and (p1 < e):
            return y, (b, e), num
    return None


def find_gears(file_content):
    dimensions = len(file_content), len(file_content[0])
    all_numbers = find_all_numbers(file_content)
    all_asterix = find_all_asterix(file_content)
    gears = {}
    for pos_0, (b, e), ast in all_asterix:
        if verbose:
            print(f'{ast} -> ({pos_0}, [{b}:{e}])')
        positions = available_positions(pos_0, b, e, max_0=dimensions[0], max_1=dimensions[1])
        for p in positions:
            numbers = check_number(p[0], p[1], all_numbers)
            if verbose:
                print(f'     -> ({p[0], p[1]}) : ', end='')
                if numbers is not None:
                    print(numbers[2])
                else:
                    print()
            if numbers is not None:
                nums = gears.get((pos_0, (b, e)), [])
                gears[(pos_0, (b, e))] = nums + [numbers]
        elements = gears.get((pos_0, (b, e)), [])
        if elements:
            gears[(pos_0, (b, e))] = list(set(elements))
    gears = {k: v for k, v in gears.items() if len(v) == 2}
    return gears


def get_gear_ratio(gear: list[tuple[int, tuple[int, int], int]]):
    return gear[0][2] * gear[1][2]


gears = find_gears(file_content)
if verbose:
    for k, v in gears.items():
        print(k, v)

gear_ratios = {k: get_gear_ratio(v) for k, v in gears.items()}

print("Event 1:", sum([v for k, v in gear_ratios.items()]))


