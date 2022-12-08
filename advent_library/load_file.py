from ast import literal_eval


def as_digit_grid(file_name):
    with open(file_name) as f:
        return [[int(y) for y in x.strip()] for x in f.readlines()]


def as_literals(file_name):
    with open(file_name) as f:
        return [literal_eval(x.strip()) for x in f.readlines()]


def as_strings(file_name):
    with open(file_name) as f:
        return [x.strip() for x in f.readlines()]
