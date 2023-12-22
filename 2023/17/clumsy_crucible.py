# clumsy_crucible.py

from enum import Enum
import heapq
import numpy as np
import parse
from pathlib import Path
import sys
import time
from tqdm import tqdm


class Direction(Enum):
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4


MOVES = {
    Direction.NORTH: (-1, 0),
    Direction.SOUTH: (1, 0),
    Direction.WEST: (0, -1),
    Direction.EAST: (0, 1),
}

IN_OUT_DIR = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
    Direction.EAST: Direction.WEST,
}


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = []
    for line in puzzle_input.split("\n"):
        parsed_line = [int(x["character"]) for x in parse.findall("{character}", line)]
        parsed_input.append(parsed_line)

    return np.array(parsed_input)


class Grid2D:
    def __init__(self, values, part):
        self.num_rows, self.num_cols = values.shape

        self.values = values

        if part == "part1":
            self.nodes = self.generate_nodes_part1(values)
            self.node_ids = {val: key for key, val in self.nodes.items()}
            self.graph = self.generate_graph_part1()

        elif part == "part2":
            self.nodes = self.generate_nodes_part2(values)
            self.node_ids = {val: key for key, val in self.nodes.items()}
            self.graph = self.generate_graph_part2()

    def generate_nodes_part1(self, values):
        """
        Generates all nodes to accomodate movement restriction
        """
        nodes = {}

        # Add special case for starting node.
        nodes[0] = (
            (0, 0),
            None,
            0,
            values[0, 0],
        )

        for moves in [1, 2, 3]:
            nodes[moves] = (
                (0, 0),
                Direction.EAST,
                moves,
                values[0, 0],
            )

        for moves in [1, 2, 3]:
            nodes[3 + moves] = (
                (0, 0),
                Direction.SOUTH,
                moves,
                values[0, 0],
            )

        node_id = len(nodes)

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if (row, col) == (0, 0):
                    continue
                for incoming in Direction:
                    for num_moves in [1, 2, 3]:
                        nodes[node_id] = (
                            (row, col),
                            incoming,
                            num_moves,
                            values[row, col],
                        )

                        node_id += 1

        return nodes

    def generate_graph_part1(self):
        """
        Generate adjacency list
        """

        graph = {}

        for node_id, ((row, col), incoming, num_moves, value) in self.nodes.items():
            graph[node_id] = []

            if (row, col) == (0, 0):
                graph[node_id].append(
                    self.node_ids[
                        (
                            (0, 1),
                            Direction.WEST,
                            1,
                            self.values[0, 1],
                        )
                    ]
                )
                graph[node_id].append(
                    self.node_ids[
                        (
                            (1, 0),
                            Direction.NORTH,
                            1,
                            self.values[1, 0],
                        )
                    ]
                )
                continue

            # Checking all outgoing directions
            for direction in Direction:
                next_move = MOVES[direction]
                next_row, next_col = row + next_move[0], col + next_move[1]

                if (
                    (0 <= next_row < self.num_rows)
                    and (0 <= next_col < self.num_cols)
                    and direction != incoming
                ):
                    if direction == IN_OUT_DIR[incoming] and num_moves < 3:
                        graph[node_id].append(
                            (
                                self.node_ids[
                                    (
                                        (next_row, next_col),
                                        incoming,
                                        num_moves + 1,
                                        self.values[next_row, next_col],
                                    )
                                ]
                            )
                        )

                    elif direction != IN_OUT_DIR[incoming]:
                        graph[node_id].append(
                            (
                                (
                                    self.node_ids[
                                        (
                                            (next_row, next_col),
                                            IN_OUT_DIR[direction],
                                            1,
                                            self.values[next_row, next_col],
                                        )
                                    ]
                                )
                            )
                        )

        return graph

    def generate_nodes_part2(self, values):
        """
        Generates all nodes to accomodate movement restriction
        """
        nodes = {}

        # Add special case for starting node.
        nodes[0] = (
            (0, 0),
            None,
            0,
            values[0, 0],
        )

        for moves in range(1, 11):
            nodes[moves] = (
                (0, 0),
                Direction.EAST,
                moves,
                values[0, 0],
            )

        for moves in range(1, 11):
            nodes[10 + moves] = (
                (0, 0),
                Direction.SOUTH,
                moves,
                values[0, 0],
            )

        node_id = len(nodes)

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if (row, col) == (0, 0):
                    continue
                for incoming in Direction:
                    for num_moves in range(1, 11):
                        nodes[node_id] = (
                            (row, col),
                            incoming,
                            num_moves,
                            values[row, col],
                        )

                        node_id += 1

        return nodes

    def generate_graph_part2(self):
        """
        Generate adjacency list
        """

        graph = {}

        for node_id, ((row, col), incoming, num_moves, value) in self.nodes.items():
            graph[node_id] = []

            if (row, col) == (0, 0):
                graph[node_id].append(
                    self.node_ids[
                        (
                            (0, 1),
                            Direction.WEST,
                            1,
                            self.values[0, 1],
                        )
                    ]
                )
                graph[node_id].append(
                    self.node_ids[
                        (
                            (1, 0),
                            Direction.NORTH,
                            1,
                            self.values[1, 0],
                        )
                    ]
                )
                continue

            # Checking all outgoing directions
            for direction in Direction:
                next_move = MOVES[direction]
                next_row, next_col = row + next_move[0], col + next_move[1]

                if (
                    (0 <= next_row < self.num_rows)
                    and (0 <= next_col < self.num_cols)
                    and direction != incoming
                ):
                    if direction == IN_OUT_DIR[incoming] and num_moves < 10:
                        graph[node_id].append(
                            (
                                self.node_ids[
                                    (
                                        (next_row, next_col),
                                        incoming,
                                        num_moves + 1,
                                        self.values[next_row, next_col],
                                    )
                                ]
                            )
                        )

                    elif direction != IN_OUT_DIR[incoming] and num_moves >= 4:
                        graph[node_id].append(
                            (
                                (
                                    self.node_ids[
                                        (
                                            (next_row, next_col),
                                            IN_OUT_DIR[direction],
                                            1,
                                            self.values[next_row, next_col],
                                        )
                                    ]
                                )
                            )
                        )

        return graph

    def naive_djikstras(self, root):
        """
        Complexity O(N^2)

        Inspired by https://pythonalgos.com/2022/08/17/dijkstras-algorithm-in-5-steps-with-python/
        """

        num_nodes = len(self.graph)

        # Initialize distances
        dist = np.ones(num_nodes) * np.infty
        dist[root] = 0

        # Initialize visited array
        visited = np.zeros(num_nodes, dtype=bool)

        # Initialize previous node tracker
        previous_node = {}

        # Loop through all nodes
        for _ in tqdm(range(num_nodes)):
            u = -1  # start node as -1

            # Loop through all nodes to check for visitation status
            for curr_node_id in range(num_nodes):
                # If node curr_node_id has not been visited and is not processed
                # or the distance we have to it is less than the distance to the
                # start node
                if not visited[curr_node_id] and (
                    u == -1 or dist[curr_node_id] < dist[u]
                ):
                    u = curr_node_id

            # All the nodes have been visited or we cannot reach this node
            if dist[u] == np.infty:
                break

            # Set the node as visited
            visited[u] = True

            # Compare the distance to each node from the start node to the
            # currently stored distance

            for neighbour in self.graph[u]:
                value = self.nodes[neighbour][-1]

                if dist[u] + value < dist[neighbour]:
                    dist[neighbour] = dist[u] + value
                    previous_node[neighbour] = u

        return dist, previous_node

    def djikstras(self, root):
        """
        Complexity O(N*log N)

        Inspired by https://pythonalgos.com/2022/08/17/dijkstras-algorithm-in-5-steps-with-python/
        """

        num_nodes = len(self.graph)

        # Initialize distances
        dist = np.ones(num_nodes) * np.infty
        dist[root] = 0

        # Initialize visited array
        visited = np.zeros(num_nodes, dtype=bool)

        # Initialize previous node tracker
        previous_node = {}

        # Set up priority queue
        pq = [(0, root)]

        # Process nodes as long as needed
        while len(pq) > 0:
            # Get the root, discard the distance
            _, u = heapq.heappop(pq)

            if visited[u]:
                continue

            visited[u] = True

            # Compare the distance to each node from the start node to the
            # currently stored distance

            for neighbour in self.graph[u]:
                value = self.nodes[neighbour][-1]

                if dist[u] + value < dist[neighbour]:
                    dist[neighbour] = dist[u] + value
                    previous_node[neighbour] = u

                    heapq.heappush(pq, (dist[neighbour], neighbour))

        return dist, previous_node

    def get_coord_nodes(self, coord):
        coord_nodes = [
            node_id for node_id, node in self.nodes.items() if node[0] == coord
        ]

        return coord_nodes

    def backtrack_nodes(self, previous_node, start_node, end_node):
        curr_node = end_node

        while curr_node != start_node:
            print(f"{curr_node} : {self.nodes[curr_node][0]}")
            curr_node = previous_node[curr_node]


