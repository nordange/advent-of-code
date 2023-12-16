# test_lens_library.py

from pathlib import Path
import pytest
import lens_library as aoc

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
        "rn=1",
        "cm-",
        "qp=3",
        "cm=2",
        "qp-",
        "pc=4",
        "ot=9",
        "ab=5",
        "pc-",
        "pc=6",
        "ot=7",
    ]


def test_hash_algorithm():
    assert aoc.hash_algorithm("HASH") == 52


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 1320


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 145
