# lava_floor.py

from collections import defaultdict
import numpy as np
from pathlib import Path
import sys
from tqdm import tqdm

sys.setrecursionlimit(5000)

DIRECTION_PASSTHROUGH = {"N": "S", "S": "N", "W": "E", "E": "W"}


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = []
    for line in puzzle_input.split("\n"):
        parsed_input.append(list(line))

    return np.array(parsed_input, dtype=str)


class Grid:
    def __init__(self, input_grid):
        self.num_rows, self.num_cols = input_grid.shape
        self.tiles = []

        for row_idx, row in enumerate(input_grid):
            row_tiles = []
            for col_idx, value in enumerate(row):
                tile_id = self.coord_to_tile_id((row_idx, col_idx))
                row_tiles.append(Tile(value, row_idx, col_idx, tile_id))
            self.tiles.append(row_tiles)

    def is_valid_coord(self, coord):
        return (0 <= coord[0] < self.num_rows) and (0 <= coord[1] < self.num_cols)

    def coord_to_tile_id(self, coord):
        tile_id = coord[0] * self.num_cols + coord[1]

        return tile_id

    def tile_id_to_coord(self, tile_id):
        row = tile_id // self.num_cols
        col = tile_id % self.num_cols

        return (row, col)

    def get_next_beam_tiles(self, curr_tile, incoming):
        outgoing = curr_tile.transmit(incoming)

        next_tiles = []
        for new_dir in outgoing:
            if new_dir == "N":
                new_coord = curr_tile.row - 1, curr_tile.col
            elif new_dir == "W":
                new_coord = curr_tile.row, curr_tile.col - 1
            elif new_dir == "S":
                new_coord = curr_tile.row + 1, curr_tile.col
            elif new_dir == "E":
                new_coord = curr_tile.row, curr_tile.col + 1

            if self.is_valid_coord(new_coord):
                next_tiles.append(
                    (
                        self.tiles[new_coord[0]][new_coord[1]],
                        DIRECTION_PASSTHROUGH[new_dir],
                    )
                )

        return next_tiles

    def dfs(self, curr_tile, visited, incoming):
        visited[curr_tile.tile_id].update(incoming)

        candidates = self.get_next_beam_tiles(curr_tile, incoming)

        for neighbour_tile, next_incoming in candidates:
            if next_incoming not in visited[neighbour_tile.tile_id]:
                self.dfs(neighbour_tile, visited, next_incoming)

        return visited

    def beam(self, start_coord, incoming):
        visited = defaultdict(set)

        curr_tile = self.tiles[start_coord[0]][start_coord[1]]

        visited = self.dfs(curr_tile, visited, incoming)

        return visited


class Tile:
    def __init__(self, symbol, row, col, tile_id=None):
        self.symbol = symbol
        self.row = row
        self.col = col
        self.tile_id = tile_id

    def __repr__(self):
        return f"[{self.row}, {self.col}] {self.symbol}"

    def transmit(self, incoming):
        if self.symbol == ".":
            outgoing = [DIRECTION_PASSTHROUGH[incoming]]
        elif self.symbol == "/":
            if incoming == "E":
                outgoing = ["S"]
            elif incoming == "N":
                outgoing = ["W"]
            elif incoming == "W":
                outgoing = ["N"]
            elif incoming == "S":
                outgoing = ["E"]
        elif self.symbol == "\\":
            if incoming == "E":
                outgoing = ["N"]
            elif incoming == "N":
                outgoing = ["E"]
            elif incoming == "W":
                outgoing = ["S"]
            elif incoming == "S":
                outgoing = ["W"]
        elif self.symbol == "|":
            if incoming == "E":
                outgoing = ["N", "S"]
            elif incoming == "N":
                outgoing = ["S"]
            elif incoming == "W":
                outgoing = ["N", "S"]
            elif incoming == "S":
                outgoing = ["N"]
        elif self.symbol == "-":
            if incoming == "E":
                outgoing = ["W"]
            elif incoming == "N":
                outgoing = ["W", "E"]
            elif incoming == "W":
                outgoing = ["E"]
            elif incoming == "S":
                outgoing = ["W", "E"]
        return outgoing


def part1(data):
    """Solve part 1"""

    grid = Grid(data)

    visited = grid.beam((0, 0), "W")

    return len(visited.keys())


def part2(data):
    """Solve part 2"""

    grid = Grid(data)

    starting_configs = []

    # Top row:
    for idx in range(0, data.shape[1] - 1):
        starting_configs.append([(0, idx), "N"])

    # Left column
    for idx in range(0, data.shape[0] - 1):
        starting_configs.append([(idx, 0), "W"])

    # Bottom row:
    for idx in range(0, data.shape[1] - 1):
        starting_configs.append([(data.shape[0] - 1, idx), "S"])

    # Right column
    for idx in range(idx, data.shape[1] - 1):
        starting_configs.append([(idx, 0), "E"])

    # Corners
    starting_configs.append([(0, 0), "N"])
    starting_configs.append([(0, 0), "W"])

    starting_configs.append([(0, data.shape[1] - 1), "N"])
    starting_configs.append([(0, data.shape[1] - 1), "E"])

    starting_configs.append([(data.shape[0] - 1, 0), "S"])
    starting_configs.append([(data.shape[0] - 1, 0), "W"])

    starting_configs.append([(data.shape[0] - 1, data.shape[1] - 1), "S"])
    starting_configs.append([(data.shape[0] - 1, data.shape[1] - 1), "E"])

    visited = grid.beam((0, 0), "W")

    num_energizes = []
    for starting_config in tqdm(starting_configs):
        visited = grid.beam(starting_config[0], starting_config[1])
        num_energizes.append(len(visited.keys()))

    return max(num_energizes)


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
