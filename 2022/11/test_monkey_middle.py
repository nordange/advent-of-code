# test_monkey_middle.py

from pathlib import Path
import pytest
import monkey_middle as aoc

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

    assert len(example1.monkeys) == 4

    assert example1.monkeys[0].items == [79, 98]
    assert example1.monkeys[1].operation == ["old", "+", "6"]
    assert example1.monkeys[2].test_recipe[-1] == "13"
    assert example1.monkeys[3].next_monkey_true == 0
    assert example1.monkeys[3].next_monkey_false == 1


def test_part2_example1(example1):
    """Test part 2 on example input"""

    assert aoc.part2(example1) == 2713310158
