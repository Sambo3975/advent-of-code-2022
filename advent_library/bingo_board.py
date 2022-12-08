from colorama import Fore, Style
from math import floor, log10, sqrt


class BingoBoard:
    """A Bingo board. This is not the standard Bingo board, though. You can't win on diagonals, and any number may
    appear in any column """

    def __init__(self, contents, diagonal_win=False):

        self.contents = contents
        self.diagonal_win = diagonal_win

        self.tile_digits = floor(log10(max(contents))) + 2
        self.marks = [False for _ in range(len(contents))]
        self.size = int(sqrt(len(contents)))

        self.last_call = None
        self.win = None
        self.called_on_board = False

    def call(self, number):
        """If the called number is in the board, mark it. Then, if the called number resulted in a win, return the
        score of the win. Otherwise, return False. """

        self.last_call = number

        # Mark the number if it is on the board

        marked = False
        for i in range(len(self.contents)):
            if self.contents[i] == number:
                self.marks[i] = True
                self.called_on_board = True
                marked = True
                break
        # Can't have won if no new number was marked
        if not marked:
            self.called_on_board = False
            return False

        # Determine if a winning number was called

        win = False
        # Check for a win on a row
        for i in range(0, len(self.contents), self.size):
            for j in range(self.size):
                if not self.marks[i + j]:
                    break
                if j == self.size - 1:
                    self.win = [x for x in range(i, i + self.size, 1)]
                    win = True
            if win:
                break
        # Check for a win in a column
        if not win:
            for i in range(self.size):
                for j in range(0, len(self.contents), self.size):
                    if not self.marks[i + j]:
                        break
                    if j == len(self.contents) - self.size:
                        self.win = [x for x in range(i, len(self.contents), self.size)]
                        win = True
                if win:
                    break
        # Check for a diagonal win
        if not win and self.diagonal_win:
            for i in range(0, len(self.contents), self.size + 1):
                if not self.marks[i]:
                    break
                if i == len(self.contents) - 1:
                    self.win = [x for x in range(0, len(self.contents), self.size + 1)]
                    win = True
            if not win:
                for i in range(self.size - 1, len(self.contents) - 1, self.size - 1):
                    if not self.marks[i]:
                        break
                    if i == len(self.contents) - self.size:
                        self.win = [x for x in range(self.size - 1, len(self.contents) - 1, self.size - 1)]
                        win = True

        # Handle winning

        if win:

            # Score = (sum of all unmarked numbers) * (last called number)
            score = 0
            for i in range(len(self.contents)):
                if not self.marks[i]:
                    score += self.contents[i]
            return score * number
        return False


def draw_boards(*args):
    print()
    for i in range(0, len(args[0].contents), args[0].size):
        drew_first_board = False
        for board in args:
            if drew_first_board:
                print(' ' * 8, end='')
            for j in range(board.size):
                if board.marks[i + j]:
                    style = Style.NORMAL
                    if board.win and (i + j in board.win):
                        fore = Fore.YELLOW
                        style = Style.BRIGHT
                    elif board.contents[i + j] == board.last_call:
                        fore = Fore.CYAN
                        style = Style.BRIGHT
                    else:
                        fore = Fore.GREEN
                    print(fore + style + str(board.contents[i + j]).rjust(board.tile_digits, ' ') + Style.RESET_ALL,
                          end='')
                else:
                    print(str(board.contents[i + j]).rjust(board.tile_digits, ' '), end='')
            drew_first_board = True
        print()
    print()
