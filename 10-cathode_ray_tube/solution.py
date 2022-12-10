import pyperclip

from option_selection import OptionSelector
from testing import test_bed


class CommunicationCPU:
    def __init__(self, render_program: bool = True):
        self.instructions = None
        self.registers = {'x': 0}
        self.cycle_number = 0
        self.cycles_until_instruction_done = 0
        self.register_diagnostic_cycle = 0
        self.diagnostics: list[int] = []
        self.instruction_lookup = {
            'noop': (1, self._noop),
            'addx': (2, self._addx),
        }
        self.instruction_function = None
        self.instruction_arguments = None
        self.render_program = render_program

    def __repr__(self):
        return 'CommunicationCPU()'

    def _noop(self, _: tuple):
        pass

    def _addx(self, args: tuple):
        self.registers['x'] += args[1]

    @staticmethod
    def parse_instruction(instruction: str):
        instruction: list = instruction.split(' ')
        for i in range(1, len(instruction)):
            instruction[i] = int(instruction[i])
        return instruction

    def load_program(self, path: str):
        with open(path, 'r') as f:
            self.instructions = [self.parse_instruction(instruction) for instruction in f.read().rstrip().split('\n')]

    def start_instruction(self):
        instruction = self.instructions[0]
        (delay, call) = self.instruction_lookup[instruction[0]]
        self.cycles_until_instruction_done = delay
        self.instruction_function = call
        self.instruction_arguments = instruction
        self.instructions = self.instructions[1:]

    def finish_instruction(self):
        self.instruction_function(self.instruction_arguments)

    def execute_program(self, path: str = None):
        if path is not None:
            self.load_program(path)
        self.register_diagnostic_cycle = 20
        self.cycle_number = 0
        self.registers['x'] = 1
        while len(self.instructions) > 0:
            self.start_instruction()
            while self.cycles_until_instruction_done > 0:

                if self.render_program:
                    draw_position = self.cycle_number % 40
                    output = '#' if draw_position - 1 <= self.registers['x'] <= draw_position + 1 else ' '
                    end = '\n' if (draw_position + 1) % 40 == 0 else ''
                    print(output, end=end)

                self.cycle_number += 1
                self.cycles_until_instruction_done -= 1

                if self.cycle_number == self.register_diagnostic_cycle:
                    self.register_diagnostic_cycle += 40
                    self.diagnostics.append(self.registers['x'] * self.cycle_number)
            self.finish_instruction()
        return sum(self.diagnostics)


def test_small_example_program():
    cpu = CommunicationCPU(False)
    cpu.execute_program('test.txt')
    test_bed(lambda x: x.registers['x'], (cpu,), (-1,))


def test_large_example_program():
    cpu = CommunicationCPU(False)
    test_bed(cpu.execute_program, ('test2.txt',), (13140,))


def test_render_program():
    cpu = CommunicationCPU()
    cpu.execute_program('test2.txt')


def part_1():
    cpu = CommunicationCPU(False)
    sum_of_signal_strengths = cpu.execute_program('input.txt')
    print(f'Sum of signal strengths: {sum_of_signal_strengths}')
    pyperclip.copy(sum_of_signal_strengths)
    print('Copied to clipboard!')
    
    
def part_2():
    cpu = CommunicationCPU()
    cpu.execute_program('input.txt')


def main():
    print('Day 10 - Cathode-Ray Tube')
    selector = OptionSelector()
    selector.add_option('1', 'part 1', part_1)
    selector.add_option('2', 'part 2', part_2)
    selector.add_option('ts', 'test small example program', test_small_example_program)
    selector.add_option('tl', 'test large example program', test_large_example_program)
    selector.add_option('tr', 'test program rendering', test_render_program)
    selector.run()


if __name__ == '__main__':
    main()
