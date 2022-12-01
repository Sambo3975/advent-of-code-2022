import pyperclip


def read(path):
    with open(path, 'r') as f:
        data = f.read()
    return data.strip().split('\n\n')


def count_calories(path):

    max_calories = 0
    data = read(path)
    for entry in data:
        max_calories = max(max_calories, sum([int(x) for x in entry.split('\n')]))
    return max_calories


def top_3_calories(path):
    data = read(path)
    totals = []
    for entry in data:
        totals.append(sum([int(x) for x in entry.split('\n')]))
    return sum(sorted(totals, reverse=True)[:3])


def main():
    while True:
        print("Day 1 - Calorie Counting")
        print("------------------------------------")
        print(" 1:  part 1 solution")
        print(" 2:  part 2 solution")
        print("t1:  part 1 test")
        print('t2:  part 2 test')
        print(" q:  quit")
        match input("> "):
            case '1':
                res = count_calories("input.txt")
                print(f'Max calories: {res}')
                pyperclip.copy(res)
                print('Result copied to clipboard!')
            case '2':
                res = top_3_calories("input.txt")
                print(f'Max calories: {res}')
                pyperclip.copy(res)
                print('Result copied to clipboard!')
            case 't1':
                res = count_calories("test.txt")
                print(f'Max calories: {res}')
            case 't2':
                res = top_3_calories('test.txt')
                print(f'Sum of calories in top 3: {res}')
            case 'q':
                break
            case _:
                print("Invalid selection")
        print()


if __name__ == '__main__':
    main()
