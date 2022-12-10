# tuning.py

from pathlib import Path
import sys


def parse(puzzle_input):
    """Parse input"""
    return puzzle_input.strip()


def detect_message(text_string, marker_length):
    """
    Detect marker consisting of first n distinct successive characters

    >>> detect_message("bvwbjplbgvbhsrlpgdmjqwftvncz", 4)
    5

    >>> detect_message("nppdvjthqldpwncqszvftbrmjlhg", 4)
    6

    >>> detect_message("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4)
    10

    >>> detect_message("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4)
    11

    >>> detect_message("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14)
    19

    >>> detect_message("bvwbjplbgvbhsrlpgdmjqwftvncz", 14)
    23

    >>> detect_message("nppdvjthqldpwncqszvftbrmjlhg", 14)
    23

    >>> detect_message("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14)
    29

    >>> detect_message("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14)
    26
    """

    for i in range(0, len(text_string) - marker_length):
        curr_chars = text_string[i : (i + marker_length)]

        if len(curr_chars) == len(set(curr_chars)):
            # Marker found
            return i + marker_length


def part1(data):
    """Solve part 1
    Criterion: First four set of characters with no duplicated characters
    """
    marker_length = 4

    return detect_message(data, marker_length)


def part2(data):
    """Solve part 2"""
    marker_length = 14

    return detect_message(data, marker_length)


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
