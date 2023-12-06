# test_boat_race.py

from pathlib import Path
import pytest
import boat_race as aoc

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
        {"duration": 7, "distance": 9},
        {"duration": 15, "distance": 40},
        {"duration": 30, "distance": 200},
    ]


@pytest.mark.parametrize("race_id, result", [(0, 4), (1, 8), (2, 9)])
def test_part1_example1_ways_to_win(example1, race_id, result):
    curr_data = example1[race_id]

    assert aoc.ways_to_win(curr_data["duration"], curr_data["distance"]) == result


def test_part1_example1(example1):
    """Test part 1 on example input"""

    assert aoc.part1(example1) == 288


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 71503
