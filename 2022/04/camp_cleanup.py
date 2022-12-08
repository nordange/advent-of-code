# camp_cleanup.py

import numpy as np
from pathlib import Path
import sys


def parse(puzzle_input):
    """Parse input"""

    all_elf_sections = []

    for line in puzzle_input.split():

        line_elf_sections = []

        for elf_sections in line.split(","):
            limits = elf_sections.strip().split("-")
            line_elf_sections.append(
                np.arange(int(limits[0]), int(limits[1]) + 1).tolist()
            )

        all_elf_sections.append(line_elf_sections)

    return all_elf_sections


def part1(data):
    """Solve part 1"""
    # Count in how many assignment pairs one range fully contain the other

    counter = 0

    for elf_sections in data:

        total_range = set(elf_sections[0])
        for new_section in elf_sections[1:]:
            total_range = total_range.union(set(new_section))

        max_length_original_set = max([len(x) for x in elf_sections])

        if len(total_range) == max_length_original_set:
            counter += 1

    return counter


def part2(data):
    """Solve part 2"""
    # In how many assignment pairs do the ranges overlap

    counter = 0

    for elf_sections in data:
        total_range = set(elf_sections[0])
        for new_section in elf_sections[1:]:
            total_range = total_range.union(set(new_section))

        if len(total_range) < sum([len(x) for x in elf_sections]):
            counter += 1

    return counter


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

        print("\n".join(str(solution) for solution in solutions))
