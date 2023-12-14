# test_point_of_incidence.py

import numpy as np
from pathlib import Path
import pytest
import point_of_incidence as aoc

PUZZLE_DIR = Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc.parse_input(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc.parse_input(puzzle_input)


def test_parse_example1(example1):
    """Test that the data is parsed properly"""
    np.testing.assert_array_equal(
        example1,
        [
            np.array(
                [
                    ["#", ".", "#", "#", ".", ".", "#", "#", "."],
                    [".", ".", "#", ".", "#", "#", ".", "#", "."],
                    ["#", "#", ".", ".", ".", ".", ".", ".", "#"],
                    ["#", "#", ".", ".", ".", ".", ".", ".", "#"],
                    [".", ".", "#", ".", "#", "#", ".", "#", "."],
                    [".", ".", "#", "#", ".", ".", "#", "#", "."],
                    ["#", ".", "#", ".", "#", "#", ".", "#", "."],
                ]
            ),
            np.array(
                [
                    ["#", ".", ".", ".", "#", "#", ".", ".", "#"],
                    ["#", ".", ".", ".", ".", "#", ".", ".", "#"],
                    [".", ".", "#", "#", ".", ".", "#", "#", "#"],
                    ["#", "#", "#", "#", "#", ".", "#", "#", "."],
                    ["#", "#", "#", "#", "#", ".", "#", "#", "."],
                    [".", ".", "#", "#", ".", ".", "#", "#", "#"],
                    ["#", ".", ".", ".", ".", "#", ".", ".", "#"],
                ]
            ),
        ],
    )


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 405


def test_part1_example2(example2):
    """
    Test part 1 on example input
    Taken from https://www.reddit.com/r/adventofcode/comments/18hitog/2023_day_13_easy_additional_examples/
    """

    assert aoc.part1(example2) == 709


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 400


def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc.part2(example2) == 1400
