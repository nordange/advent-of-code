# test_lavaduct_lagoon.py

import numpy as np
from pathlib import Path
import pytest
import lavaduct_lagoon as aoc

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
        {"direction": "R", "length": 6, "colour": "#70c710"},
        {"direction": "D", "length": 5, "colour": "#0dc571"},
        {"direction": "L", "length": 2, "colour": "#5713f0"},
        {"direction": "D", "length": 2, "colour": "#d2c081"},
        {"direction": "R", "length": 2, "colour": "#59c680"},
        {"direction": "D", "length": 2, "colour": "#411b91"},
        {"direction": "L", "length": 5, "colour": "#8ceee2"},
        {"direction": "U", "length": 2, "colour": "#caa173"},
        {"direction": "L", "length": 1, "colour": "#1b58a2"},
        {"direction": "U", "length": 2, "colour": "#caa171"},
        {"direction": "R", "length": 2, "colour": "#7807d2"},
        {"direction": "U", "length": 3, "colour": "#a77fa3"},
        {"direction": "L", "length": 2, "colour": "#015232"},
        {"direction": "U", "length": 2, "colour": "#7a21e3"},
    ]


def test_dig_edge_example1(example1):
    rows, cols, start_coord = aoc.determine_canvas_size(example1)
    terrain_map = np.zeros((rows, cols), dtype=bool)

    terrain_map, edges = aoc.dig_edge(example1, terrain_map, start_coord)

    assert terrain_map.sum() == 38


def test_convert_hex_instruction():
    assert aoc.convert_hex_instruction("#7807d2") == {
        "direction": "L",
        "length": 491645,
        "colour": "#7807d2",
    }
    assert aoc.convert_hex_instruction("#70c710") == {
        "direction": "R",
        "length": 461937,
        "colour": "#70c710",
    }
    assert aoc.convert_hex_instruction("#0dc571") == {
        "direction": "D",
        "length": 56407,
        "colour": "#0dc571",
    }
    assert aoc.convert_hex_instruction("#caa173") == {
        "direction": "U",
        "length": 829975,
        "colour": "#caa173",
    }


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 62


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 952408144115
