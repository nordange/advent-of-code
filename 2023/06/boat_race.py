# boat_race.py

import numpy as np
import parse
from pathlib import Path
import sys


def parse_input(puzzle_input):
    """Parse input"""

    raw_durations, raw_distances = puzzle_input.split("\n")

    durations = [
        res["race_duration"]
        for res in parse.findall("{race_duration:d}", raw_durations)
    ]
    distances = [
        res["distance"] for res in parse.findall("{distance:d}", raw_distances)
    ]

    parsed_input = []

    for curr_duration, curr_distance in zip(durations, distances):
        parsed_input.append({"duration": curr_duration, "distance": curr_distance})

    return parsed_input


def ways_to_win(duration, distance):
    # duration_button (=speed) | distance

    res = np.zeros((duration + 1, 2))

    res[:, 0] = np.arange(0, duration + 1)
    res[:, 1] = res[:, 0] * (duration - res[:, 0])

    num_ways = (res[:, 1] > distance).sum()

    return num_ways


def part1(data):
    """
    Solve part 1

    Determine the number of ways you can beat the record in each race.

    What do you get if you multiply these numbers together?
    """

    num_ways = []
    for race in data:
        num_ways.append(ways_to_win(race["duration"], race["distance"]))

    return np.prod(num_ways)


def part2(data):
    """Solve part 2"""

    total_duration = int("".join([str(race["duration"]) for race in data]))
    total_distance = int("".join([str(race["distance"]) for race in data]))

    num_ways = ways_to_win(total_duration, total_distance)

    return num_ways


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
