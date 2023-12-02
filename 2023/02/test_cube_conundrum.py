# test_cube_conundrum.py

from pathlib import Path
import pytest
import cube_conundrum as aoc

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
    assert example1 == {
        1: [{"blue": 3, "red": 4}, {"red": 1, "green": 2, "blue": 6}, {"green": 2}],
        2: [
            {"blue": 1, "green": 2},
            {"red": 1, "green": 3, "blue": 4},
            {"green": 1, "blue": 1},
        ],
        3: [
            {"blue": 6, "red": 20, "green": 8},
            {"red": 4, "blue": 5, "green": 13},
            {"green": 5, "red": 1},
        ],
        4: [
            {"blue": 6, "red": 3, "green": 1},
            {"red": 6, "green": 3},
            {"green": 3, "blue": 15, "red": 14},
        ],
        5: [{"blue": 1, "red": 6, "green": 3}, {"red": 1, "green": 2, "blue": 2}],
    }


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 8


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 2286
