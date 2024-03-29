# aoc_template.py

from pathlib import Path
import sys


def parse_input(puzzle_input):
    """Parse input"""


def part1(data):
    """Solve part 1"""


def part2(data):
    """Solve part 2"""


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
