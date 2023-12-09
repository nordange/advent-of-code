# mirage_maintenance.py

import numpy as np
import parse
from pathlib import Path
import sys


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = []
    for line in puzzle_input.split("\n"):
        parsed_line = [x["number"] for x in parse.findall("{number:d}", line)]
        parsed_input.append(parsed_line)

    return parsed_input


def predict_value(history):
    curr_diffs = np.diff(history)
    curr_sum = np.absolute(curr_diffs).sum()

    values = [history[-1]]
    while curr_sum != 0:
        values.append(curr_diffs[-1])

        curr_diffs = np.diff(curr_diffs)
        curr_sum = np.absolute(curr_diffs).sum()

    return sum(values)


def predict_value_backwards(history):
    curr_diffs = np.diff(history)
    curr_sum = np.absolute(curr_diffs).sum()

    prev_values = [history[0]]
    while curr_sum != 0:
        prev_values.append(curr_diffs[0])

        curr_diffs = np.diff(curr_diffs)
        curr_sum = np.absolute(curr_diffs).sum()

    # Rebuild backwards
    curr_value = 0
    for prev_value in prev_values[::-1]:
        curr_value = prev_value - curr_value

    return curr_value


def part1(data):
    """
    Solve part 1

    What is the sum of these extrapolated values?
    """

    predicted_values = []
    for history in data:
        predicted_values.append(predict_value(history))

    return sum(predicted_values)


def part2(data):
    """Solve part 2"""

    predicted_values = []
    for history in data:
        predicted_values.append(predict_value_backwards(history))

    return sum(predicted_values)


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
