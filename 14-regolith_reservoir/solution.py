import pyperclip

from magic_matrix import MagicMatrix
from option_selection import OptionSelector
from testing import test_bed
from collections import deque
from typing import Deque


def read(path: str):
    with open(path, 'r') as f:
        lines = [[[int(z) for z in y.split(',')] for y in x.split(' -> ')] for x in f.read().rstrip().split('\n')]
    grid = MagicMatrix()
    for i in range(len(lines)):
        for j in range(1, len(lines[i])):
            for y in range(min(lines[i][j - 1][1], lines[i][j][1]), max(lines[i][j - 1][1], lines[i][j][1]) + 1):
                for x in range(min(lines[i][j - 1][0], lines[i][j][0]), max(lines[i][j - 1][0], lines[i][j][0]) + 1):
                    grid[y, x] = '#'
    return grid


def test_read():
    print(read('in_1.txt'))


def drop_sand(grid: MagicMatrix) -> bool:
    """
    Simulate dropping a unit of sand from the position (500,0).

    Positive y is down. A unit of sand first attempts to fall down one space. If the space below is blocked,
    it attempts to fall down and to the left one space. If that space is blocked, it attempts to fall down and to the
    right one space. If that space is blocked, the unit of sand stops moving. This repeats until the unit of sand
    either stops moving or falls into the abyss :param grid: Represents a slice of the cave, including all stone and
    all sand that has previously fallen :return: True if the sand came to rest, False if it fell into the abyss
    """
    x = 500
    y = 0
    while True:
        if y == grid.extents()[3]:
            return False  # fall into the abyss
        elif grid[y + 1, x] is None:
            pass    # fall straight down
        elif grid[y + 1, x - 1] is None:
            x -= 1  # fall down and left
        elif grid[y + 1, x + 1] is None:
            x += 1  # fall down and right
        else:
            grid[y, x] = 'o'
            return True
        y += 1


def fill_with_sand(path: str, show_picture: bool = False) -> int:
    """
    Repeatedly drop sand, one unit at a time, until a unit of sand falls into the abyss
    :param path: Path to a file containing data about the slice of the cave where sand is to be dropped
    :param show_picture: If true, a picture of the cave will be shown at the end
    :return: An integer representing the number of units of sand dropped before sand started falling into the abyss
    """
    cave = read(path)
    rocks = len(cave)  # No sand has been dropped, so len is equal to the number of rock spaces
    while drop_sand(cave):
        pass
    if show_picture:
        print(cave)
    return len(cave) - rocks  # len is now equal to the number of rock spaces plus sand spaces


def fast_drop_sand(grid: MagicMatrix, max_y: int, sand_path: Deque[tuple[int, int]], infinite_floor: bool = False):
    """
    Simulate dropping a unit of sand from the position (500,0).

    Positive y is down.

    A unit of sand first attempts to fall down one space. If the space below is blocked, it attempts to fall down and to
    the left one space. If that space is blocked, it attempts to fall down and to the right one space. If that space is
    blocked, the unit of sand stops moving. This repeats until the unit of sand either stops moving or falls into the
    abyss. This version reduces time complexity by caching the path taken by units of sand to avoid repeating work
    :param grid: Represents a slice of the cave, including all stone and all sand that has previously fallen
    :param max_y: maximum y position for a grain of sand.
    :param sand_path: Used as a stack containing the path previous units of sand took to get to this space
    :param infinite_floor: If True, the simulation will treat max_y as the lowest empty space above an infinite floor.
    If False, max_y will be treated as the lowest point above an abyss
    :return: True if the sand came to rest, False if it fell into the abyss or the sand drop point was blocked
    """
    # Optimization to avoid repeating work
    start_point = sand_path[-1]
    if grid[start_point] is not None:  # End of path is blocked; attempt to start from the previous space in the path
        sand_path.pop()
        if len(sand_path) == 0:  # Start of path is blocked; no more sand can be spawned
            return False
        start_point = sand_path[-1]
    (y, x) = start_point

    while True:
        if y == max_y:
            if infinite_floor:
                grid[y, x] = 'o'
                return True
            return False
        elif grid[y + 1, x] is None:
            pass
        elif grid[y + 1, x - 1] is None:
            x -= 1  # fall down and left
        elif grid[y + 1, x + 1] is None:
            x += 1  # fall down and right
        else:
            grid[y, x] = 'o'
            return True
        y += 1
        sand_path.append((y, x))


def fast_fill_with_sand(path: str, infinite_floor: bool = False, show_picture: bool = False):
    """
    Repeatedly drop sand, one unit at a time, until a unit of sand falls into the abyss or the entry point is blocked.

    This version supports simulation of an infinite floor. It also caches the path taken by last unit of
    sand, avoiding unnecessary work and vastly improving performance
    :param path: Path to a file containing data about the slice of the cave where sand is to be dropped
    :param infinite_floor: If true, the simulation will be run with an infinite floor
    :param show_picture: If true, a picture of the cave will be shown at the end
    :return:
    """
    cave = read(path)
    rocks = len(cave)  # No sand has been dropped, so len is equal to the number of rock spaces
    sand_path = deque([(0, 500)])
    max_y = cave.extents()[2]
    if infinite_floor:
        max_y += 1
    while fast_drop_sand(cave, max_y, sand_path, infinite_floor):
        pass
    if show_picture:
        print(cave)
    return len(cave) - rocks  # len is now equal to the number of rock spaces plus sand spaces


def test_fill_with_sand():
    test_bed(fill_with_sand, (('in_1.txt', True),), (24,))


def test_fast_fill_with_sand():
    path = 'in_1.txt'
    test_bed(fast_fill_with_sand, ((path, False, True), (path, True, True)), (24, 93))


def part_1():
    result = fill_with_sand('input.txt')
    print(f'{result} units of sand came to rest.')
    pyperclip.copy(result)
    print('Copied to clipboard!')


def part_1_fast():
    result = fast_fill_with_sand('input.txt')
    print(f'{result} units of sand came to rest.')
    pyperclip.copy(result)
    print('Copied to clipboard!')


def part_2():
    result = fast_fill_with_sand('input.txt', True)
    print(f'{result} units of sand came to rest.')
    pyperclip.copy(result)
    print('Copied to clipboard!')


def main():
    print('Day 14 - Regolith Reservoir')
    selector = OptionSelector()
    selector.add_option('1', 'part 1 (slow)', part_1)
    selector.add_option('1f', 'part 1 (fast)', part_1_fast)
    selector.add_option('2', 'part 2', part_2)
    selector.add_option('tr', 'test read (visual)', test_read)
    selector.add_option('tf', 'test fill with sand (visual + automated)', test_fill_with_sand)
    selector.add_option('tf2', 'test fast fill with sand (visual + automated)', test_fast_fill_with_sand)
    selector.run()


if __name__ == '__main__':
    main()
