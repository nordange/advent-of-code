# pipe_maze.py

from copy import deepcopy
import numpy as np
from pathlib import Path
import sys

sys.setrecursionlimit(5000)

PIPE_MAZE_READER = {
    "|": {"N": "S"},
    "-": {"E": "W"},
    "L": {"N": "E"},
    "J": {"N": "W"},
    "7": {"S": "W"},
    "F": {"S": "E"},
    ".": {},
}
for key, dirs in PIPE_MAZE_READER.items():
    PIPE_MAZE_READER[key].update({v: k for k, v in dirs.items()})

DIRECTION_FLIPPER = {"N": "S", "S": "N", "W": "E", "E": "W"}


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = []
    for line in puzzle_input.split("\n"):
        parsed_input.append(list(line))

    return np.array(parsed_input, dtype=str)


def find_start_coordinates(map):
    raw_coords = np.where(map == "S")

    return raw_coords[0][0], raw_coords[1][0]


def find_start_pipe_type(data, coords):
    connections = []
    # Check connection going N
    if "S" in PIPE_MAZE_READER[data[coords[0] - 1, coords[1]]].keys():
        connections.append("N")
    # Check connection going E
    if "W" in PIPE_MAZE_READER[data[coords[0], coords[1] + 1]].keys():
        connections.append("E")
    # Check connection going S
    if "N" in PIPE_MAZE_READER[data[coords[0] + 1, coords[1]]].keys():
        connections.append("S")
    # Check connection going W
    if "E" in PIPE_MAZE_READER[data[coords[0], coords[1] - 1]].keys():
        connections.append("W")

    connections = "".join(connections + connections[::-1])
    if "NS" in connections:
        return "|"
    elif "EW" in connections:
        return "-"
    elif "NE" in connections:
        return "L"
    elif "NW" in connections:
        return "J"
    elif "SW" in connections:
        return "7"
    elif "SE" in connections:
        return "F"


def get_next_coords(curr_coords, direction):
    if direction == "N":
        next_coords = (curr_coords[0] - 1, curr_coords[1])
    elif direction == "S":
        next_coords = (curr_coords[0] + 1, curr_coords[1])
    elif direction == "W":
        next_coords = (curr_coords[0], curr_coords[1] - 1)
    elif direction == "E":
        next_coords = (curr_coords[0], curr_coords[1] + 1)

    return next_coords


def identify_pipe_loop(data):
    start_coords = find_start_coordinates(data)
    start_pipe = find_start_pipe_type(data, start_coords)

    curr_coords = start_coords
    curr_direction = list(PIPE_MAZE_READER[start_pipe].keys())[0]

    next_coords = get_next_coords(curr_coords, curr_direction)
    next_direction = PIPE_MAZE_READER[data[next_coords]][
        DIRECTION_FLIPPER[curr_direction]
    ]

    steps = np.ones_like(data, dtype=int) * np.nan

    steps[curr_coords] = 0

    num_steps = 1
    while start_coords != next_coords:
        steps[next_coords] = num_steps

        curr_coords = next_coords
        curr_direction = next_direction

        next_coords = get_next_coords(curr_coords, curr_direction)

        if next_coords != start_coords:
            next_direction = PIPE_MAZE_READER[data[next_coords]][
                DIRECTION_FLIPPER[curr_direction]
            ]

        num_steps += 1

    return steps


def part1(data):
    """
    Solve part 1

    How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?
    """

    loop_distances = identify_pipe_loop(data)

    return int(np.nanmax(loop_distances) + 1) // 2


def print_maze(maze):
    for line in maze:
        print(" ".join(line.tolist()))


def is_safe(grid, row, col, visited):
    return (
        (0 <= row < len(grid))
        and (0 <= col < len(grid[0]))
        and (grid[row][col] != "X")
        and (visited[row][col] == False)
    )


def dfs(row, col, visited, grid):
    valid_row = [-1, 0, 0, 1]
    valid_col = [0, -1, 1, 0]

    visited[row, col] = True

    for neighbour in range(len(valid_row)):
        new_row = row + valid_row[neighbour]
        new_col = col + valid_col[neighbour]

        if is_safe(grid, new_row, new_col, visited):
            dfs(new_row, new_col, visited, grid)

    return visited


def is_enclosed(coords, grid):
    for row, col in zip(coords[0], coords[1]):
        # Combinations flipping inside/outside : |, F-J, L-7 (F-7 and L-J reguire no change)
        intersections = len([x for x in grid[row, (col + 1) :] if x in "|LJ"])
        if (
            (row <= 0)
            or (row == (len(grid) - 1))
            or (col <= 0)
            or (col == (len(grid[0]) - 1))
        ):
            return False

        elif intersections % 2 == 0:
            return False

    return True


def part2(data):
    """Solve part 2"""

    # Use depth-first-search to find all islands
    loop_distances = identify_pipe_loop(data)
    idx_pipe = np.where(loop_distances >= 0)
    idx_notpipe = np.where(np.isnan(loop_distances) == True)

    maze = deepcopy(data)
    maze[idx_pipe] = "X"
    maze[idx_notpipe] = "."

    # Prepare for inside/outside algorithm
    start_coords = find_start_coordinates(data)
    start_pipe = find_start_pipe_type(data, start_coords)

    maze_pipe = deepcopy(data)
    maze_pipe[idx_pipe] = data[idx_pipe]
    maze_pipe[idx_notpipe] = "."
    maze_pipe[start_coords] = start_pipe

    visited = np.zeros_like(maze, dtype=bool)

    while (maze == ".").sum() > 0:
        rows, cols = np.where(maze == ".")
        start_row, start_col = rows[0], cols[0]

        visited = np.zeros_like(maze, dtype=bool)

        island_idx = dfs(start_row, start_col, visited, maze)

        # Inside or outside?
        if is_enclosed(np.where(island_idx == True), maze_pipe):
            maze[island_idx] = "I"
        else:
            maze[island_idx] = "O"

    return (maze == "I").sum()


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