def part1(data):
    """Solve part 1"""

    # Each grid point is represented as follows: (coordinate, incoming_direction, num_consequtive_moves)
    # Grid2D class with all tiles
    # - number tiles consequtively
    # End node example1: ((12, 12), <Direction.WEST: 2>, 1, 3)

    grid = Grid2D(data, part="part1")

    start = time.time()
    # dist, previous_node = grid.naive_djikstras(0)
    dist, previous_node = grid.djikstras(0)
    print(f"Elapsed time: {(time.time() - start):.1f} seconds")

    coord_nodes = grid.get_coord_nodes((grid.num_rows - 1, grid.num_cols - 1))

    min_loss = min(dist[coord_nodes])

    return int(min_loss)


def part2(data):
    """Solve part 2"""

    # End node example 1: 6708 : ((12, 12), <Direction.NORTH: 1>, 8, 3)
    # End node example 2: 2354 : 2354 ((4, 11), <Direction.WEST: 2>, 4, 1)

    grid = Grid2D(data, part="part2")

    start = time.time()
    # dist, previous_node = grid.naive_djikstras(0)
    dist, previous_node = grid.djikstras(0)
    print(f"Elapsed time: {(time.time() - start):.1f} seconds")

    coord_nodes = [
        node
        for node in grid.get_coord_nodes((grid.num_rows - 1, grid.num_cols - 1))
        if grid.nodes[node][2] >= 4
    ]

    min_loss = min(dist[coord_nodes])

    return int(min_loss)


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
