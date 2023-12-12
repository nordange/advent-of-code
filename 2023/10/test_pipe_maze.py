# test_pipe_maze.py

import numpy as np
from pathlib import Path
import pytest
import pipe_maze as aoc

from pipe_maze import find_start_coordinates, find_start_pipe_type


PUZZLE_DIR = Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc.parse_input(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc.parse_input(puzzle_input)


@pytest.fixture
def example3():
    puzzle_input = (PUZZLE_DIR / "example3.txt").read_text().strip()
    return aoc.parse_input(puzzle_input)


@pytest.fixture
def example4():
    puzzle_input = (PUZZLE_DIR / "example4.txt").read_text().strip()
    return aoc.parse_input(puzzle_input)


@pytest.fixture
def example5():
    puzzle_input = (PUZZLE_DIR / "example5.txt").read_text().strip()
    return aoc.parse_input(puzzle_input)


def test_parse_example1(example1):
    """Test that the data is parsed properly"""

    exp_input = np.array(
        [
            ["-", "L", "|", "F", "7"],
            ["7", "S", "-", "7", "|"],
            ["L", "|", "7", "|", "|"],
            ["-", "L", "-", "J", "|"],
            ["L", "|", "-", "J", "F"],
        ],
        dtype=str,
    )

    np.testing.assert_array_equal(example1, exp_input)


def test_parse_example2(example2):
    """Test that the data is parsed properly"""

    exp_input = np.array(
        [
            ["7", "-", "F", "7", "-"],
            [".", "F", "J", "|", "7"],
            ["S", "J", "L", "L", "7"],
            ["|", "F", "-", "-", "J"],
            ["L", "J", ".", "L", "J"],
        ],
        dtype=str,
    )

    np.testing.assert_array_equal(example2, exp_input)


def test_find_start_coordinates_example1(example1):
    assert find_start_coordinates(example1) == (1, 1)


def test_find_start_coordinates_example2(example2):
    assert find_start_coordinates(example2) == (2, 0)


def test_find_start_pipe_type_example1(example1):
    assert find_start_pipe_type(example1, find_start_coordinates(example1)) == "F"


def test_find_start_pipe_type_example2(example2):
    assert find_start_pipe_type(example2, find_start_coordinates(example2)) == "F"


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 4


def test_part1_example2(example2):
    """Test part 1 on example input"""
    assert aoc.part1(example2) == 8


def test_part2_example3(example3):
    """Test part 2 on example input"""
    assert aoc.part2(example3) == 4


def test_part2_example4(example4):
    """Test part 2 on example input"""
    assert aoc.part2(example4) == 8


def test_part2_example5(example5):
    """Test part 2 on example input"""
    assert aoc.part2(example5) == 10
