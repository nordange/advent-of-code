# test_camel_cards.py

from pathlib import Path
import pytest
import camel_cards as aoc
from camel_cards import create_hands, CardHand, CardHandType

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
        {"hand": "32T3K", "bid": 765},
        {"hand": "T55J5", "bid": 684},
        {"hand": "KK677", "bid": 28},
        {"hand": "KTJJT", "bid": 220},
        {"hand": "QQQJA", "bid": 483},
    ]


def test_part1_example1_create_hands(example1):
    assert create_hands(example1) == [
        CardHand("32T3K", 765),
        CardHand("T55J5", 684),
        CardHand("KK677", 28),
        CardHand("KTJJT", 220),
        CardHand("QQQJA", 483),
    ]


@pytest.mark.parametrize(
    "hand_id, hand_type",
    [
        (0, CardHandType.ONE_PAIR),
        (1, CardHandType.THREE_OF_A_KIND),
        (2, CardHandType.TWO_PAIRS),
        (3, CardHandType.TWO_PAIRS),
        (4, CardHandType.THREE_OF_A_KIND),
    ],
)
def test_part1_example1_hand_types(example1, hand_id, hand_type):
    hands = create_hands(example1, use_jokers=False)

    assert hands[hand_id].hand_type == hand_type


def test_part1_example1(example1):
    """Test part 1 on example input"""
    assert aoc.part1(example1) == 6440


@pytest.mark.parametrize(
    "hand_id, hand_type",
    [
        (0, CardHandType.ONE_PAIR),
        (1, CardHandType.FOUR_OF_A_KIND),
        (2, CardHandType.TWO_PAIRS),
        (3, CardHandType.FOUR_OF_A_KIND),
        (4, CardHandType.FOUR_OF_A_KIND),
    ],
)
def test_part2_example1_hand_types(example1, hand_id, hand_type):
    hands = create_hands(example1, use_jokers=True)

    assert hands[hand_id].hand_type == hand_type


def test_part2_example1(example1):
    """Test part 2 on example input"""
    assert aoc.part2(example1) == 5905
