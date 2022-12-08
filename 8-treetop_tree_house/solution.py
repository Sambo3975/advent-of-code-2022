import numpy as np
import numpy.typing as npt
import pyperclip

from option_selection import OptionSelector
from testing import test_bed


def read(path):
    with open(path, 'r') as f:
        data = f.read().rstrip().split('\n')
    grid = np.empty((len(data), len(data[0])), int)
    for i in range(len(data)):
        for j in range(len(data)):
            grid[i, j] = int(data[i][j])
    return grid


def initialize_visibility_matrix(grid: npt.NDArray):
    return np.full(grid.shape, False, bool)


def update_tree_visibility(tree_grid: npt.NDArray[int], tree_visibility: npt.NDArray[bool], row: int, column: int,
                           visible_trees: int, blocked_height: int):
    if (height := tree_grid[row, column]) > blocked_height:
        if not tree_visibility[row, column]:
            visible_trees += 1
            tree_visibility[row, column] = True
        blocked_height = height
    return visible_trees, blocked_height


def count_visible_trees(path):
    tree_grid = read(path)
    tree_visibility = initialize_visibility_matrix(tree_grid)
    visible_trees = 4  # corners will always be visible

    # Left to right
    for row in range(1, tree_grid.shape[0] - 1):
        blocked_height = -1
        for column in range(tree_grid.shape[1]):
            visible_trees, blocked_height = update_tree_visibility(tree_grid, tree_visibility, row, column,
                                                                   visible_trees, blocked_height)
            if blocked_height == 9:
                break
    # Right to left
    for row in range(1, tree_grid.shape[0] - 1):
        blocked_height = -1
        for column in range(tree_grid.shape[1] - 1, -1, -1):
            visible_trees, blocked_height = update_tree_visibility(tree_grid, tree_visibility, row, column,
                                                                   visible_trees, blocked_height)
            if blocked_height == 9:
                break
    # Top to bottom
    for column in range(1, tree_grid.shape[1] - 1):
        blocked_height = -1
        for row in range(tree_grid.shape[0]):
            visible_trees, blocked_height = update_tree_visibility(tree_grid, tree_visibility, row, column,
                                                                   visible_trees, blocked_height)
            if blocked_height == 9:
                break
    # Bottom to top
    for column in range(1, tree_grid.shape[1] - 1):
        blocked_height = -1
        for row in range(tree_grid.shape[0] - 1, -1, -1):
            visible_trees, blocked_height = update_tree_visibility(tree_grid, tree_visibility, row, column,
                                                                   visible_trees, blocked_height)
            if blocked_height == 9:
                break

    return visible_trees


def test_count_visible_trees():
    test_bed(count_visible_trees, ['test.txt'], [21])


def part_1():
    visible_trees = count_visible_trees('input.txt')
    print(f'There are {visible_trees} visible trees.')
    pyperclip.copy(visible_trees)
    print('Copied to clipboard!')


def get_scenic_score(tree_grid: npt.NDArray[int], row: int, column: int):
    """
    Get the scenic score for the tree at the given position in the grid. Assumes that the checked tree is not on the
    edge (there is no reason to consider a tree on the edge as it will always have a scenic score of 0)
    :param tree_grid: Grid of trees parsed from the input file
    :param row: Row of the tree to check
    :param column: Column of the tree to check
    :return: Integer representing the scenic score
    """
    height = tree_grid[row, column]

    # check to the left
    score_left = 0
    for i in range(column - 1, -1, -1):
        score_left += 1
        if tree_grid[row, i] >= height:
            break
    # check to the right
    score_right = 0
    for i in range(column + 1, tree_grid.shape[1]):
        score_right += 1
        if tree_grid[row, i] >= height:
            break
    # check above
    score_up = 0
    for i in range(row - 1, -1, -1):
        score_up += 1
        if tree_grid[i, column] >= height:
            break
    # check below
    score_down = 0
    for i in range(row + 1, tree_grid.shape[0]):
        score_down += 1
        if tree_grid[i, column] >= height:
            break

    return score_left * score_right * score_up * score_down


def test_get_scenic_score():
    tree_grid = read('test.txt')
    inputs = (
        (tree_grid, 1, 2),
        (tree_grid, 3, 2),
    )
    expected_outputs = (4, 8)
    test_bed(get_scenic_score, inputs, expected_outputs)


def get_highest_scenic_score(path):
    tree_grid = read(path)
    highest_score = 0
    for row in range(1, tree_grid.shape[0] - 1):
        for column in range(1, tree_grid.shape[1] - 1):
            highest_score = max(highest_score, get_scenic_score(tree_grid, row, column))
    return highest_score


def test_get_highest_scenic_score():
    test_bed(get_highest_scenic_score, ('test.txt',), (8,))


def part_2():
    highest_score = get_highest_scenic_score('input.txt')
    print(f'Highest possible scenic score: {highest_score}')
    pyperclip.copy(highest_score)
    print('Copied to clipboard!')


def main():
    print('Day 8 - Treetop Tree House')
    selector = OptionSelector()
    selector.add_option('1', 'part 1', part_1)
    selector.add_option('2', 'part 2', part_2)
    selector.add_option('tc', 'test count_visible_trees()', test_count_visible_trees)
    selector.add_option('ts', 'test get_scenic_score', test_get_scenic_score)
    selector.add_option('th', 'test get_highest_scenic_score', test_get_highest_scenic_score)
    selector.run()


if __name__ == '__main__':
    main()
