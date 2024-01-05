# test_pulse_propagation.py

from pathlib import Path
import pytest
import pulse_propagation as aoc

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
        {"name": "broadcaster", "type": "broadcaster", "destinations": ["a", "b", "c"]},
        {"name": "a", "type": "flip-flop", "destinations": ["b"]},
        {"name": "b", "type": "flip-flop", "destinations": ["c"]},
        {"name": "c", "type": "flip-flop", "destinations": ["inv"]},
        {"name": "inv", "type": "conjunction", "destinations": ["a"]},
    ]


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 32000000


def test_parse_example2(example2):
    """Test that the data is parsed properly"""
    assert example2 == [
        {
            "name": "broadcaster",
            "type": "broadcaster",
            "destinations": ["a"],
        },
        {"name": "a", "type": "flip-flop", "destinations": ["inv", "con"]},
        {
            "name": "inv",
            "type": "conjunction",
            "destinations": ["b"],
        },
        {
            "name": "b",
            "type": "flip-flop",
            "destinations": ["con"],
        },
        {"name": "con", "type": "conjunction", "destinations": ["output"]},
    ]


def test_part1_example2(example2):
    """Test part 1 on example input"""
    assert aoc.part1(example2) == 11687500
