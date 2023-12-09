# test_mirage_maintenace.py

from pathlib import Path
import pytest
import mirage_maintenance as aoc

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
    assert example1 == [
        [0, 3, 6, 9, 12, 15],
        [1, 3, 6, 10, 15, 21],
        [10, 13, 16, 21, 30, 45],
    ]


@pytest.mark.parametrize("line_id, predicted_value", [(0, 18), (1, 28), (2, 68)])
def test_part1_example1_single_lines(example1, line_id, predicted_value):
    assert aoc.predict_value(example1[line_id]) == predicted_value


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 114


@pytest.mark.parametrize(
    "line_id, predicted_value_backwards", [(0, -3), (1, 0), (2, 5)]
)
def test_part2_example1_single_lines(example1, line_id, predicted_value_backwards):
    assert aoc.predict_value_backwards(example1[line_id]) == predicted_value_backwards


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 2
