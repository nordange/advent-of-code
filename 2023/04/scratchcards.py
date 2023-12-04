# scratchcards.py

from copy import deepcopy
import numpy as np
import parse
from pathlib import Path
import sys


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = {}

    for line in puzzle_input.split("\n"):
        card_id_match = parse.search("{card_id:d}:", line)
        card_id = card_id_match["card_id"]

        wins_str, own_str = (
            line[(card_id_match.spans["card_id"][1] + 1) :].strip().split("|")
        )

        wins = [match["number"] for match in parse.findall("{number:d}", wins_str)]
        own = [match["number"] for match in parse.findall("{number:d}", own_str)]

        parsed_input[card_id] = {"winning_numbers": wins, "own_numbers": own}

    return parsed_input


def part1(data):
    """
    Solve part 1

    The first match makes the card worth one point and each match after the first doubles the point value of that card

    How many points are they worth in total?

    """

    card_points = []

    for idx, scratchcard in data.items():
        correct_numbers = len(
            set(scratchcard["winning_numbers"]).intersection(
                set(scratchcard["own_numbers"])
            )
        )

        if correct_numbers > 0:
            card_points.append(np.power(2, correct_numbers - 1))

    return sum(card_points)


def part2(data):
    """
    Solve part 2

    Including the original set of scratchcards, how many total scratchcards do you end up with?
    """

    scratchcards = deepcopy(data)

    for idx, scratchcard in scratchcards.items():
        scratchcard.update({"copies": 1})

    min_id = min(scratchcards.keys())
    max_id = max(scratchcards.keys())

    for idx in range(min_id, max_id + 1):
        correct_numbers = len(
            set(scratchcards[idx]["winning_numbers"]).intersection(
                set(scratchcards[idx]["own_numbers"])
            )
        )

        for copy_idx in range(idx + 1, idx + 1 + correct_numbers):
            scratchcards[copy_idx]["copies"] = (
                scratchcards[copy_idx]["copies"] + scratchcards[idx]["copies"]
            )

    num_scratchcards = sum(
        [scratchcard["copies"] for scratchcard in scratchcards.values()]
    )

    return num_scratchcards


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
