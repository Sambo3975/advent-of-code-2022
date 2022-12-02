import pyperclip

outcomes_1 = {
    'A X': 4,  # Rock:1 + Draw:3
    'A Y': 8,  # Paper:2 + Win:6
    'A Z': 3,  # Scissors:3 + Loss:0
    'B X': 1,  # Rock:1 + Loss:0
    'B Y': 5,  # Paper:2 + Draw:3
    'B Z': 9,  # Scissors:3 + Win:6
    'C X': 7,  # Rock:1 + Win:6
    'C Y': 2,  # Paper:2 + Loss:0
    'C Z': 6,  # Scissors:3 + Draw:3
}
opponent_play_to_index = {
    'A': 0,
    'B': 1,
    'C': 2,
}
my_plays = {
    'X': -1,
    'Y': 0,
    'Z': 1,
}
index_to_choice = ['X', 'Y', 'Z']


def read(path):
    with open(path, 'r') as f:
        return f.read().strip().split('\n')


def strategy_score(path):
    data = read(path)
    score = 0
    for x in data:
        score += outcomes_1[x]

    return score


def fixed_strategy_score(path):
    data = read(path)
    score = 0
    for line in data:
        (opponent, me) = line.split(' ')
        index = opponent_play_to_index[opponent]
        index += my_plays[me]
        index %= 3
        me = index_to_choice[index]
        score += outcomes_1[" ".join((opponent, me))]
    return score


def test_1():
    score = strategy_score('test.txt')
    print(f'Total score: {score}')


def test_2():
    score = fixed_strategy_score('test.txt')
    print(f'Total score: {score}')


def part_1():
    score = strategy_score('input.txt')
    print(f'Total score: {score}')
    pyperclip.copy(score)
    print('Copied to clipboard!')


def part_2():
    score = fixed_strategy_score('input.txt')
    print(f'Total score: {score}')
    pyperclip.copy(score)
    print('Copied to clipboard!')


def main():
    while True:
        print('Day 2 - Rock Paper Scissors')
        print('-------------------------------')
        print(' 1:  part 1')
        print(' 2:  part 2')
        print('t1:  test 1')
        print('t2:  test 2')
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
