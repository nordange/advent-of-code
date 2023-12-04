# test_scratchcards.py

from pathlib import Path
import pytest
import scratchcards as aoc

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
        1: {
            "winning_numbers": [41, 48, 83, 86, 17],
            "own_numbers": [83, 86, 6, 31, 17, 9, 48, 53],
        },
        2: {
            "winning_numbers": [13, 32, 20, 16, 61],
            "own_numbers": [61, 30, 68, 82, 17, 32, 24, 19],
        },
        3: {
            "winning_numbers": [1, 21, 53, 59, 44],
            "own_numbers": [69, 82, 63, 72, 16, 21, 14, 1],
        },
        4: {
            "winning_numbers": [41, 92, 73, 84, 69],
            "own_numbers": [59, 84, 76, 51, 58, 5, 54, 83],
        },
        5: {
            "winning_numbers": [87, 83, 26, 28, 32],
            "own_numbers": [88, 30, 70, 12, 93, 22, 82, 36],
        },
        6: {
            "winning_numbers": [31, 18, 13, 56, 72],
            "own_numbers": [74, 77, 10, 23, 35, 67, 36, 11],
        },
    }


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 13


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 30
