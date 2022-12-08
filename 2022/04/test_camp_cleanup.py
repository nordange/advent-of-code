# test_aoc_template.py

from pathlib import Path
import pytest
import camp_cleanup as aoc

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
    assert example1 == [
        [[2, 3, 4], [6, 7, 8]],
        [[2, 3], [4, 5]],
        [[5, 6, 7], [7, 8, 9]],
        [[2, 3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7]],
        [[6], [4, 5, 6]],
        [[2, 3, 4, 5, 6], [4, 5, 6, 7, 8]],
    ]


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 2


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 4
