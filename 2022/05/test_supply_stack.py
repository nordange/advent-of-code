# test_supply_stack.py

from pathlib import Path
import pytest
import supply_stack as aoc

PUZZLE_DIR = Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text()
    return aoc.parse(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text()
    return aoc.parse(puzzle_input)


def test_parse_example1(example1):
    """Test that the data is parsed properly"""

    stacks, instructions = example1
    assert stacks == {1: ["Z", "N"], 2: ["M", "C", "D"], 3: ["P"]}
    assert instructions == [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)]


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == "CMZ"


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == "MCD"
