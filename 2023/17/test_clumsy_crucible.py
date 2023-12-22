# test_clumsy_crucible.py

import numpy as np
from pathlib import Path
import pytest
import clumsy_crucible as aoc

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
        np.array(
            [
                [2, 4, 1, 3, 4, 3, 2, 3, 1, 1, 3, 2, 3],
                [3, 2, 1, 5, 4, 5, 3, 5, 3, 5, 6, 2, 3],
                [3, 2, 5, 5, 2, 4, 5, 6, 5, 4, 2, 5, 4],
                [3, 4, 4, 6, 5, 8, 5, 8, 4, 5, 4, 5, 2],
                [4, 5, 4, 6, 6, 5, 7, 8, 6, 7, 5, 3, 6],
                [1, 4, 3, 8, 5, 9, 8, 7, 9, 8, 4, 5, 4],
                [4, 4, 5, 7, 8, 7, 6, 9, 8, 7, 7, 6, 6],
                [3, 6, 3, 7, 8, 7, 7, 9, 7, 9, 6, 5, 3],
                [4, 6, 5, 4, 9, 6, 7, 9, 8, 6, 8, 8, 7],
                [4, 5, 6, 4, 6, 7, 9, 9, 8, 6, 4, 5, 3],
                [1, 2, 2, 4, 6, 8, 6, 8, 6, 5, 5, 6, 3],
                [2, 5, 4, 6, 5, 4, 8, 8, 8, 7, 7, 3, 5],
                [4, 3, 2, 2, 6, 7, 4, 6, 5, 5, 5, 3, 3],
            ]
        ),
    )


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 102


def test_parse_example2(example2):
    """Test that the data is parsed properly"""
    np.testing.assert_array_equal(
        example2,
        np.array(
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1],
            ]
        ),
    )


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 94


def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc.part2(example2) == 71
