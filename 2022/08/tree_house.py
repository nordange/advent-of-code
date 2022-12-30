# tree_house.py

import numpy as np
from pathlib import Path
import sys


def parse(puzzle_input):
    """Parse input"""
    puzzle_input_lines = puzzle_input.split("\n")

    all_lines = []
    for line in puzzle_input_lines:
        line_nums = [int(x) for x in line]
        all_lines.append(line_nums)

    return np.array(all_lines, dtype=int)


def get_visible_trees(forest):

    num_rows, num_cols = forest.shape

    # All edge trees are visible
    visible_edge_trees = num_rows * 2 + (num_cols - 2) * 2

    visible_interior_trees = 0
    # Interior trees
    for row in range(1, num_rows - 1):
        for col in range(1, num_cols - 1):
            tree = forest[row, col]
            if (
                (tree > forest[row, :col].max())
                or (tree > forest[row, (col + 1) :].max())
                or (tree > forest[:row, col].max())
                or (tree > forest[(row + 1) :, col].max())
            ):
                visible_interior_trees += 1

    return visible_edge_trees + visible_interior_trees


def get_single_scenic_score(tree, neighbours):
    """
    Calculate single scenic score


    Usage examples
    >>> get_single_scenic_score(5, np.array([3]))
    1
    >>> get_single_scenic_score(5, np.array([5,2]))
    1
    >>> get_single_scenic_score(5, np.array([3,5,3]))
    2
    >>> get_single_scenic_score(5, np.array([1,2]))
    2
    """

    height_diffs = neighbours - tree

    if height_diffs.max() >= 0:
        return (height_diffs >= 0).argmax() + 1
    else:
        return len(height_diffs)


def get_scenic_score(forest):

    num_rows, num_cols = forest.shape

    scenic_scores = np.zeros_like(forest)

    for row in range(1, num_rows - 1):
        for col in range(1, num_cols - 1):
            tree = forest[row, col]

            trees_up = forest[:row, col][::-1]
            trees_down = forest[(row + 1) :, col]
            trees_left = forest[row, :col][::-1]
            trees_right = forest[row, (col + 1) :]

            scenic_up = get_single_scenic_score(tree, trees_up)
            scenic_down = get_single_scenic_score(tree, trees_down)
            scenic_left = get_single_scenic_score(tree, trees_left)
            scenic_right = get_single_scenic_score(tree, trees_right)

            scenic_scores[row, col] = (
                scenic_up * scenic_down * scenic_left * scenic_right
            )

    return scenic_scores.max()


def part1(forest):
    """Solve part 1"""

    return get_visible_trees(forest)


def part2(forest):
    """Solve part 2"""

    return get_scenic_score(forest)


def solve(puzzle_input):
    """Solve the entire puzzle for the given input"""
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
