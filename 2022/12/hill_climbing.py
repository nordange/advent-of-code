# hill_climbing.py

from copy import deepcopy
import numpy as np
from pathlib import Path
import string
import sys
from tqdm import tqdm


class Square:

    char_value = dict(
        zip(
            "S" + string.ascii_lowercase + "E",
            range(len("S" + string.ascii_lowercase + "E")),
        )
    )

    inverse_char_value = {val: key for key, val in char_value.items()}

    id_counter = 0

    def __init__(self, character: str, coordinates: tuple):
        self.character = character
        self.value = self.char_value[character]
        self.row_idx = coordinates[0]
        self.col_idx = coordinates[1]

        self.id = Square.id_counter
        Square.id_counter += 1

        # Algorithm specific quantities
        self.visited = False

    def get_next_lower_character(self):
        new_value = self.value - 1

        return self.inverse_char_value.get(new_value, 0)

    def get_next_higher_character(self):
        new_value = self.value + 1

        return self.inverse_char_value[new_value]


class Map:
    def __init__(self, text_map):

        self.rows = len(text_map)
        self.cols = len(text_map[0])

        self.squares = {}

        self.path = []

        self.last_lookup = {
            "top": "bottom",
            "bottom": "top",
            "left": "right",
            "right": "left",
        }

        for row_idx in range(0, self.rows):
            for col_idx in range(0, self.cols):
                self.squares[row_idx, col_idx] = Square(
                    text_map[row_idx][col_idx], (row_idx, col_idx)
                )

    def get_square_by_character(self, character):

        for coord, square in self.squares.items():
            if square.character == character:
                return square

    def get_square_by_coord(self, coords):
        return self.squares.get(coords)

    def find_shortest_path_dijkstra(self, start_square):

        distances = {square: np.infty for coord, square in self.squares.items()}
        distances[start_square] = 0

        prev_square = {square: None for coord, square in self.squares.items()}

        unvisited = list(distances.keys())
        unvisited_dist = {square: dist for square, dist in distances.items()}

        curr_square = start_square

        while len(unvisited) > 0:

            neighbors = [
                x
                for x in self.get_candidate_squares(curr_square).values()
                if x is not None
            ]

            legal_neighbors = [x for x in neighbors if x.value - curr_square.value <= 1]

            unvisited_neighbors = [x for x in legal_neighbors if not x.visited]
            unvisited_neighbors_dist = {
                square: dist
                for square, dist in distances.items()
                if square in unvisited_neighbors
            }

            while len(unvisited_neighbors) > 0:
                next_square = min(
                    unvisited_neighbors_dist, key=unvisited_neighbors_dist.get
                )

                unvisited_neighbors.remove(next_square)

                del unvisited_neighbors_dist[next_square]

                curr_dist = distances[curr_square] + 1
                if curr_dist < distances[next_square]:
                    distances[next_square] = curr_dist
                    prev_square[next_square] = curr_square

            curr_square.visited = True

            unvisited.remove(curr_square)

            unvisited_dist = {
                square: dist for square, dist in distances.items() if not square.visited
            }
            if len(unvisited_dist) > 0:
                curr_square = min(unvisited_dist, key=unvisited_dist.get)

        return distances, prev_square

    def find_shortest_path_floyd_warshall(self):

        # First generate matrix of distances between all nodes
        distances = np.ones((len(self.squares), len(self.squares)), dtype=int) * np.inf
        np.fill_diagonal(distances, 0)

        start_id = min([x.id for x in self.squares.values()])

        for square in self.squares.values():
            legal_neighbors = [
                x
                for x in self.get_candidate_squares(square).values()
                if x is not None and (x.value - square.value <= 1)
            ]
            for neighbor in legal_neighbors:
                distances[square.id - start_id, neighbor.id - start_id] = 1

        for k in tqdm(range(0, distances.shape[0])):
            for i in range(0, distances.shape[0]):
                distances[i, :] = np.minimum(
                    distances[i, :], distances[i, k] + distances[k, :]
                )

        return distances

    def get_candidate_squares(self, square):

        next_squares = {}

        next_squares["top"] = self.get_square_by_coord(
            (square.row_idx - 1, square.col_idx)
        )
        next_squares["bottom"] = self.get_square_by_coord(
            (square.row_idx + 1, square.col_idx)
        )
        next_squares["left"] = self.get_square_by_coord(
            (square.row_idx, square.col_idx - 1)
        )
        next_squares["right"] = self.get_square_by_coord(
            (square.row_idx, square.col_idx + 1)
        )

        return next_squares


def parse(puzzle_input):
    """Parse input"""

    map = Map(puzzle_input.split("\n"))

    return map


def part1(data):
    """Solve part 1"""

    map = deepcopy(data)

    start_square = map.get_square_by_character("S")
    end_square = map.get_square_by_character("E")

    distances, prev_square = map.find_shortest_path_dijkstra(start_square)
    return distances[end_square]


def part2(data):
    """Solve part 2"""

    map = deepcopy(data)

    start_id = min([x.id for x in map.squares.values()])

    end_square = map.get_square_by_character("E")

    distances = map.find_shortest_path_floyd_warshall()

    # Find all squares with level 'a'
    squares_a = [x for x in map.squares.values() if x.character == "a"]

    distances_from_a = [
        distances[x.id - start_id, end_square.id - start_id] for x in squares_a
    ]

    return min(distances_from_a)


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
