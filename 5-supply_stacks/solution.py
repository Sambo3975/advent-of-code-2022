import re
from collections import deque

import pyperclip


def read(path):
    with open(path, 'r') as f:
        data = f.read().rstrip()
    (crates, rearrangement_procedure) = data.split('\n\n')
    crates = crates.split('\n')
    crate_stacks = []
    for i in range(1, len(crates[-1]), 4):
        stack = deque()
        for j in range(len(crates) - 2, -1, -1):
            if i >= len(crates[j]) or (crate_letter := crates[j][i]) == ' ':
                break
            stack.append(crate_letter)
        crate_stacks.append(stack)
    return crate_stacks, rearrangement_procedure.split('\n')


def test_read():
    crate_stacks, _ = read('test.txt')
    print(crate_stacks)


def move_crates_with_crate_mover_9000(path):
    crate_stacks, movement_procedure = read(path)
    for instruction in movement_procedure:
        (number_of_crates, start_stack, destination_stack) = (
            int(x) for x in re.match(r'move (\d+) from (\d+) to (\d+)', instruction).groups())
        for i in range(number_of_crates):
            crate_stacks[destination_stack - 1].append(crate_stacks[start_stack - 1].pop())
    return ''.join((stack[-1] for stack in crate_stacks))


def test_move_crates_with_crate_mover_9000():
    message = move_crates_with_crate_mover_9000('test.txt')
    print(f'Top crates: {message}')


def part_1():
    message = move_crates_with_crate_mover_9000('input.txt')
    print(f'Top crates: {message}')
    pyperclip.copy(message)
    print('Copied to clipboard!')


def move_crates_with_crate_mover_9001(path):
    crate_stacks, movement_procedure = read(path)
    for instruction in movement_procedure:
        (number_of_crates, start_stack, destination_stack) = (
            int(x) for x in re.match(r'move (\d+) from (\d+) to (\d+)', instruction).groups())
        temp_stack = deque()
        for i in range(number_of_crates):
            temp_stack.append(crate_stacks[start_stack - 1].pop())
        for i in range(number_of_crates):
            crate_stacks[destination_stack - 1].append(temp_stack.pop())
    return ''.join((stack[-1] for stack in crate_stacks))


def test_move_crates_with_crate_mover_9001():
    message = move_crates_with_crate_mover_9001('test.txt')
    print(f'Top crates: {message}')


def part_2():
    message = move_crates_with_crate_mover_9001('input.txt')
    print(f'Top crates: {message}')
    pyperclip.copy(message)
    print('Copied to clipboard!')


def main():
    while True:
        print(
            'Day 5 - Supply Stacks\n'
            '------------------------\n'
            '  1:  part 1\n'
            '  2:  part 2\n'
            ' tr:  read() test\n'
            'tm0:  move_crates_with_crate_mover_9000() test\n'
            'tm1:  move_crates_with_crate_mover_9001() test\n'
            '  q:  quit\n'
        )
        match input('> '):
            case '1':
                part_1()
            case '2':
                part_2()
            case 'tr':
                test_read()
            case 'tm0':
                test_move_crates_with_crate_mover_9000()
            case 'tm1':
                test_move_crates_with_crate_mover_9001()
            case 'q':
                print()
                break
            case _:
                print('Invalid selection')
        print()


if __name__ == '__main__':
    main()
