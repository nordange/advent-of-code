# test_rope_bridge.py

from pathlib import Path
import pytest
import rope_bridge as aoc

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
    assert example1 == ["R 4", "U 4", "L 3", "D 1", "R 4", "D 1", "L 5", "R 2"]


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 13


def test_parse_example2(example2):
    """Test that the data is parsed properly"""
    assert example2 == ["R 5", "U 8", "L 8", "D 3", "R 17", "D 10", "L 25", "U 20"]


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 1


def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc.part2(example2) == 36
