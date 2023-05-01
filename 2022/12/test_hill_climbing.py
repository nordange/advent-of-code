# test_hill_climbing.py

from pathlib import Path
import pytest
import hill_climbing as aoc

PUZZLE_DIR = Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc.parse(puzzle_input)


def test_parse_example1(example1):
    """Test that the data is parsed properly"""

    assert len(example1.squares) == 40
    assert example1.squares[0, 0].character == "S"
    assert example1.squares[2, 5].character == "E"


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 31


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 29
