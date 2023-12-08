# camel_cards.py

from collections import Counter
from enum import IntEnum
import parse
from pathlib import Path
import sys


CARDS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

CARDS_JOKERS = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


class CardHandType(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class CardHand:
    def __init__(self, hand: str, bid: int, use_jokers=False):
        self.hand = hand
        self.bid = bid
        self.use_jokers = use_jokers

        self.hand_type = self._determine_hand_type(hand)

    def _determine_hand_type(self, hand):
        if self.use_jokers:
            return self._determine_hand_type_jokers(hand)
        else:
            return self._determine_hand_type_no_jokers(hand)

    def _determine_hand_type_no_jokers(self, hand):
        card_counts = Counter(hand)

        if len(card_counts) == 1:
            return CardHandType.FIVE_OF_A_KIND
        elif len(card_counts) == 2:
            if 4 in card_counts.values():
                return CardHandType.FOUR_OF_A_KIND
            elif 3 in card_counts.values():
                if 2 in card_counts.values():
                    return CardHandType.FULL_HOUSE
                else:
                    return CardHandType.THREE_OF_A_KIND
        elif len(card_counts) == 3:
            if 3 in card_counts.values():
                return CardHandType.THREE_OF_A_KIND
            elif 2 in card_counts.values():
                if len(card_counts) == 3:
                    return CardHandType.TWO_PAIRS
                elif len(card_counts) == 4:
                    return CardHandType.ONE_PAIR
        elif len(card_counts) == 4:
            return CardHandType.ONE_PAIR
        else:
            return CardHandType.HIGH_CARD

    def _determine_hand_type_jokers(self, hand):
        card_counts = Counter(hand)

        if "J" in card_counts.keys():
            if card_counts["J"] == 5:  # All jokers
                return CardHandType.FIVE_OF_A_KIND

            candidate_cards = [card for card in card_counts.keys() if card != "J"]
            candidates = []

            for card in candidate_cards:
                joker_hand = hand.replace(card, "J")
                candidates.append(self._determine_hand_type_no_jokers(joker_hand))

            best_type = sorted(candidates, reverse=True)[0]

            return best_type

        else:
            return self._determine_hand_type_no_jokers(hand)

    def __repr__(self):
        return f"{self.hand} ({self.hand_type.name}): bid {self.bid}"

    def __eq__(self, other):
        return (self.hand == other.hand) and (self.bid == other.bid)

    def __lt__(self, other):
        if self.hand_type == other.hand_type:
            for my_card, their_card in zip(self.hand, other.hand):
                if self.use_jokers:
                    if CARDS_JOKERS[my_card] != CARDS_JOKERS[their_card]:
                        return CARDS_JOKERS[my_card] < CARDS_JOKERS[their_card]
                else:
                    if CARDS[my_card] != CARDS[their_card]:
                        return CARDS[my_card] < CARDS[their_card]
            return False  # Equal
        else:
            return self.hand_type < other.hand_type

    def __gt__(self, other):
        if self.hand_type == other.hand_type:
            for my_card, their_card in zip(self.hand, other.hand):
                if self.use_jokers:
                    if CARDS_JOKERS[my_card] != CARDS_JOKERS[their_card]:
                        return CARDS_JOKERS[my_card] > CARDS_JOKERS[their_card]

                else:
                    if CARDS[my_card] != CARDS[their_card]:
                        return CARDS[my_card] > CARDS[their_card]
            return False  # Equal
        else:
            return self.hand_type < other.hand_type


def parse_input(puzzle_input):
    """Parse input"""

    hands = []

    for line in puzzle_input.split("\n"):
        match = parse.search("{hand} {bid:d}", line)
        hand = match["hand"]
        bid = match["bid"]

        hands.append({"hand": hand, "bid": bid})

    return hands


def create_hands(data, use_jokers=False):
    hands = []
    for hand in data:
        hands.append(CardHand(hand["hand"], hand["bid"], use_jokers=use_jokers))

    return hands


def part1(data):
    """
    Solve part 1

    What are the total winnings? Each hand: bid amount multiplied by rank
    """

    ranked_hands = sorted(create_hands(data), reverse=True)

    winnings = sum(
        [
            rank * hand.bid
            for (rank, hand) in zip(range(len(ranked_hands), 0, -1), ranked_hands)
        ]
    )

    return winnings


def part2(data):
    """
    Solve part 2

    Use jokers
    """

    hands = create_hands(data, use_jokers=True)
    ranked_hands = sorted(hands, reverse=True)

    winnings = sum(
        [
            rank * hand.bid
            for (rank, hand) in zip(range(len(ranked_hands), 0, -1), ranked_hands)
        ]
    )

    return winnings


def solve(puzzle_input):
    """Solve the entire puzzle for the given input"""
    data = parse_input(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = Path(path).read_text().strip()

        solutions = solve(puzzle_input)

        print("\n".join(str(solution) for solution in solutions))
