# test_aplenty.py

from pathlib import Path
import pytest
import aplenty as aoc

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

    expected = {
        "workflows": {
            "px": [
                {"cat": "a", "op": "<", "value": 2006, "next": "qkq"},
                {"cat": "m", "op": ">", "value": 2090, "next": "A"},
                {"next": "rfg"},
            ],
            "pv": [{"cat": "a", "op": ">", "value": 1716, "next": "R"}, {"next": "A"}],
            "lnx": [{"cat": "m", "op": ">", "value": 1548, "next": "A"}, {"next": "A"}],
            "rfg": [
                {"cat": "s", "op": "<", "value": 537, "next": "gd"},
                {"cat": "x", "op": ">", "value": 2440, "next": "R"},
                {"next": "A"},
            ],
            "qs": [
                {"cat": "s", "op": ">", "value": 3448, "next": "A"},
                {"next": "lnx"},
            ],
            "qkq": [
                {"cat": "x", "op": "<", "value": 1416, "next": "A"},
                {"next": "crn"},
            ],
            "crn": [{"cat": "x", "op": ">", "value": 2662, "next": "A"}, {"next": "R"}],
            "in": [
                {"cat": "s", "op": "<", "value": 1351, "next": "px"},
                {"next": "qqz"},
            ],
            "qqz": [
                {"cat": "s", "op": ">", "value": 2770, "next": "qs"},
                {"cat": "m", "op": "<", "value": 1801, "next": "hdj"},
                {"next": "R"},
            ],
            "gd": [{"cat": "a", "op": ">", "value": 3333, "next": "R"}, {"next": "R"}],
            "hdj": [{"cat": "m", "op": ">", "value": 838, "next": "A"}, {"next": "pv"}],
        },
        "parts": [
            {"x": 787, "m": 2655, "a": 1222, "s": 2876},
            {"x": 1679, "m": 44, "a": 2067, "s": 496},
            {"x": 2036, "m": 264, "a": 79, "s": 2244},
            {"x": 2461, "m": 1339, "a": 466, "s": 291},
            {"x": 2127, "m": 1623, "a": 2188, "s": 1013},
        ],
    }

    assert example1 == expected


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 19114


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 167409079868000
