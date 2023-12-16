# test_parabolic_reflector_dish.py

import numpy as np
from pathlib import Path
import pytest
import parabolic_reflector_dish as aoc

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
                ["O", ".", ".", ".", ".", "#", ".", ".", ".", "."],
                ["O", ".", "O", "O", "#", ".", ".", ".", ".", "#"],
                [".", ".", ".", ".", ".", "#", "#", ".", ".", "."],
                ["O", "O", ".", "#", "O", ".", ".", ".", ".", "O"],
                [".", "O", ".", ".", ".", ".", ".", "O", "#", "."],
                ["O", ".", "#", ".", ".", "O", ".", "#", ".", "#"],
                [".", ".", "O", ".", ".", "#", "O", ".", ".", "O"],
                [".", ".", ".", ".", ".", ".", ".", "O", ".", "."],
                ["#", ".", ".", ".", ".", "#", "#", "#", ".", "."],
                ["#", "O", "O", ".", ".", "#", ".", ".", ".", "."],
            ]
        ),
    )


def test_part1_tilt_platform_north_example1(example1):
    tilted = aoc.tilt_platform_north(example1)

    np.testing.assert_array_equal(
        tilted,
        np.array(
            [
                ["O", "O", "O", "O", ".", "#", ".", "O", ".", "."],
                ["O", "O", ".", ".", "#", ".", ".", ".", ".", "#"],
                ["O", "O", ".", ".", "O", "#", "#", ".", ".", "O"],
                ["O", ".", ".", "#", ".", "O", "O", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", ".", "#", "."],
                [".", ".", "#", ".", ".", ".", ".", "#", ".", "#"],
                [".", ".", "O", ".", ".", "#", ".", "O", ".", "O"],
                [".", ".", "O", ".", ".", ".", ".", ".", ".", "."],
                ["#", ".", ".", ".", ".", "#", "#", "#", ".", "."],
                ["#", ".", ".", ".", ".", "#", ".", ".", ".", "."],
            ],
            dtype=str,
        ),
    )


def test_part2_cycle_platform_1_cycle(example1):
    cycled = aoc.cycle_platform(example1, 1)

    np.testing.assert_array_equal(
        cycled,
        np.array(
            [
                [".", ".", ".", ".", ".", "#", ".", ".", ".", "."],
                [".", ".", ".", ".", "#", ".", ".", ".", "O", "#"],
                [".", ".", ".", "O", "O", "#", "#", ".", ".", "."],
                [".", "O", "O", "#", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", "O", "O", "O", "#", "."],
                [".", "O", "#", ".", ".", ".", "O", "#", ".", "#"],
                [".", ".", ".", ".", "O", "#", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", "O", "O", "O", "O"],
                ["#", ".", ".", ".", "O", "#", "#", "#", ".", "."],
                ["#", ".", ".", "O", "O", "#", ".", ".", ".", "."],
            ]
        ),
    )


def test_part2_cycle_platform_3_cycles(example1):
    cycled = aoc.cycle_platform(example1, 3)

    np.testing.assert_array_equal(
        cycled,
        np.array(
            [
                [".", ".", ".", ".", ".", "#", ".", ".", ".", "."],
                [".", ".", ".", ".", "#", ".", ".", ".", "O", "#"],
                [".", ".", ".", ".", ".", "#", "#", ".", ".", "."],
                [".", ".", "O", "#", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", "O", "O", "O", "#", "."],
                [".", "O", "#", ".", ".", ".", "O", "#", ".", "#"],
                [".", ".", ".", ".", "O", "#", ".", ".", ".", "O"],
                [".", ".", ".", ".", ".", ".", ".", "O", "O", "O"],
                ["#", ".", ".", ".", "O", "#", "#", "#", ".", "O"],
                ["#", ".", "O", "O", "O", "#", ".", ".", ".", "O"],
            ]
        ),
    )


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 136


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 64
