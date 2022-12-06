import pyperclip


def read(path):
    with open(path, 'r') as f:
        return f.read().strip().split('\n')


def find_unique_string(datastream, length):
    for i in range(len(datastream) - length):
        character_set = set(datastream[i:i + length])
        if len(character_set) == length:
            return i + length


def find_start_of_packet(datastream):
    return find_unique_string(datastream, 4)


def test_find_start_of_packet():
    streams = read('test.txt')
    for stream in streams:
        print(f'{stream}: first marker after character {find_start_of_packet(stream)}')


def part_1():
    with open('input.txt', 'r') as f:
        marker_end = find_start_of_packet(f.read().strip())
    print(f'First marker after character {marker_end}')
    pyperclip.copy(marker_end)
    print('Copied to clipboard!')


def find_start_of_message(datastream):
    return find_unique_string(datastream, 14)


def test_find_start_of_message():
    streams = read('test.txt')
    for stream in streams:
        print(f'{stream}: first marker after character {find_start_of_message(stream)}')


def part_2():
    with open('input.txt', 'r') as f:
        marker_end = find_start_of_message(f.read().strip())
    print(f'First marker after character {marker_end}')
    pyperclip.copy(marker_end)
    print('Copied to clipboard!')


def main():
    while True:
        print(
            'Day 6 - Tuning Trouble\n'
            '-------------------------\n'
            ' 1:  part 1\n'
            ' 2:  part 2\n'
            'tp:  test find_start_of_packet\n'
            'tm:  test find_start_of_message\n'
            ' q:  quit'
        )
        match input('> '):
            case '1':
                part_1()
            case '2':
                part_2()
            case 'tp':
                test_find_start_of_packet()
            case 'tm':
                test_find_start_of_message()
            case 'q':
                print()
                break
            case _:
                print("Invalid selection")
        print()


if __name__ == '__main__':
    main()
