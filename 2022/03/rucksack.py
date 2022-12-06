# aoc_template.py

from pathlib import Path
import numpy as np
import string
import sys


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.split("\n")


def get_common_items(compartments: list[str]) -> str:
    """
    Get common items in rucksack compartments

    Usage examples
    >>> get_common_items(["vJrwpWtwJgWr", "hcsFMMfFFhFp"])
    'p'
    >>> get_common_items(["jqHRNqRjqzjGDLGL", "rsFMfFZSrLrFZsSL"])
    'L'
    >>> get_common_items(["PmmdzqPrV", "vPwwTWBwg"])
    'P'
    >>> get_common_items(["wMqvLMZHhHMvwLH", "jbvcjnnSBnvTQFn"])
    'v'
    >>> get_common_items(["ttgJtRGJ","QctTZtZT"])
    't'
    >>> get_common_items(["CrZsJsPPZsGz", "wwsLwLmpwMDw"])
    's'
    """

    # total_items = len(inventory)
    # first_compartment = inventory[:(total_items//2)]
    # second_compartment = inventory[(total_items//2):]

    # common_items = list(set(first_compartment).intersection(second_compartment))
    common_items = set(compartments[0])
    for compartment in compartments[1:]:
        common_items = common_items.intersection(set(compartment))

    return list(common_items)[0]


def get_item_priority(item: str) -> int:
    """
    Convert item to numeric priority

    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52

    Usage examples:
    >>> get_item_priority("p")
    16
    >>> get_item_priority("L")
    38
    >>> get_item_priority("P")
    42
    >>> get_item_priority("v")
    22
    >>> get_item_priority("t")
    20
    >>> get_item_priority("s")
    19
    """

    letters = string.ascii_lowercase + string.ascii_uppercase

    priority_map = dict(zip(letters, 1 + np.arange(len(letters))))

    return priority_map.get(item)


def part1(data):
    """Solve part 1"""

    priorities = []
    for rucksack in data:
        total_items = len(rucksack)
        first_compartment = rucksack[: (total_items // 2)]
        second_compartment = rucksack[(total_items // 2) :]

        common_items = get_common_items([first_compartment, second_compartment])

        priorities.append(get_item_priority(common_items))

    return sum(priorities)


def part2(data):
    """Solve part 2"""

    priorities = []

    groups = []  # Hold groups of three rucksacks

    counter = 0
    curr_group = []

    for rucksack in data:

        if counter == 3:
            groups.append(curr_group)
            curr_group = []
            counter = 0

        curr_group.append(rucksack)
        counter += 1

    groups.append(curr_group)

    for group in groups:
        common_items = get_common_items(group)

        priorities.append(get_item_priority(common_items))

    return sum(priorities)


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
