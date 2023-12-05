# soil_fertilizer.py

import bisect
import numpy as np
import pandas as pd
import parse
from pathlib import Path
import sys
from tqdm import tqdm
from typing import List


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = {}

    # Seeds
    seeds_str = parse.search("Seeds: {seeds}\n", puzzle_input)["seeds"]
    parsed_input["seeds"] = [x["seed"] for x in parse.findall("{seed:d}", seeds_str)]

    # Mappings
    map_names = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]

    for map_name, map_input in zip(map_names, puzzle_input.split("\n\n")[1:]):
        search_string = f"{map_name} map:\n"
        map_str = map_input.lstrip(search_string)

        map_details = []
        for line in map_str.split("\n"):
            map_details.append([x["num"] for x in parse.findall("{num:d}", line)])

        parsed_input[map_name] = map_details

    return parsed_input


class Mapper:
    def __init__(self, map_input: List[List], reverse=False):
        self._map = self._convert_map_input(map_input, reverse=reverse)

    def _convert_map_input(self, map_input: List[List], reverse=False) -> np.ndarray:
        # Format: destination_range_start | source_range_start | range_length
        # Output format: "dest_start" | "source_start" | "source_end_excl" | "range_length",

        if reverse:
            data = [[x[1], x[0], x[0] + x[2], x[2]] for x in map_input]
        else:
            data = [[x[0], x[1], x[1] + x[2], x[2]] for x in map_input]

        curr_map = (
            pd.DataFrame(
                columns=[
                    "dest_start",
                    "source_start",
                    "source_end_excl",
                    "range_length",
                ],
                data=data,
            )
            .sort_values(["source_start"])
            .reset_index(drop=True)
        )

        return curr_map.to_numpy()

    def map(self, source_val: int) -> int:
        source_starts = self._map[:, 1]

        curr_start_idx = bisect.bisect(source_starts, source_val)

        if curr_start_idx == 0:
            # Prior to start of mapping
            return source_val
        elif (curr_start_idx >= len(source_starts)) and (
            source_val >= self._map[curr_start_idx - 1, 2]
        ):
            # Beyond range of mapping
            return source_val
        else:
            new_value = self._map[curr_start_idx - 1, 0] + (
                source_val - source_starts[curr_start_idx - 1]
            )
            return new_value

        return source_val


def part1(data):
    """
    Solve part 1

    Each line within a map contains three numbers: the destination range start, the source range start, and the range length

    Find the lowest location number that corresponds to any of the initial seeds
    """

    map_sequence = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]

    mappers = []
    for map_name in map_sequence:
        mappers.append(Mapper(data[map_name]))

    location_numbers = []
    for seed in data["seeds"]:
        curr_val = seed

        for mapper in mappers:
            curr_val = mapper.map(curr_val)

        location_numbers.append(curr_val)

    return min(location_numbers)


def part2(data):
    """
    Solve part 2

    What is the lowest location number that corresponds to any of the initial seed numbers?
    """

    map_sequence = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]

    mappers = []
    for map_name in map_sequence:
        mappers.append(Mapper(data[map_name]))

    min_location_number = np.infty

    # Extract seeds from range
    for seed_start, seed_range in zip(data["seeds"][0::2], data["seeds"][1::2]):
        for seed in tqdm(range(seed_start, seed_start + seed_range)):
            curr_val = seed

            for mapper in mappers:
                curr_val = mapper.map(curr_val)

            if curr_val < min_location_number:
                min_location_number = curr_val

    return min_location_number


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
