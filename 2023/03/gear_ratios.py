# gear_ratios.py

from pathlib import Path
import re
import sys


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = []

    for line in puzzle_input.split("\n"):
        # Add dot character at start and end of line
        parsed_input.append(f".{line}.")

    # Add blank/dotted first and last line with extra width
    blank_line = "." * len(parsed_input[0])
    parsed_input.insert(0, blank_line)
    parsed_input.append(blank_line)

    return parsed_input


def part1(data):
    """
    Solve part 1

    What is the sum of all of the part numbers in the engine schematic?
    """

    valid_numbers = []

    for idx, line in enumerate(data):
        curr_valid_numbers = []
        curr_invalid_numbers = []

        # First and last line will not find anything

        for match in re.finditer(r"\d+", line):
            span_from, span_to = match.span()
            curr_number = int(match.group())
            neighbourhood = (
                data[idx - 1][(span_from - 1) : (span_to + 1)]
                + line[span_from - 1]
                + line[span_to]
                + data[idx + 1][(span_from - 1) : (span_to + 1)]
            ).replace(".", "")

            if len(neighbourhood) > 0:
                curr_valid_numbers.append(curr_number)
            else:
                curr_invalid_numbers.append(curr_number)

        valid_numbers = valid_numbers + curr_valid_numbers

    return sum(valid_numbers)


def part2(data):
    """
    Solve part 2

    A gear is any * symbol that is adjacent to exactly two part numbers.
    Its gear ratio is the result of multiplying those two numbers together.

    What is the sum of all of the gear ratios in your engine schematic?
    """

    # Search for all '*'
    # Check whether is is adjacent to EXACTLY two part numbers

    gears = []

    numbers_found = {}
    gears_found = {}
    for idx, line in enumerate(data):
        numbers_found[idx] = list(re.finditer(r"\d+", line))
        gears_found[idx] = [match.span()[0] for match in re.finditer(r"\*", line)]

    gear_ratios = []

    for idx, gear_idxs in gears_found.items():
        for gear_idx in gear_idxs:
            curr_parts = []

            # Check adjacent part numbers above
            for part_number_match in numbers_found[idx - 1]:
                span_from, span_to = part_number_match.span()
                curr_part_number = int(part_number_match.group())

                if gear_idx in range(span_from - 1, span_to + 1):
                    curr_parts.append(curr_part_number)

            # Check adjacent part numbers on same line
            for part_number_match in numbers_found[idx]:
                span_from, span_to = part_number_match.span()
                curr_part_number = int(part_number_match.group())

                if gear_idx in [span_from - 1, span_to]:
                    curr_parts.append(curr_part_number)

            # Check adjacent part numbers below
            for part_number_match in numbers_found[idx + 1]:
                span_from, span_to = part_number_match.span()
                curr_part_number = int(part_number_match.group())

                if gear_idx in range(span_from - 1, span_to + 1):
                    curr_parts.append(curr_part_number)

            if len(curr_parts) == 2:
                gear_ratios.append(curr_parts[0] * curr_parts[1])

    return sum(gear_ratios)


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
