# haunted_wasteland.py

from math import gcd
import numpy as np
import parse
from pathlib import Path
import sys


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = {}

    lines = puzzle_input.split("\n")

    parsed_input["instructions"] = lines[0]
    parsed_input["nodes"] = []

    for line in lines[2:]:
        match = parse.search("{name} = ({left}, {right})", line)
        parsed_input["nodes"].append(
            {"name": match["name"], "left": match["left"], "right": match["right"]}
        )

    return parsed_input


class Tree:
    def __init__(self, nodes):
        self.nodes = {
            x["name"]: {"left": x["left"], "right": x["right"]} for x in nodes
        }

    def get_left_for_node(self, node_name):
        return self.nodes[node_name]["left"]

    def get_right_for_node(self, node_name):
        return self.nodes[node_name]["right"]


def part1(data, start_node="AAA", end_node="ZZZ"):
    """
    Solve part 1

    Starting at AAA, how many steps are required to reach ZZZ?
    """

    tree = Tree(data["nodes"])

    instructions = list(data["instructions"])

    curr_node = start_node
    steps = 0

    while not curr_node.endswith(end_node):
        instruction = instructions[steps % len(instructions)]

        if instruction == "L":
            next_node = tree.get_left_for_node(curr_node)

        elif instruction == "R":
            next_node = tree.get_right_for_node(curr_node)

        steps += 1
        curr_node = next_node

    return steps


def part2(data):
    """
    Solve part 2

    Start at every node that ends with A and follow all of the paths at the same time
    until they all simultaneously end up at nodes that end with Z.

    How many steps does it take before you're only on nodes that end with Z?

    """

    tree = Tree(data["nodes"])

    start_nodes = [
        node_name for node_name in tree.nodes.keys() if node_name.endswith("A")
    ]

    min_steps_per_node = []
    for start_node in start_nodes:
        min_steps_per_node.append(part1(data, start_node, "Z"))

    min_steps_overall = np.prod(
        np.array(min_steps_per_node) // gcd(*min_steps_per_node)
    ) * gcd(*min_steps_per_node)

    return min_steps_overall


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
