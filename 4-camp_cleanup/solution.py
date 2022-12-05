import re

import pyperclip


class Assignment:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __contains__(self, item):
        return item.start >= self.start and item.end <= self.end

    def overlaps(self, item):
        return item.start <= self.end and item.end >= self.start


def read(path):
    with open(path, 'r') as f:
        return f.read().strip().split('\n')


def readline(line):
    line = [int(x) for x in re.split('[-,]', line)]
    return Assignment(line[0], line[1]), Assignment(line[2], line[3])


def count_fully_contained_pairs(path):
    assignments = [readline(line) for line in read(path)]
    fully_contained_pairs = 0
    for (assignment_a, assignment_b) in assignments:
        if assignment_a in assignment_b or assignment_b in assignment_a:
            fully_contained_pairs += 1
    return fully_contained_pairs


def test_1():
    fully_contained_pairs = count_fully_contained_pairs('test.txt')
    print(f'Fully contained pairs: {fully_contained_pairs}')


def part_1():
    fully_contained_pairs = count_fully_contained_pairs('input.txt')
    print(f'Fully contained pairs: {fully_contained_pairs}')
    pyperclip.copy(fully_contained_pairs)
    print('Copied to clipboard!')


def count_overlapping_pairs(path):
    assignments = [readline(line) for line in read(path)]
    overlapping_pairs = 0
    for (assignment_a, assignment_b) in assignments:
        if assignment_a.overlaps(assignment_b) or assignment_b.overlaps(assignment_a):
            overlapping_pairs += 1
    return overlapping_pairs


def test_2():
    fully_contained_pairs = count_overlapping_pairs('test.txt')
    print(f'Overlapping pairs: {fully_contained_pairs}')


def part_2():
    fully_contained_pairs = count_overlapping_pairs('input.txt')
    print(f'Overlapping pairs: {fully_contained_pairs}')
    pyperclip.copy(fully_contained_pairs)
    print('Copied to clipboard!')


def main():
    while True:
        print(
            "Day 4 - Camp Cleanup\n"
            "-----------------------\n"
            " 1:  part 1\n"
            " 2:  part 2\n"
            "t1:  part 1 test\n"
            "t2:  part 2 test\n"
            " q:  quit\n"
        )
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
                print('Invalid selection')
        print()


if __name__ == '__main__':
    main()
