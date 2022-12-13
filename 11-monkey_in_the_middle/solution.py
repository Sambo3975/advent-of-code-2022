import re
from collections import deque
from typing import Callable

import pyperclip
import regex

from option_selection import OptionSelector
from testing import test_bed


class Monkey:
    def __init__(self, monkey_group: list['Monkey'], items: list[int], operation: Callable[[int], int], divisor: int,
                 true_catcher: int, false_catcher: int):
        """
        Constructor
        :param items: List of integers representing items, with higher numbers indicating items I am more worried about
        :param operation: The effect this monkey has on my worry level about an inspected item. This is a function that
        takes an integer representing the old worry level of an item and returns an integer representing the new worry
        level of the item
        :param divisor: Divisor used for the test. Let old equal my worry level for an item. Then, if
        old % divisor == 0, pass to the monkey in this group of monkeys
        :param true_catcher:
        :param false_catcher:
        """
        self.monkey_group = monkey_group
        self.items = deque(items)
        self.operation = operation
        self.divisor = divisor
        self.true_catcher = true_catcher
        self.false_catcher = false_catcher

        self.inspections = 0

    def __repr__(self):
        return 'Monkey(\n' \
               f'    monkey_group=[...]\n' \
               f'    items={repr(self.items)}\n' \
               f'    operation={self.operation}\n' \
               f'    divisor={self.divisor}\n' \
               f'    true_catcher={self.true_catcher}\n' \
               f'    false_catcher={self.false_catcher}\n)'

    @classmethod
    def group_from_file(cls, path: str):
        with open(path, 'r') as f:
            monkey_data = f.read().rstrip().split('\n\n')
        monkey_group: list[cls] = []
        for monkey in monkey_data:
            monkey = monkey.split('\n')
            starting_items = [  # Using the regex library for support of repeating capture groups
                int(x) for x in regex.match(r'^  Starting items: (?:(\d+)(?:, )?)+$', monkey[1]).captures(1)]
            operation = eval('lambda old: ' + re.match(r'^  Operation: new = (.+)$', monkey[2]).group(1))
            divisor = int(re.match(r'^  Test: divisible by (\d+)$', monkey[3]).group(1))
            catcher_pattern = r'^    If \w+: throw to monkey (\d+)$'
            true_catcher = int(re.match(catcher_pattern, monkey[4]).group(1))
            false_catcher = int(re.match(catcher_pattern, monkey[5]).group(1))
            monkey_group.append(cls(monkey_group, starting_items, operation, divisor, true_catcher, false_catcher))
        return monkey_group

    def catch_item(self, worry_level: int):
        self.items.append(worry_level)

    def play_keep_away_round(self, freaking_out: bool = False):
        while len(self.items) > 0:
            self.inspections += 1
            worry_level = self.operation(self.items.popleft())
            if not freaking_out:
                worry_level //= 3
            if worry_level % self.divisor == 0:
                catcher = self.true_catcher
            else:
                catcher = self.false_catcher
            self.monkey_group[catcher].catch_item(worry_level)


def test_group_from_file():
    for x in Monkey.group_from_file('test_1.txt'):
        print(x)


def play_keep_away(path: str, rounds: int, freaking_out: bool = False):
    monkeys = Monkey.group_from_file(path)
    for _ in range(rounds):
        for monkey in monkeys:
            monkey.play_keep_away_round(freaking_out)
    monkeys_by_activity_level = sorted(monkeys, key=lambda x: x.inspections, reverse=True)
    return monkeys_by_activity_level[0].inspections * monkeys_by_activity_level[1].inspections


def test_play_keep_away():
    test_bed(play_keep_away, (('test_1.txt', 20),), (10605,))


def test_play_keep_away_but_im_losing_it():
    # This is Python, I ain't afraid of integer overflow
    test_bed(play_keep_away, (('test_1.txt', 10000, True),), (2713310158,))


def part_1():
    monkey_business_level = play_keep_away('input.txt', 20)
    print(f'Level of monkey business: {monkey_business_level} MBUs (monkey business units)')
    pyperclip.copy(monkey_business_level)
    print('Copied to clipboard!')


def part_2():
    monkey_business_level = play_keep_away('input.txt', 10000, True)
    print(f'Level of monkey business: {monkey_business_level} MBUs (monkey business units)')
    pyperclip.copy(monkey_business_level)
    print('Copied to clipboard!')


def main():
    selector = OptionSelector()
    selector.add_option('1', 'part 1', part_1)
    selector.add_option('2', 'part 2', part_2)
    selector.add_option('tg', 'test group from file', test_group_from_file)
    selector.add_option('tp', 'test play keep away', test_play_keep_away)
    selector.add_option('tl', 'test play keep away but I\'m losing it', test_play_keep_away_but_im_losing_it)
    selector.run()


if __name__ == '__main__':
    main()
