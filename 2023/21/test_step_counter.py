# test_step_counter.py

import numpy as np
from pathlib import Path
import pytest
import step_counter as aoc

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
    expected_input = {
        "start_coord": (5, 5),
        "garden": np.array(
            [
                [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", "#", "#", "#", ".", "#", "."],
                [".", "#", "#", "#", ".", "#", "#", ".", ".", "#", "."],
                [".", ".", "#", ".", "#", ".", ".", ".", "#", ".", "."],
                [".", ".", ".", ".", "#", ".", "#", ".", ".", ".", "."],
                [".", "#", "#", ".", ".", ".", "#", "#", "#", "#", "."],
                [".", "#", "#", ".", ".", "#", ".", ".", ".", "#", "."],
                [".", ".", ".", ".", ".", ".", ".", "#", "#", ".", "."],
                [".", "#", "#", ".", "#", ".", "#", "#", "#", "#", "."],
                [".", "#", "#", ".", ".", "#", "#", ".", "#", "#", "."],
                [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            ],
            dtype=str,
        ),
    }
    np.testing.assert_array_equal(example1["garden"], expected_input["garden"])
    assert example1["start_coord"] == expected_input["start_coord"]


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1, num_steps=6) == 16


@pytest.mark.skip(reason="Not implemented")
def test_parse_example2(example2):
    """Test that the data is parsed properly"""
    assert example2 == ...


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == ...


@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc.part2(example2) == ...
