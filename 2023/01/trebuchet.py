# trebuchet.py

import parse
from pathlib import Path
import regex as re
import sys


def parse_input(puzzle_input):
    """Parse input"""

    lines = puzzle_input.split("\n")

    return lines


def get_digits(data):
    line_digits = []

    for line in data:
        curr_digits = [result["digit"] for result in parse.findall("{digit:1d}", line)]

        line_digits.append(curr_digits)

    return line_digits


def get_digits_with_text(data):
    text_digits_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    digits_pattern = "|".join([r"\d"] + list(text_digits_map.keys()))

    line_digits = []

    for line in data:
        raw_digits = re.findall(digits_pattern, line, overlapped=True)

        curr_digits = []
        for raw_digit in raw_digits:
            try:
                curr_digits.append(int(raw_digit))
            except ValueError:
                curr_digits.append(text_digits_map[raw_digit])

        line_digits.append(curr_digits)

    return line_digits


def part1(data):
    """
    Solve part 1

    Calibration values: Two digit number formed by first and last digit in each string (line)

    What is the sum of all the calibration values?

    """

    line_digits = get_digits(data)

    calibration_values = []

    for digits in line_digits:
        calibration_value = 10 * digits[0] + digits[-1]
        calibration_values.append(calibration_value)

    return sum(calibration_values)


def part2(data):
    """
    Solve part 2

    Calibration values: Can also contain digits spelled out by letters

    What is the sum of all the calibration values?

    """

    line_digits = get_digits_with_text(data)

    calibration_values = []

    for digits in line_digits:
        calibration_value = 10 * digits[0] + digits[-1]
        calibration_values.append(calibration_value)

    return sum(calibration_values)


def solve(puzzle_input):
    """Solve the entire puzzle for the given input"""
    data = parse_input(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = Path(path).read_text().strip()

        solutions = solve(puzzle_input)

        print("\n".join(str(solution) for solution in solutions))
