# parabolic_reflector_dish.py

import functools
from itertools import pairwise
import numpy as np
from pathlib import Path
import sys


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = []
    for line in puzzle_input.split("\n"):
        parsed_input.append(list(line))

    return np.array(parsed_input, dtype=str)


def tilt_platform_north(data):
    platform = np.insert(
        data, [0, data.shape[0]], np.repeat("#", data.shape[1]), axis=0
    )

    for col_idx in range(platform.shape[1]):
        platform_col = platform[:, col_idx]

        fixed_rock_idx = np.where(platform_col == "#")[0]

        for from_idx, to_idx in pairwise(fixed_rock_idx):
            platform_col[(from_idx + 1) : (to_idx)] = np.sort(
                platform_col[(from_idx + 1) : to_idx]
            )[::-1]

    return platform[1:-1, :]


@functools.cache
def tilt_column(column):
    curr_col = np.array(column)
    fixed_rock_idx = np.where(curr_col == "#")[0]

    for from_idx, to_idx in pairwise(fixed_rock_idx):
        curr_col[(from_idx + 1) : (to_idx)] = np.sort(
            curr_col[(from_idx + 1) : to_idx]
        )[::-1]

    return curr_col


def tilt_platform(extended_platform, direction):
    if direction == "N":
        for col_idx in range(1, extended_platform.shape[1]):
            extended_platform[:, col_idx] = tilt_column(
                tuple(extended_platform[:, col_idx])
            )
    elif direction == "W":
        for row_idx in range(1, extended_platform.shape[0]):
            extended_platform[row_idx, :] = tilt_column(
                tuple(extended_platform[row_idx, :])
            )
    elif direction == "S":
        for col_idx in range(1, extended_platform.shape[1]):
            extended_platform[:, col_idx] = tilt_column(
                tuple(extended_platform[:, col_idx][::-1])
            )[::-1]
    elif direction == "E":
        for row_idx in range(1, extended_platform.shape[0]):
            extended_platform[row_idx, :] = tilt_column(
                tuple(extended_platform[row_idx, :][::-1])
            )[::-1]

    return extended_platform


def cycle_platform(data, cycles):
    platform = np.full((data.shape[0] + 2, data.shape[1] + 2), "#")
    platform[1:-1, 1:-1] = data

    for i in range(cycles):
        platform = tilt_platform(platform, "N")
        platform = tilt_platform(platform, "W")
        platform = tilt_platform(platform, "S")
        platform = tilt_platform(platform, "E")

    return platform[1:-1, 1:-1]


def hash_matrix(matrix):
    hash = ""
    for row in matrix:
        hash += "".join(row.tolist())

    return hash


def part1(data):
    """Solve part 1"""

    tilted = tilt_platform_north(data)

    weights = np.arange(tilted.shape[0], 0, -1)
    num_rocks = (tilted == "O").sum(axis=1)

    load = (num_rocks * weights).sum()

    return load


def part2(data):
    """Solve part 2"""

    # Cycle until pattern repeat itself
    platform = cycle_platform(data, 1)
    patterns = [hash_matrix(platform)]

    num_cycles = 1000000000

    for cycle_idx in range(2, num_cycles + 1):
        platform = cycle_platform(platform, 1)
        hash = hash_matrix(platform)

        if hash in patterns:
            break
        else:
            patterns.append(hash)

    # It does not necessarily repeat from the initial condition
    repeat_cycle_idx = len(patterns) - patterns.index(hash)

    equivalent_cycles = repeat_cycle_idx + num_cycles % repeat_cycle_idx

    final_platform = cycle_platform(data, equivalent_cycles)

    weights = np.arange(final_platform.shape[0], 0, -1)
    num_rocks = (final_platform == "O").sum(axis=1)

    load = (num_rocks * weights).sum()

    return load


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
