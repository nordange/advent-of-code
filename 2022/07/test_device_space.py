# test_device_space.py

from pathlib import Path
import pytest
import device_space as aoc

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

    assert example1.get_structure() == [
        "- / (dir)",
        "  - a (dir)",
        "    - e (dir)",
        "      - i (file, size=584)",
        "    - f (file, size=29116)",
        "    - g (file, size=2557)",
        "    - h.lst (file, size=62596)",
        "  - b.txt (file, size=14848514)",
        "  - c.dat (file, size=8504156)",
        "  - d (dir)",
        "    - j (file, size=4060174)",
        "    - d.log (file, size=8033020)",
        "    - d.ext (file, size=5626152)",
        "    - k (file, size=7214296)",
    ]


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 95437


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 24933642
