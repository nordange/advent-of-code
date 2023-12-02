# cube_conundrum.py

import numpy as np
import parse
from pathlib import Path
import sys


def parse_input(puzzle_input):
    """Parse input"""

    cubes_per_game = {}
    for line in puzzle_input.split("\n"):
        game_id_search = parse.search("Game {game_id:d}:", line)

        game_id = game_id_search["game_id"]
        game_start_idx = game_id_search.spans["game_id"][1]

        cubes_per_game[game_id] = []
        for game in line[game_start_idx:].lstrip(": ").split(";"):
            game_res = {}
            for colour in ["red", "green", "blue"]:
                colour_search_string = f"{{cube_num:d}} {colour}"
                res = parse.search(colour_search_string, game)

                if res is not None:
                    game_res[colour] = res["cube_num"]
            cubes_per_game[game_id].append(game_res)

    return cubes_per_game


def is_game_valid(game_draw, max_cubes):
    for colour, max_cube in max_cubes.items():
        if max_cube < game_draw.get(colour, 0):
            return False
    return True


def part1(data):
    """
    Solve part 1

    Which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

    What is the sum of the IDs of those games?
    """

    max_cubes = {"red": 12, "green": 13, "blue": 14}

    valid_game_ids = []
    for game_id, game_draws in data.items():
        temp_valid_games = []
        for game_draw in game_draws:
            temp_valid_games.append(is_game_valid(game_draw, max_cubes))

        if all(temp_valid_games):
            valid_game_ids.append(game_id)

    return sum(valid_game_ids)


def find_minimum_cubes(game_draws):
    minimum_cubes = {}
    for colour in ["red", "green", "blue"]:
        minimum_cubes[colour] = max(
            [game_draw.get(colour, 0) for game_draw in game_draws]
        )

    return minimum_cubes


def part2(data):
    """
    Solve part 2

    What is the fewest number of cubes of each color that could have been in the bag to make the game possible?

    For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
    """

    powers = []

    for game_id, game_draws in data.items():
        minimum_cubes = find_minimum_cubes(game_draws)
        power = np.prod(list(minimum_cubes.values()))
        powers.append(power)

    return sum(powers)


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
