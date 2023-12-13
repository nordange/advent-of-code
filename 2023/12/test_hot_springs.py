# test_hot_springs.py

from pathlib import Path
import pytest
import hot_springs as aoc

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
        {"springs": "???.###", "damage_groups": [1, 1, 3]},
        {"springs": ".??..??...?##.", "damage_groups": [1, 1, 3]},
        {"springs": "?#?#?#?#?#?#?#?", "damage_groups": [1, 3, 1, 6]},
        {"springs": "????.#...#...", "damage_groups": [4, 1, 1]},
        {"springs": "????.######..#####.", "damage_groups": [1, 6, 5]},
        {"springs": "?###????????", "damage_groups": [3, 2, 1]},
    ]


@pytest.mark.parametrize(
    "line_id, result", [(0, 1), (1, 4), (2, 1), (3, 1), (4, 4), (5, 10)]
)
def test_generate_possibilities(example1, line_id, result):
    assert (
        aoc.generate_possibilities(
            example1[line_id]["springs"], example1[line_id]["damage_groups"]
        )
        == result
    )


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 21


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 525152
