import pyperclip

from testing import test_bed
from option_selection import OptionSelector

direction_to_vector = {
    'R': (1, 0),
    'U': (0, 1),
    'L': (-1, 0),
    'D': (0, -1),
}


def sign(number: int):
    return -1 if number < 0 else (0 if number == 0 else 1)


def parse_instruction(line: str):
    line = line.split(' ')
    return direction_to_vector[line[0]], int(line[1])


def read(path: str):
    with open(path, 'r') as f:
        return (parse_instruction(line) for line in f.read().rstrip().split('\n'))


def update_rope_head(motion_vector: tuple[int], head_position: list[int]):
    # move the head as instructed
    head_position[0] += motion_vector[0]
    head_position[1] += motion_vector[1]


def update_rope_tail(head_position: list[int], tail_position: list[int],
                     visited_positions: set[tuple[int, int]] = None):
    # if tail is 2 or more spaces away from the head (counting diagonal moves as 1 space), move it toward the head
    # using the logic of a D.R.O.D. Roach
    if tail_position[0] < head_position[0] - 1 or tail_position[0] > head_position[0] + 1 \
            or tail_position[1] < head_position[1] - 1 or tail_position[1] > head_position[1] + 1:
        tail_position[0] += sign(head_position[0] - tail_position[0])
        tail_position[1] += sign(head_position[1] - tail_position[1])
        if visited_positions is not None:
            visited_positions.add((tail_position[0], tail_position[1]))


def simulate_short_rope(path: str):
    return simulate_rope(path, 2)


def test_simulate_short_rope():
    test_bed(simulate_short_rope, ['test.txt'], [13])


def simulate_rope(path: str, rope_length: int = 10):
    instructions = read(path)
    knot_positions = [[0, 0] for _ in range(rope_length)]
    visited_positions = {(0, 0)}
    for instruction in instructions:
        for _ in range(instruction[1]):
            update_rope_head(instruction[0], knot_positions[0])
            for i in range(1, len(knot_positions)):
                update_rope_tail(knot_positions[i - 1], knot_positions[i],
                                 None if i < len(knot_positions) - 1 else visited_positions)
    return len(visited_positions)


def test_simulate_rope():
    test_bed(simulate_rope, ['test2.txt'], [36])


def part_1():
    visited_positions = simulate_short_rope('input.txt')
    print(f'The tail of the rope visited {visited_positions} unique positions.')
    pyperclip.copy(visited_positions)
    print('Copied to clipboard!')


def part_2():
    visited_positions = simulate_rope('input.txt')
    print(f'The tail of the rope visited {visited_positions} unique positions.')
    pyperclip.copy(visited_positions)
    print('Copied to clipboard!')


def main():
    print('Day 9 - Rope Bridge')
    selector = OptionSelector()
    selector.add_option('1', 'part 1', part_1)
    selector.add_option('2', 'part 2', part_2)
    selector.add_option('ts', 'test simulate_short_rope()', test_simulate_short_rope)
    selector.add_option('tr', 'test simulate_rope', test_simulate_rope)
    selector.run()


if __name__ == '__main__':
    main()
