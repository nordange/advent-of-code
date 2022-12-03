# aoc_template.py

from pathlib import Path
import sys

def parse(puzzle_input):
    """ Parse input """
    
    calories = []
    curr_calories = []
    for line in puzzle_input.split("\n"):
        if line == '':
            calories.append(curr_calories)
            curr_calories = []
        else:
            curr_calories.append(int(line))
    
    if len(curr_calories) > 0:
        calories.append(curr_calories)
    return calories

def part1(data):
    """ Solve part 1 
    Find the how many calories the elf carrying the most calories is carrying.
    Input is nested list of calories of each food each elf is carrying, e.g.
    [ [100, 200, 300],  # Elf 1
      [50, 150], # Elf 2
    ]
    """

    calories_per_elf = []
    for elf_calories in data:
        calories_per_elf.append(sum(elf_calories))

    return max(calories_per_elf)

def part2(data):
    """ Solve part 2 
    Find the sum of calories for the top three elves
    """
    
    calories_per_elf = []
    for elf_calories in data:
        calories_per_elf.append(sum(elf_calories))

    return sum(sorted(calories_per_elf, reverse=True)[:3])


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

        