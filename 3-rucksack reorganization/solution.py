from collections import Counter

import pyperclip


def read(path):
    with open(path, 'r') as f:
        return f.read().strip().split('\n')


def ascii_to_priority(ascii_value):
    if ord('a') <= ascii_value <= ord('z'):
        return ascii_value - 96  # a's ASCII value is 97; priority should be 1
    return ascii_value - 38      # A's ASCII value is 65; priority should be 27


def sum_item_priorities(path):
    data = read(path)
    sum_priorities = 0
    for rucksack in data:
        split_point = len(rucksack) // 2
        left_compartment = Counter(rucksack[:split_point])
        right_compartment = Counter(rucksack[split_point:])
        for key in left_compartment.keys():
            if key in right_compartment:
                sum_priorities += ascii_to_priority(ord(key))
                break
    return sum_priorities


def sum_badge_priorities(path):
    rucksacks = read(path)
    sum_priorities = 0
    for i in range(0, len(rucksacks), 3):
        rucksack_1 = Counter(rucksacks[i])
        rucksack_2 = Counter(rucksacks[i + 1])
        rucksack_3 = Counter(rucksacks[i + 2])
        for key in rucksack_1:
            if key in rucksack_2 and key in rucksack_3:
                sum_priorities += ascii_to_priority(ord(key))
                break
    return sum_priorities


def test_1():
    priority = sum_item_priorities('test.txt')
    print(f'Priority: {priority}')


def part_1():
    priority = sum_item_priorities('input.txt')
    print(f'Priority: {priority}')
    pyperclip.copy(priority)
    print('Copied to clipboard!')


def test_2():
    priority = sum_badge_priorities('test.txt')
    print(f'Priority: {priority}')


def part_2():
    priority = sum_badge_priorities('input.txt')
    print(f'Priority: {priority}')
    pyperclip.copy(priority)
    print('Copied to clipboard!')


def main():
    while True:
        print('Day 3 - Rucksack Reorganization')
        print('----------------------------------')
        print(' 1:  part 1')
        print(' 2:  part 2')
        print('t1:  part 1 test')
        print('t2:  part 2 test')
        print(' q:  quit')
        match input('> '):
            case '1':
                part_1()
            case '2':
                part_2()
            case 't1':
                test_1()
            case 't2':
                test_2()
            case 'q':
                print()
                break
            case _:
                print("Invalid selection")
        print()


if __name__ == '__main__':
    main()
