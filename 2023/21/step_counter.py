# step_counter.py

from enum import Enum
import numpy as np
from pathlib import Path
import sys


class Direction(Enum):
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4


MOVES = {
    Direction.NORTH: np.array([-1, 0]),
    Direction.SOUTH: np.array([1, 0]),
    Direction.WEST: np.array([0, -1]),
    Direction.EAST: np.array([0, 1]),
}


def parse_input(puzzle_input):
    """Parse input"""

    raw_input = []
    for line in puzzle_input.split("\n"):
        raw_input.append(list(line))

    garden = np.array(raw_input, dtype=str)
    start_coord = np.where(garden == "S")

    # Start coord is ordinary garden plot
    garden[start_coord] = "."

    parsed_input = {
        "start_coord": (start_coord[0][0], start_coord[1][0]),
        "garden": garden,
    }

    return parsed_input


def is_valid_coord(coord, num_rows, num_cols):
    return (0 <= coord[0] < num_rows) and (0 <= coord[1] < num_cols)


def create_adjacency_list(garden_map):
    """
    Create dictionary of lists to describe which grid points are reachable from each point
    Garden plot = '.'
    Rock = '#'
    """

    adjacency_list = {}

    num_rows, num_cols = garden_map.shape

    for row in range(num_rows):
        for col in range(num_cols):
            curr_coord = np.array([row, col])
            curr_adj = []

            for move in MOVES.values():
                new_coord = curr_coord + move

                if (
                    is_valid_coord(new_coord, num_rows, num_cols)
                    and garden_map[tuple(new_coord)] == "."
                ):
                    curr_adj.append(tuple(new_coord))

            adjacency_list[tuple(curr_coord)] = curr_adj

    return adjacency_list


def count_reachable_tiles(data, num_steps):
    """
    Build adjacency list for all nodes
    Go one step, add all reachable to a set. Repeat for all reachable points.
    """

    start_coord = data["start_coord"]
    garden_map = data["garden"]

    adjacency_list = create_adjacency_list(garden_map)

    reachable = {0: set([start_coord])}

    for curr_steps in range(1, num_steps + 1):
        reachable[curr_steps] = set()

        for tile_coord in reachable[curr_steps - 1]:
            reachable[curr_steps].update(adjacency_list[tile_coord])

    return reachable


def part1(data, num_steps: int):
    """Solve part 1"""

    reachable = count_reachable_tiles(data, num_steps)

    return len(reachable[num_steps])


def part2(data):
    """Solve part 2"""


def solve(puzzle_input):
    """Solve the entire puzzle for the given input"""
    data = parse_input(puzzle_input)
    solution1 = part1(data, num_steps=64)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = Path(path).read_text().strip()

        solutions = solve(puzzle_input)

        print("\n".join(str(solution) for solution in solutions))
