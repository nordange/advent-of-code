# hot_springs.py

from collections import Counter
import functools
from itertools import product
import numpy as np
import parse
from pathlib import Path
import sys
from tqdm import tqdm


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = []
    for line in puzzle_input.split("\n"):
        springs = parse.search("{springs} ", line)["springs"]
        damage_groups = [res["num"] for res in parse.findall("{num:d}", line)]

        parsed_input.append({"springs": springs, "damage_groups": damage_groups})

    return parsed_input


def generate_possibilities(springs, damage_groups):
    counts = Counter(springs)
    unknown_idx = [i for i, character in enumerate(springs) if character == "?"]

    possibilities = set()

    springs_arr = np.array(list(springs))
    for combo in product("#.", repeat=counts["?"]):
        for idx, character in zip(unknown_idx, combo):
            springs_arr[idx] = character
        curr_springs = "".join(springs_arr)
        groups = [len(x) for x in curr_springs.split(".") if len(x)]
        if groups == damage_groups:
            possibilities.update([curr_springs])

    return len(possibilities)


@functools.cache
def count_possibilities(springs, damage_groups, curr_group_size):
    """
    Recursive functions

    Inspired by https://github.com/AlbertVeli/AdventOfCode/blob/master/2023/12/12_2.py

    Parameters
    ----------
    springs : str
        String representation of the springs
    damage_groups : list
        Damage groups we are looking for
    curr_group_size
        The current group size
    """

    if len(springs) == 0:
        if (len(damage_groups) == 0) and (curr_group_size == 0):
            # We are finished
            return 1
        elif (len(damage_groups) == 1) and (curr_group_size == damage_groups[0]):
            # One group left, size is the same as the current group
            return 1
        else:
            # No match
            return 0

    if (len(damage_groups) > 0) and (curr_group_size > damage_groups[0]):
        # The current group is too large
        return 0

    num_possibilities = 0

    curr_spring = springs[0]

    if curr_spring in "#?":
        num_possibilities += count_possibilities(
            springs[1:], damage_groups, curr_group_size + 1
        )

    if curr_spring in ".?":
        # Group size has to be zero
        if (len(damage_groups) > 0) and (curr_group_size == damage_groups[0]):
            num_possibilities += count_possibilities(springs[1:], damage_groups[1:], 0)

        elif curr_group_size == 0:
            num_possibilities += count_possibilities(springs[1:], damage_groups, 0)

    return num_possibilities


def part1(data):
    """Solve part 1"""

    possibilities = []
    for row in tqdm(data):
        springs = row["springs"]
        damage_groups = row["damage_groups"]
        possibilities.append(generate_possibilities(springs, damage_groups))

    return sum(possibilities)


def part2(data):
    """Solve part 2"""

    possibilities = []
    for row in tqdm(data):
        springs = "?".join([row["springs"]] * 5)
        damage_groups = tuple(row["damage_groups"]) * 5
        possibilities.append(count_possibilities(springs, damage_groups, 0))

    return sum(possibilities)


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
