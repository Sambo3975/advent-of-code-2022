import re
from typing import Deque, List

import pyperclip

from testing import test_bed

from collections import deque


class FileNode:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __str__(self, depth=0):
        return f'{"  " * depth}- {self.name} (file, size={self.size})'

    def __repr__(self):
        return f'FileNode("{self.name}", {self.size})'

    def get_size(self):
        return self.size


class DirectoryNode(FileNode):
    def __init__(self, name):
        super().__init__(name, -1)
        self.children: List['FileNode'] = []

    def __str__(self, depth=0):
        result = f'{"  " * depth}- {self.name} (dir)'
        for child in self.children:
            result += '\n' + child.__str__(depth + 1)
        return result

    def __repr__(self):
        return f"DirectoryNode('{self.name}')"

    @staticmethod
    def __get_subdirectory(name: str, directory_queue: Deque['DirectoryNode']):
        while len(directory_queue) > 0:
            current_node = directory_queue.popleft()
            if current_node.name == name:  # found
                return current_node
            for child in current_node.children:
                if isinstance(child, DirectoryNode):
                    directory_queue.append(child)

    def get_subdirectory(self, name, recursive=False):
        """
        Attempt to find a subdirectory. Includes this directory in the search Will return None if the directory is not
        found
        :param name: Name of subdirectory
        :param recursive: If True, the search will be run recursively, breadth-first, on all subdirectories
        the user
        :return: DirectoryNode for the searched directory
        """
        if recursive:
            return self.__get_subdirectory(name, deque([self]))
        else:
            if self.name == name:
                return self
            for child in self.children:
                if child.name == name:
                    return child

    def get_all_subdirectories(self, directory_list: List['DirectoryNode'] = None):
        """
        Get all subdirectories. Includes this directory
        :return: list of subdirectories
        """
        if directory_list is None:
            directory_list = []
        directory_list.append(self)
        for child in self.children:
            if isinstance(child, DirectoryNode):
                child.get_all_subdirectories(directory_list)
        return directory_list

    def get_size(self):
        if self.size >= 0:
            return self.size
        self.size = 0
        for child in self.children:
            self.size += child.get_size()
        return self.size


def change_directory(new_path: str, file_path: Deque['FileNode|DirectoryNode']):
    """
    Change directories
    :param new_path: relative path to new directory
    :param file_path: current file path
    :return: None
    """
    if new_path.startswith('/'):  # the root has already been created
        return
    if new_path.startswith('..'):  # up one level
        file_path.pop()
    else:  # down one level
        file_path.append(file_path[-1].get_subdirectory(new_path))


def construct_file_tree_from_terminal_output(path):
    """
    Construct the file tree structure from the terminal output stored in a log at path
    :param path: location of the log file
    :return: DirectoryNode the root of the file tree
    """
    root = DirectoryNode('/')
    file_path: Deque['DirectoryNode'] = deque([root])
    with open(path, 'r') as f:
        terminal_output = f.read().rstrip().splitlines()

    listing_directory = False

    for line in terminal_output:
        if len(line) == 0:  # I don't know if there will be an empty line at the end or not
            break

        if listing_directory:
            if not line.startswith('$'):  # this is a line of output
                if line.startswith('dir '):  # directory
                    file_path[-1].children.append(DirectoryNode(line[4:]))
                if (match := re.match(r'^(\d+) ([\w.]+)', line)) is not None:  # file
                    file_path[-1].children.append(FileNode(match.group(2), int(match.group(1))))
            else:  # next line of input has been reached
                listing_directory = False

        if line.startswith('$ cd '):  # changed directories
            change_directory(line[5:], file_path)
        elif line.startswith('$ ls'):
            listing_directory = True

    return root


def test_construct_file_tree(_=None):
    return str(construct_file_tree_from_terminal_output('test.txt'))


def get_directory_size(directory: DirectoryNode):
    return directory.get_size()


def test_get_directory_size():
    root = construct_file_tree_from_terminal_output('test.txt')
    with open('test_size.txt') as f:
        directories = [root.get_subdirectory(name, True) for name in f.read().rstrip().split('\n')]
    with open('test_out_size.txt') as f:
        sizes = [int(x) for x in f.read().rstrip().split('\n')]
    test_bed(get_directory_size, directories, sizes)


def get_all_subdirectories(root: DirectoryNode):
    return repr(root.get_all_subdirectories())


def test_get_all_subdirectories():
    root = construct_file_tree_from_terminal_output('test.txt')
    expected_result = "[DirectoryNode('/'), DirectoryNode('a'), DirectoryNode('e'), DirectoryNode('d')]"
    test_bed(get_all_subdirectories, [root], [expected_result])


def get_total_size_of_small_directories(path):
    """
    Get the total size of "small" (100,000 units or fewer) directories
    :param path: location of the terminal log
    :return: Integer representing the total size in units
    """
    root = construct_file_tree_from_terminal_output(path)
    subdirectories = root.get_all_subdirectories()
    total_size = 0
    for directory in subdirectories:
        if (size := directory.get_size()) <= 100_000:
            total_size += size
    return total_size


def test_get_total_size_of_small_directories():
    test_bed(get_total_size_of_small_directories, ['test.txt'], [95437])


def part_1():
    total_size = get_total_size_of_small_directories('input.txt')
    print(f'Total size of small directories: {total_size}')
    pyperclip.copy(total_size)
    print('Copied to clipboard!')


def find_smallest_subdirectory_to_delete(path):
    root = construct_file_tree_from_terminal_output(path)
    needed_space = 30_000_000 - (70_000_000 - root.get_size())  # this will set the size field on all subdirectories
    if needed_space <= 0:
        print('No directory needs to be deleted.')
        return
    directories_with_sizes = sorted([(x.name, x.size) for x in root.get_all_subdirectories()], key=lambda x: x[1])
    for (name, size) in directories_with_sizes:
        if size >= needed_space:
            return name, size


def test_find_smallest_subdirectory_to_delete():
    test_bed(find_smallest_subdirectory_to_delete, ['test.txt'], [('d', 24_933_642)])


def part_2():
    name, size = find_smallest_subdirectory_to_delete('input.txt')
    print(f'Smallest subdirectory to delete: {name}; size = {size}')
    pyperclip.copy(size)
    print('Copied size to clipboard!')


def main():
    while True:
        print(
            'Day 7 - No Space Left on Device\n'
            '----------------------------------\n'
            ' 1:  Part 1\n'
            ' 2:  Part 2\n'
            'tc:  test construct_file_tree()\n'
            'ts:  test get_directory_size()\n'
            'tg:  test get_all_subdirectories()\n'
            'tt:  test get_total_size_of_small_directories()\n'
            'tf:  test find_smallest_subdirectory_to_delete()\n'
            ' q:  quit'
        )
        match input('> '):
            case '1':
                part_1()
            case '2':
                part_2()
            case 'tc':
                with open('test_out.txt') as f:
                    test_bed(test_construct_file_tree, [None], [f.read()])
            case 'ts':
                test_get_directory_size()
            case 'tg':
                test_get_all_subdirectories()
            case 'tt':
                test_get_total_size_of_small_directories()
            case 'tf':
                test_find_smallest_subdirectory_to_delete()
            case 'q':
                print()
                break
        print()


if __name__ == '__main__':
    main()
