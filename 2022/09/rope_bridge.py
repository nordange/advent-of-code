# rope_bridge.py

from colorama import Cursor
import numpy as np
from pathlib import Path
import sys


def parse(puzzle_input):
    """Parse input"""

    puzzle_input_lines = puzzle_input.split("\n")

    return puzzle_input_lines


def track_head(moves, start_pos):
    """
    Track head movements from given starting position based on instructions

    Parameters
    ----------
    moves : list of strings
        Each string on format: direction (U/D/L/R) distance
    start_pos : tuple
        (x, y)


    >>> track_head(["R 2"], (1,1))
    [(1, 1), (1, 2), (1, 3)]

    >>> track_head(["U 3"], (0,0))
    [(0, 0), (1, 0), (2, 0), (3, 0)]

    >>> track_head(["R 4"], (2,3))
    [(2, 3), (2, 4), (2, 5), (2, 6), (2, 7)]

    >>> track_head(["L 1"], (1,1))
    [(1, 1), (1, 0)]

    >>> track_head(["L 1"], (0, 0))
    [(0, 1), (0, 0)]

    >>> track_head(["D 2", "L 3"], (0, 0))
    [(2, 3), (1, 3), (0, 3), (0, 2), (0, 1), (0, 0)]
    """

    trace = [start_pos]

    curr_pos = start_pos
    for move in moves:
        direction, distance = move.split(" ")

        if direction == "R":
            trace.extend(
                [(curr_pos[0], curr_pos[1] + x) for x in range(1, int(distance) + 1)]
            )
        elif direction == "L":
            trace.extend(
                [(curr_pos[0], curr_pos[1] - x) for x in range(1, int(distance) + 1)]
            )
        elif direction == "D":
            trace.extend(
                [(curr_pos[0] - x, curr_pos[1]) for x in range(1, int(distance) + 1)]
            )
        elif direction == "U":
            trace.extend(
                [(curr_pos[0] + x, curr_pos[1]) for x in range(1, int(distance) + 1)]
            )

        curr_pos = trace[-1]

    # Adjust coordinates
    min_row = min([row for row, col in trace])
    min_col = min([col for row, col in trace])

    if min_row < 0:
        trace = [(row + abs(min_row), col) for row, col in trace]

    if min_col < 0:
        trace = [(row, col + abs(min_col)) for row, col in trace]

    return trace


def is_touching(head_pos, tail_pos):
    """
    Determine if head and tail are touching
    Touching = diagonally adjacent/overlapping/next to each other

    Usage examples:
    >>> is_touching((0, 0), (0, 0))
    True
    >>> is_touching((0, 0), (0, 1))
    True
    >>> is_touching((0, 0), (1, 0))
    True
    >>> is_touching((0, 0), (1, 1))
    True
    >>> is_touching((0, 0), (0, 2))
    False
    >>> is_touching((0, 0), (2, 2))
    False
    """

    # Overlapping
    if head_pos == tail_pos:
        return True

    # Next to each other vertically
    if (abs(head_pos[0] - tail_pos[0]) == 1) and (head_pos[1] == tail_pos[1]):
        return True

    # Next to each other horizontally
    if (head_pos[0] == tail_pos[0]) and (abs(head_pos[1] - tail_pos[1]) == 1):
        return True

    # Diagonally adjacent
    if (abs(head_pos[0] - tail_pos[0]) == 1) and (abs(head_pos[1] - tail_pos[1]) == 1):
        return True

    return False


def track_tail(head_trace):
    """
    Simulate tail movement

    If H is two steps directly up, down, left or right from T, T must also move in
    that direction

    If H and T aren't touching and aren't in the same row or column, T always moves
    one step diagonally to keep up

    Usage examples
    >>> track_tail([(0, 0), (0, 1), (0, 2)])
    [(0, 0), (0, 0), (0, 1)]
    >>> track_tail([(0, 0), (1, 0), (2, 0)])
    [(0, 0), (0, 0), (1, 0)]
    >>> track_tail([(0, 0), (1, 0), (1, 1), (2, 1)])
    [(0, 0), (0, 0), (0, 0), (1, 1)]
    >>> track_tail([(0, 0), (1, 0), (1, 1), (1, 2)])
    [(0, 0), (0, 0), (0, 0), (1, 1)]
    """

    tail_trace = [head_trace[0]]

    for idx in range(1, len(head_trace)):
        curr_head_pos = head_trace[idx]
        prev_head_pos = head_trace[idx - 1]
        tail_pos = tail_trace[-1]

        if not is_touching(curr_head_pos, tail_pos):
            tail_pos = (
                tail_pos[0] + np.sign(curr_head_pos[0] - tail_pos[0]),
                tail_pos[1] + np.sign(curr_head_pos[1] - tail_pos[1]),
            )
        tail_trace.append(tail_pos)

    return tail_trace


def part1(data):
    """Solve part 1"""
    # How many positions does T visit at least once?

    start_pos = (0, 0)

    head_trace = track_head(data, start_pos)

    tail_trace = track_tail(head_trace)

    return len(set(tail_trace))


def draw_status(traces, time_step):
    # For extra debugging
    max_row = max([x[0] for knot_trace in traces for x in knot_trace])
    max_col = max([x[1] for knot_trace in traces for x in knot_trace])

    board = np.ones((max_row + 1, max_col + 1)) * 99

    curr_trace_pos = [x[time_step] for x in traces]

    for idx, pos in enumerate(curr_trace_pos):
        board[max_row - pos[0], pos[1]] = int(min(board[max_row - pos[0], pos[1]], idx))

    for row in board:
        row_str = (
            " ".join([str(x) for x in row])
            .replace("99.0", ".")
            .replace(".0", "")
            .replace("0", "H")
        )
        print(row_str)


def part2(data):
    """Solve part 2"""
    # 10 knots, H and 9 T

    start_pos = (0, 0)
    head_trace = track_head(data, start_pos)

    traces = [head_trace]

    for i in range(9):
        tail_trace = track_tail(head_trace)
        head_trace = tail_trace
        traces.append(tail_trace)

    timesteps = [int(x.split(" ")[1]) for x in data]
    acc_timesteps = list(np.cumsum(timesteps))

    # For extra debugging
    # for x in range(len(traces[0])):
    # for x in acc_timesteps:
    # for x in range(13, 22):
    #     print(f"\nTime {x}")
    #     draw_status(traces, x)

    return len(set(tail_trace))


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
