# lens_library.py

import parse
from pathlib import Path
import sys


def parse_input(puzzle_input):
    """Parse input"""

    return puzzle_input.split(",")


def hash_algorithm(input_txt):
    curr_value = 0
    for character in input_txt:
        curr_value += ord(character)
        curr_value *= 17
        curr_value %= 256

    return curr_value


def part1(data):
    """Solve part 1"""

    hash_steps = []

    for step in data:
        hash_steps.append(hash_algorithm(step))

    return sum(hash_steps)


class Box:
    def __init__(self):
        self.slots = []
        self.focal_lengths = {}

    def update_lens(self, label, focal_length):
        if label not in self.slots:
            self.slots.append(label)

        self.focal_lengths[label] = focal_length

    def remove_lens(self, label):
        if label in self.slots:
            self.slots.remove(label)
            self.focal_lengths.pop(label)

    def __repr__(self):
        contents = " ".join(
            [f"[{label} {self.focal_lengths[label]}]" for label in self.slots]
        )

        return contents


def part2(data):
    """Solve part 2"""

    boxes = []
    for _ in range(256):
        boxes.append(Box())

    for line in data:
        match = parse.search("{label}{operator:W}", line)

        box_id = hash_algorithm(match["label"])

        if match["operator"] == "=":
            focal_length = int(line[-1])
            boxes[box_id].update_lens(match["label"], focal_length)

        elif match["operator"] == "-":
            boxes[box_id].remove_lens(match["label"])

    # Calculate focusing power
    focusing_power = 0
    for box_id, box in enumerate(boxes):
        for slot_id, label in enumerate(box.slots):
            focusing_power += (box_id + 1) * (slot_id + 1) * box.focal_lengths[label]

    return focusing_power


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
