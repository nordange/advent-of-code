# cosmic_expansion.py

from itertools import combinations
import numpy as np
from pathlib import Path
import sys


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = []
    for line in puzzle_input.split("\n"):
        parsed_input.append(list(line))

    universe = np.array(parsed_input, dtype=str)

    return universe


def find_expansions(universe):
    row_expansions_idx = []
    for idx, row in enumerate(universe):
        if sum(row == "#") == 0:
            row_expansions_idx.append(idx)

    col_expansions_idx = []
    for idx, col in enumerate(universe.T):
        if sum(col == "#") == 0:
            col_expansions_idx.append(idx)

    return row_expansions_idx, col_expansions_idx


def calculate_distance(
    coord1, coord2, row_expansion_idx, col_expansion_idx, expansion_factor=2
):
    y1, x1 = coord1
    y2, x2 = coord2

    extra_x = len(
        set(range(min(x1, x2), max(x1, x2) + 1)).intersection(set(col_expansion_idx))
    )
    extra_y = len(
        set(range(min(y1, y2), max(y1, y2) + 1)).intersection(set(row_expansion_idx))
    )

    distance_rows = abs(x2 - x1) + extra_x * (expansion_factor - 1)
    distance_cols = abs(y2 - y1) + extra_y * (expansion_factor - 1)

    return distance_rows + distance_cols


def part1(data):
    """Solve part 1"""

    row_expansion_idx, col_expansion_idx = find_expansions(data)

    galaxy_idxs = np.where(data == "#")
    galaxy_coords = list(zip(galaxy_idxs[0], galaxy_idxs[1]))

    pairs = combinations(galaxy_coords, 2)

    galaxy_distances = []
    for coord1, coord2 in pairs:
        curr_dist = calculate_distance(
            coord1, coord2, row_expansion_idx, col_expansion_idx
        )
        galaxy_distances.append(curr_dist)

    return sum(galaxy_distances)


def part2(data, expansion_factor=1000000):
    """Solve part 2"""
    row_expansion_idx, col_expansion_idx = find_expansions(data)

    galaxy_idxs = np.where(data == "#")
    galaxy_coords = list(zip(galaxy_idxs[0], galaxy_idxs[1]))

    pairs = combinations(galaxy_coords, 2)

    galaxy_distances = []
    for coord1, coord2 in pairs:
        curr_dist = calculate_distance(
            coord1,
            coord2,
            row_expansion_idx,
            col_expansion_idx,
            expansion_factor=expansion_factor,
        )
        galaxy_distances.append(curr_dist)

    return sum(galaxy_distances)


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
