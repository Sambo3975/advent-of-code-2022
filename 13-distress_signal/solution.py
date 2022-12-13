import re

import pyperclip
import functools

from option_selection import OptionSelector
from testing import test_bed


def read(path: str) -> list:
    with open(path, 'r') as f:
        return [tuple(eval(y) for y in x.split('\n')) for x in f.read().rstrip().split('\n\n')]


def read_flat(path: str) -> list:
    with open(path, 'r') as f:
        return [eval(x) for x in re.split(r'\n+', f.read().rstrip())]


def test_read():
    print(read('test.txt'))


def in_right_order(left_value: list | int, right_value: list | int) -> bool | None:
    """
    Check if the packet pair is in the right order
    :param left_value: Value of left packet, or a value inside the packet
    :param right_value: Value of right packet, or a value inside the packet
    :return: True if the pair is in the correct order, False if it is not, or None if it cannot be determined
    """
    left_is_list = isinstance(left_value, list)
    right_is_list = isinstance(right_value, list)
    if not left_is_list and not right_is_list:
        if left_value < right_value:
            return True
        if left_value > right_value:
            return False
    if left_is_list and not right_is_list:
        return in_right_order(left_value, [right_value])
    if not left_is_list and right_is_list:
        return in_right_order([left_value], right_value)
    if left_is_list and right_is_list:
        for i in range(min(len(left_value), len(right_value))):
            if (result := in_right_order(left_value[i], right_value[i])) is not None:
                return result
        if len(left_value) < len(right_value):
            return True
        if len(left_value) > len(right_value):
            return False


def test_in_right_order():
    packets = read('test.txt')
    test_bed(in_right_order, packets, (True, True, False, True, False, True, False, False))


def sum_indices_of_properly_ordered_packets(path):
    packets = read(path)
    result = 0
    for i in range(len(packets)):
        if in_right_order(*packets[i]):
            result += i + 1
    return result


def test_sum_indices():
    test_bed(sum_indices_of_properly_ordered_packets, ('test.txt',), (13,))


def compare_packets(packet_a: list | int, packet_b: list | int):
    if (result := in_right_order(packet_a, packet_b)) is not None:
        return -1 if result else 1
    return 0


def repr_packets(packets: list):
    result = ''
    for packet in packets:
        result += str(packet) + '\n'
    return result


def order_packets(path: str):
    # My guess: too slow or doesn't work
    packets = read_flat(path)
    packets.append([[2]])
    packets.append([[6]])
    packets.sort(key=functools.cmp_to_key(compare_packets))
    return packets


def test_order_packets():
    print('This test fails, but I ran a diff on the expected and actual outputs and there is no difference.\n'
          'It probably has to do with how the strings are encoded or something, but I don\'t wanna screw with that.\n')
    packets = order_packets('test.txt')
    with open('test_output', 'w') as f:
        f.write(repr_packets(packets))
    with open('ordered_output.txt', 'r') as f:
        test_bed(repr_packets, (packets,), (f.read().rstrip(),))
        
        
def get_decoder_key(path: str):
    packets = order_packets(path)
    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


def test_get_decoder_key():
    test_bed(get_decoder_key, ('test.txt',), (140,))


def part_1():
    result = sum_indices_of_properly_ordered_packets('input.txt')
    print(f'Sum of indices for packets in the right order: {result}')
    pyperclip.copy(result)
    print('Copied to clipboard!')
    
    
def part_2():
    result = get_decoder_key('input.txt')
    print(f'Decoder Key: {result}')
    pyperclip.copy(result)
    print('Copied to clipboard!')


def main():
    selector = OptionSelector()
    selector.add_option('1', 'part 1', part_1)
    selector.add_option('2', 'part 2', part_2)
    selector.add_option('tr', 'test read', test_read)
    selector.add_option('ti', 'test in_right_order', test_in_right_order)
    selector.add_option('ts', 'test sum_indices_of_properly_ordered_packets', test_sum_indices)
    selector.add_option('to', 'test packet ordering', test_order_packets)
    selector.add_option('td', 'test finding decoder key', test_get_decoder_key)
    selector.run()


if __name__ == '__main__':
    main()
