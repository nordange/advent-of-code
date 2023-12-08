# test_haunted_wasteland.py

from pathlib import Path
import pytest
import haunted_wasteland as aoc

PUZZLE_DIR = Path(__file__).parent


@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc.parse_input(puzzle_input)


@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc.parse_input(puzzle_input)


@pytest.fixture
def example3():
    puzzle_input = (PUZZLE_DIR / "example3.txt").read_text().strip()
    return aoc.parse_input(puzzle_input)


def test_parse_example1(example1):
    """Test that the data is parsed properly"""
    assert example1 == {
        "instructions": "RL",
        "nodes": [
            {"name": "AAA", "left": "BBB", "right": "CCC"},
            {"name": "BBB", "left": "DDD", "right": "EEE"},
            {"name": "CCC", "left": "ZZZ", "right": "GGG"},
            {"name": "DDD", "left": "DDD", "right": "DDD"},
            {"name": "EEE", "left": "EEE", "right": "EEE"},
            {"name": "GGG", "left": "GGG", "right": "GGG"},
            {"name": "ZZZ", "left": "ZZZ", "right": "ZZZ"},
        ],
    }


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 2


def test_parse_example2(example2):
    """Test that the data is parsed properly"""
    assert example2 == {
        "instructions": "LLR",
        "nodes": [
            {"name": "AAA", "left": "BBB", "right": "BBB"},
            {"name": "BBB", "left": "AAA", "right": "ZZZ"},
            {"name": "ZZZ", "left": "ZZZ", "right": "ZZZ"},
        ],
    }


def test_part1_example2(example2):
    """Test part 1 on example input"""
    assert aoc.part1(example2) == 6


def test_parse_example3(example3):
    """Test that the data is parsed properly"""
    assert example3 == {
        "instructions": "LR",
        "nodes": [
            {"name": "11A", "left": "11B", "right": "XXX"},
            {"name": "11B", "left": "XXX", "right": "11Z"},
            {"name": "11Z", "left": "11B", "right": "XXX"},
            {"name": "22A", "left": "22B", "right": "XXX"},
            {"name": "22B", "left": "22C", "right": "22C"},
            {"name": "22C", "left": "22Z", "right": "22Z"},
            {"name": "22Z", "left": "22B", "right": "22B"},
            {"name": "XXX", "left": "XXX", "right": "XXX"},
        ],
    }


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 2


def test_part2_example2(example2):
    """Test part 2 on example input"""
    assert aoc.part2(example2) == 6


def test_part2_example3(example3):
    """Test part 2 on example input"""
    assert aoc.part2(example3) == 6
