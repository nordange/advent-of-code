# test_soil_fertilizer.py

from pathlib import Path
import pytest
import soil_fertilizer as aoc

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
        "seeds": [79, 14, 55, 13],
        "seed-to-soil": [[50, 98, 2], [52, 50, 48]],
        "soil-to-fertilizer": [[0, 15, 37], [37, 52, 2], [39, 0, 15]],
        "fertilizer-to-water": [[49, 53, 8], [0, 11, 42], [42, 0, 7], [57, 7, 4]],
        "water-to-light": [[88, 18, 7], [18, 25, 70]],
        "light-to-temperature": [[45, 77, 23], [81, 45, 19], [68, 64, 13]],
        "temperature-to-humidity": [[0, 69, 1], [1, 0, 69]],
        "humidity-to-location": [[60, 56, 37], [56, 93, 4]],
    }


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 35


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 46
