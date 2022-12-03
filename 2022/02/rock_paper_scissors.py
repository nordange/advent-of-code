# aoc_template.py

from pathlib import Path
import sys

def parse(puzzle_input):
    """ Parse input """
    return [line.split(" ") for line in puzzle_input.split("\n")]

def map_elf_input(elf_input):
    """
    Map elf A, B, C input to (R)ock, (P)aper (S)cissors    
    """

    mapping = { "A" : "R", "B" : "P", "C" :"S"}

    return mapping[elf_input]

def map_own_input(own_input):
    """
    Map own X, Y, Z input to (R)ock, (P)aper (S)cissors    
    """

    mapping = { "X" : "R", "Y" : "P", "Z" :"S"}

    return mapping[own_input]

def determine_own_input(player1, desired_outcome):
    """
    Determine the required response to player 1 depending on the desired outcome
    X : lose, Y: draw, Z: win

    Usage examples:
    >>> determine_own_input("R", "X")
    'S'
    >>> determine_own_input("R", "Y")
    'R'
    >>> determine_own_input("R", "Z")
    'P'
    >>> determine_own_input("P", "X")
    'R'
    >>> determine_own_input("P", "Y")
    'P'
    >>> determine_own_input("P", "Z")
    'S'
    >>> determine_own_input("S", "X")
    'P'
    >>> determine_own_input("S", "Y")
    'S'
    >>> determine_own_input("S", "Z")
    'R'

    """

    if desired_outcome == "Y":
        return player1
    elif (player1, desired_outcome) in [("R", "X"), ("P", "Z")]:
        return "S"
    elif (player1, desired_outcome) in [("R", "Z"), ("S", "X")]:
        return "P"
    elif (player1, desired_outcome) in [("P", "X"), ("S", "Z")]:
        return "R"


def rock_paper_scissors_winner(player1, player2):
    """
    Determine winner in rock paper scissors game


    Usage examples:
    >>> rock_paper_scissors_winner("R", "R")
    0
    >>> rock_paper_scissors_winner("R", "P")
    2
    >>> rock_paper_scissors_winner("R", "S")
    1
    >>> rock_paper_scissors_winner("P", "R")
    1
    >>> rock_paper_scissors_winner("P", "P")
    0
    >>> rock_paper_scissors_winner("P", "S")
    2
    >>> rock_paper_scissors_winner("S", "R")
    2
    >>> rock_paper_scissors_winner("S", "P")
    1
    >>> rock_paper_scissors_winner("S", "S")
    0
    """

    if player1 == player2:
        return 0 # Draw
    elif (player1, player2) in[("R", "S"), ("P", "R"), ("S", "P")]:
        return 1 # Player 1 wins
    elif (player1, player2) in [("R", "P"), ("P", "S"), ("S", "R")]:
        return 2 # Player 2 wins

def rock_paper_scissors_score(player1, player2):
    """
    Determine score for rock paper scissors game

    Usage examples:
    >>> rock_paper_scissors_score("R", "P")
    8
    >>> rock_paper_scissors_score("P", "R")
    1
    >>> rock_paper_scissors_score("S", "S")
    6
    """

    selection_score_mapping = {"R" : 1, "P" : 2, "S" : 3}
    winner_score_mapping = {0: 3, 1:0, 2:6}
    
    score_selection = selection_score_mapping[player2]
    score_winner = winner_score_mapping[rock_paper_scissors_winner(player1, player2)]

    return score_selection + score_winner


def part1(data):
    """ Solve part 1 """

    game_scores = []
    for player1, player2 in data:
        normed_player1 = map_elf_input(player1)
        normed_player2 = map_own_input(player2)

        game_scores.append(rock_paper_scissors_score(normed_player1, normed_player2))
    
    return sum(game_scores)

def part2(data):
    """ Solve part 2 """

    game_scores = []
    for player1, desired_outcome in data:
        normed_player1 = map_elf_input(player1)
        normed_player2 = determine_own_input(normed_player1, desired_outcome)

        game_scores.append(rock_paper_scissors_score(normed_player1, normed_player2))
    
    return sum(game_scores)


def solve(puzzle_input):
    """ Solve the entire puzzle for the given input """
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = Path(path).read_text().strip()

        solutions = solve(puzzle_input)

        print("\n".join(str(solution) for solution in solutions))

        