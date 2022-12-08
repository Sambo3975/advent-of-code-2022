Coordinate2D = tuple[int, int]


class MagicMatrix:
    """A 'magic matrix' that extends infinitely in all directions. Based on my AoC 2015 version, but with reduced
    complexity and faster key lookups """

    def __init__(self, default_value=None, contents: dict = None):
        self.default_value = default_value
        self.__max_content_length = 0
        self.__contents = {}
        if contents is not None:
            for k, v in contents.items():
                self[k] = v

    def __getitem__(self, key: Coordinate2D):
        if key in self.__contents:
            return self.__contents[key]
        return self.default_value

    def __setitem__(self, key: Coordinate2D, value):
        self.__contents[key] = value
        self.__max_content_length = max(self.__max_content_length, len(str(value)))

    def range(self):
        """
        Get ranges that start and end at the extents of the MagicMatrix
        :return: tuple[range, range]
        """
        row_range = range(min(self.__contents), max(self.__contents) + 1)
        return row_range, range(min(self.__contents, key=lambda t: t[1]), max(self.__contents, key=lambda t: t[1]) + 1)

    def extents(self):
        top = min(self.__contents)[0]
        left = min(self.__contents, key=lambda t: t[1])[1]
        bottom = max(self.__contents)[0]
        right = max(self.__contents, key=lambda t: t[1])[1]
        return top, left, bottom, right

    def __iter__(self):
        """
        Iterate over every key within the extents of the MagicMatrix
        :return: iterator[Coordinate2D]
        """
        row_range, col_range = self.range()
        return (((row, col) for col in col_range) for row in row_range)

    def keys(self):
        """
        Iterate over every non-default key in the MagicMatrix. The order of the keys is undefined
        :return: iterator[Coordinate2D]
        """
        return self.__contents.keys()

    def values(self):
        """
        Iterate over every non-default value in the MagicMatrix. The order is undefined
        :return: iterator[any]
        """
        return self.__contents.values()

    def __repr__(self):
        return f'MagicMatrix({self.default_value}, {self.__contents})'

    def __str__(self):
        top, left, bottom, right = self.extents()
        i_range = range(top, bottom + 1)
        j_range = range(left, right + 1)
        col_width = max(len(str(right)), len(str(left)), self.__max_content_length) + 1
        row_width = max(len(str(bottom)), len(str(top)))

        res = ' ' * (row_width + 1) + ''.join((str(j).ljust(col_width) for j in j_range)) + '\n'
        res += '\n'.join(
            [str(i).rjust(row_width) + ' ' + ''.join(
                [str(c if (c := self[i, j]) is not None else '.').ljust(col_width) for j in j_range]
            ) for i in i_range]
        )

        return res

    def __len__(self):
        return len(self.__contents)
