# point_of_incidence.py

import numpy as np
from pathlib import Path
import sys


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = []
    for block in puzzle_input.split("\n\n"):
        parsed_block = []
        for line in block.split("\n"):
            parsed_block.append(list(line))
        parsed_input.append(np.array(parsed_block, dtype=str))

    return parsed_input


def find_vertical_reflection(block, smudge=False):
    num_rows, num_cols = block.shape

    reflection_deviations = []
    reflection_idxs = []
    for idx in range(0, num_cols - 1):
        curr_deviation = num_rows - np.equal(block[:, idx], block[:, idx + 1]).sum()
        if smudge:
            if curr_deviation <= 1:
                reflection_idxs.append(idx)
                reflection_deviations.append(curr_deviation)
        else:
            if curr_deviation == 0:
                reflection_idxs.append(idx)
                reflection_deviations.append(curr_deviation)

    for reflection_idx, reflection_deviation in zip(
        reflection_idxs, reflection_deviations
    ):
        reflection_length = min(reflection_idx, num_cols - (reflection_idx + 2))

        left_range = range(
            reflection_idx - 1, reflection_idx - 1 - reflection_length, -1
        )
        right_range = range(
            reflection_idx + 2, reflection_idx + 2 + reflection_length + 1
        )

        deviations = [reflection_deviation]
        for left, right in zip(left_range, right_range):
            deviation = num_rows - np.equal(block[:, left], block[:, right]).sum()
            deviations.append(deviation)

        if smudge and sum(deviations) == 1:
            return reflection_idx + 1
        elif not smudge and sum(deviations) == 0:
            return reflection_idx + 1

    return 0


def find_horizontal_reflection(block, smudge=False):
    return find_vertical_reflection(block.T, smudge=smudge)


def part1(data):
    """Solve part 1"""

    results = []
    for block in data:
        vertical_reflection = find_vertical_reflection(block)
        if vertical_reflection > 0:
            results.append(vertical_reflection)
        else:
            horizontal_reflection = find_horizontal_reflection(block)
            results.append(100 * horizontal_reflection)

    return sum(results)


def part2(data):
    """Solve part 2"""

    results = []
    for block in data:
        vertical_reflection = find_vertical_reflection(block, smudge=True)
        if vertical_reflection > 0:
            results.append(vertical_reflection)
        else:
            horizontal_reflection = find_horizontal_reflection(block, smudge=True)
            results.append(100 * horizontal_reflection)

    return sum(results)


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
