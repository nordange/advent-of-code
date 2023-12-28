# lavaduct_lagoon.py

from collections import namedtuple
from itertools import pairwise
import numpy as np
import parse
from pathlib import Path
import regex as re
import sys
from tqdm import tqdm

Point = namedtuple("Point", "y x")
Edge = namedtuple("Edge", "p1 p2")

DIRS = {"L": (0, -1), "R": (0, 1), "U": (-1, 0), "D": (1, 0)}


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = []

    for line in puzzle_input.split("\n"):
        match = parse.search("{direction} {length:d} ({hex_colour})", line)

        parsed_input.append(
            {
                "direction": match["direction"],
                "length": match["length"],
                "colour": match["hex_colour"],
            }
        )

    return parsed_input


def determine_canvas_size(data):
    widths = []
    heights = []
    for entry in data:
        direction, length, _ = entry.values()
        if direction == "R":
            widths.append(length)
        elif direction == "L":
            widths.append(-length)
        elif direction == "U":
            heights.append(-length)
        elif direction == "D":
            heights.append(length)

    rows = max(np.cumsum(heights)) - min(np.cumsum(heights))
    cols = max(np.cumsum(widths)) - min(np.cumsum(widths))

    start_row = abs(np.cumsum(heights).min())
    start_col = abs(np.cumsum(widths).min())

    return rows + 1, cols + 1, (start_row, start_col)


def dig_edge(data, terrain_map, start_coord=(0, 0)):
    curr_row = start_coord[0]
    curr_col = start_coord[1]

    edges = []

    for instruction in data:
        new_move = DIRS[instruction["direction"]]
        new_row = curr_row + new_move[0] * instruction["length"]
        new_col = curr_col + new_move[1] * instruction["length"]

        min_row, max_row = sorted([curr_row, new_row])
        min_col, max_col = sorted([curr_col, new_col])

        terrain_map[min_row : (max_row + 1), min_col : (max_col + 1)] = True

        edges.append(Edge(Point(curr_row, curr_col), Point(new_row, new_col)))

        curr_row, curr_col = new_row, new_col

    return terrain_map, edges


def extract_vertices(data, start_coord=(0, 0)):
    curr_row = start_coord[0]
    curr_col = start_coord[1]

    vertices = [Point(curr_row, curr_col)]

    for instruction in data:
        new_move = DIRS[instruction["direction"]]
        new_row = curr_row + new_move[0] * instruction["length"]
        new_col = curr_col + new_move[1] * instruction["length"]

        vertices.append(Point(new_row, new_col))

        curr_row, curr_col = new_row, new_col

    return vertices


def polygon_area(vertices):
    """
    Applies the Shoelace formula:
     - https://www.theoremoftheday.org/GeometryAndTrigonometry/Shoelace/TotDShoelace.pdf
     - https://www.101computing.net/the-shoelace-algorithm/
    """

    sum1 = 0
    sum2 = 0

    n = len(vertices)

    for i in range(n - 1):
        sum1 += vertices[i].x * vertices[i + 1].y
        sum2 += vertices[i].y * vertices[i + 1].x

    sum1 += vertices[n - 1].x * vertices[0].y
    sum2 += vertices[0].x * vertices[n - 1].y

    area = abs(sum1 - sum2) / 2

    return area


def print_trench(terrain_map, to_file=False):
    prepared_lines = []

    for map_line in terrain_map:
        curr_line = (
            " ".join([str(x) for x in map_line.tolist()])
            .replace("True", "#")
            .replace("False", ".")
        )

        prepared_lines.append(curr_line)

    if to_file:
        with open("trench.txt", "w") as f:
            for line in prepared_lines:
                f.write(line + "\n")
    else:
        for line in prepared_lines:
            print(line)


def check_edge_intersections(edges, point):
    """
    Based on https://web.cs.ucdavis.edu/~okreylos/TAship/Spring2000/PointInPolygon.html
    """

    num_intersections = 0

    for edge in edges:
        if edge.p1.y < point.y and edge.p2.y < point.y:
            continue
        elif edge.p1.y >= point.y and edge.p2.y >= point.y:
            continue
        else:
            # Sx = (Py - y1)*(x2-x1)/(y2-y1) + x1
            Sx = (point.y - edge.p1.y) * (edge.p2.x - edge.p1.x) / (
                edge.p2.y - edge.p1.y
            ) + edge.p1.x
            if Sx > point.x:
                num_intersections += 1

    return num_intersections


def dig_interior(terrain_map, edges):
    interior_map = terrain_map.copy()

    num_rows, num_cols = terrain_map.shape

    # Determine number of intersections
    for row in tqdm(range(num_rows)):
        for col in range(num_cols):
            if not terrain_map[row, col]:
                num_intersections = check_edge_intersections(edges, Point(row, col))

                if (num_intersections % 2) > 0:
                    interior_map[row, col] = True

    return interior_map


def calculate_dugout(data):
    """
    Uses Shoelace formula to get area (zero-width line). The use Pick's theorem (A = i + b/2 -1) to calculate
    the number of interior nodes

    Total number of dugout tiles is boundary nodes + internal nodes

    """

    rows, cols, start_coord = determine_canvas_size(data)

    vertices = extract_vertices(data, start_coord)
    zero_width_area = polygon_area(vertices)

    # Calculate number of boundary nodes (length of boundary/perimeter)
    perimeter = 0
    for p1, p2 in pairwise(vertices):
        perimeter += abs(p1.x - p2.x) + abs(p1.y - p2.y)

    internal_nodes = int(zero_width_area - perimeter / 2 + 1)

    return internal_nodes + perimeter


def convert_hex_instruction(colour_code):
    num_to_dir = {0: "R", 1: "D", 2: "L", 3: "U"}

    num_dir = int(colour_code[-1])
    length = int(colour_code[1:-1], 16)

    return {"direction": num_to_dir[num_dir], "length": length, "colour": colour_code}


def part1(data):
    """Solve part 1"""

    rows, cols, start_coord = determine_canvas_size(data)

    # Naive version
    # terrain_map = np.zeros((rows, cols), dtype=bool)

    # terrain_map, edges = dig_edge(data, terrain_map, start_coord)
    # # print_trench(terrain_map)

    # interior_map = dig_interior(terrain_map, edges)

    # return interior_map.sum()

    # vertices = extract_vertices(data, start_coord)
    # area = polygon_area(vertices)

    area = calculate_dugout(data)

    return area


def part2(data):
    """Solve part 2"""

    new_instructions = []
    for instruction in data:
        new_instructions.append(convert_hex_instruction(instruction["colour"]))

    area = calculate_dugout(new_instructions)

    return area


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
