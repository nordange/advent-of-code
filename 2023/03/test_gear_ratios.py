# test_gear_ratios.py

from pathlib import Path
import pytest
import gear_ratios as aoc

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
        "............",
        ".467..114...",
        "....*.......",
        "...35..633..",
        ".......#....",
        ".617*.......",
        "......+.58..",
        "...592......",
        ".......755..",
        "....$.*.....",
        "..664.598...",
        "............",
    ]


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 4361


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 467835
