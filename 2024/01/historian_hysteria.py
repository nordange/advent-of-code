# historian_hysteria.py

from collections import defaultdict
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

    return np.array(parsed_input)


def part1(data):
    """Solve part 1"""

    sorted_array = np.sort(data, axis=0)

    dist = np.abs(sorted_array[:, 0] - sorted_array[:, 1])

    return dist.sum()


def part2(data):
    """Solve part 2"""

    # First, count the number of occurences of each entry in the second list
    unique, counts = np.unique(data[:, 1], return_counts=True)

    count_dict = defaultdict(int)

    counts = dict(zip(unique, counts))
    count_dict.update(counts)

    similarity = 0
    for number in data[:, 0]:
        similarity += number * count_dict[number]

    return similarity


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
