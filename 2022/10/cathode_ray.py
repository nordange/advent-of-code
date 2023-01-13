# cathode_ray.py

import numpy as np
from pathlib import Path
import sys


def parse(puzzle_input):
    """Parse input"""

    puzzle_input_lines = puzzle_input.split("\n")

    input_data = []

    for puzzle_input_line in puzzle_input_lines:
        curr_line_splitted = puzzle_input_line.split(" ")
        if len(curr_line_splitted) == 2:
            input_data.append([curr_line_splitted[0], int(curr_line_splitted[1])])
        else:
            input_data.append(curr_line_splitted)

    return input_data


class RegisterX:
    def __init__(self):
        self.X = [1]

    def current_value(self):
        return self.X[-1]

    def addx(self, value):

        self.X.extend([self.X[-1]])
        # Starting value next cycle
        self.X.append(self.X[-1] + value)

    def noop(self):
        # Starting value next cycle
        self.X.append(self.X[-1])


def part1(data):
    """Solve part 1
    Register X starts at 1
    addx V takes two cycles to complete. After two cycles, X is increased by V
    noop takes one cycle to complete
    signal_strength = cycle_number * X

    """

    reg = RegisterX()

    for curr_instruction in data:
        if curr_instruction[0] == "noop":
            reg.noop()
        if curr_instruction[0] == "addx":
            reg.addx(curr_instruction[1])

    reg_idx = np.arange(19, 220, 40)
    reg_vals = np.array(reg.X[19:220:40])

    sum_signal_strength = sum((1 + reg_idx) * reg_vals)

    return sum_signal_strength


def draw_crt(register: list, screen_height: int, screen_width: int) -> list:
    """
    Register X controls the horizontal position of a sprite.
    The sprite is 3 pixels wide.
    Register X sets the horizontal position of the middle of the sprite.
    The CRT draws a single pixel during each cycle.
    Determine whether the sprite is visible the instant each pixel is drawn
    """

    curr_cycle = 0
    crt_lines = []
    for row in range(0, screen_height):
        curr_crt_line = ""
        for x_pos in range(0, screen_width):
            if (register[curr_cycle] >= x_pos - 1) and (
                register[curr_cycle] <= x_pos + 1
            ):
                curr_crt_line += "#"
            else:
                curr_crt_line += "."
            curr_cycle += 1

        crt_lines.append(curr_crt_line)

    return crt_lines


def part2(data):
    """Solve part 2"""

    reg = RegisterX()

    for curr_instruction in data:
        if curr_instruction[0] == "noop":
            reg.noop()
        if curr_instruction[0] == "addx":
            reg.addx(curr_instruction[1])

    crt_lines = draw_crt(reg.X, screen_height=6, screen_width=40)

    print("\n")
    for crt_line in crt_lines:
        print(crt_line)
    print("\n")

    return crt_lines


def solve(puzzle_input):
    """Solve the entire puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = Path(path).read_text().strip()

        solutions = solve(puzzle_input)

        print(str(solutions[0]))

        print("\n")
        for crt_line in solutions[1]:
            print(crt_line)
        print("\n")
