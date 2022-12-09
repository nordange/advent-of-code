# supply_stack.py
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
import sys


def parse(puzzle_input):
    """Parse input"""

    line_num_index = None
    puzzle_input_lines = puzzle_input.split("\n")

    for line_num, line in enumerate(puzzle_input_lines):
        if line == "":
            line_num_index = line_num - 1
            break

    # Initial crate configuration
    stack_lines = puzzle_input_lines[:line_num_index]
    line_idxs = puzzle_input_lines[line_num_index]
    stack_idxs = [idx for idx in range(len(line_idxs)) if line_idxs[idx] != " "]

    stacks = defaultdict(list)

    for curr_line in stack_lines[::-1]:
        for stack_idx in stack_idxs:
            if curr_line[stack_idx] != " ":
                stacks[int(line_idxs[stack_idx])].append(curr_line[stack_idx])

    # Rearrangement procedure
    arr_lines = puzzle_input_lines[line_num_index + 2 :]

    instructions = []
    for arr_line in arr_lines:
        if arr_line == "":
            continue
        num_crates = int(arr_line.split(" ")[1])
        from_stack = int(arr_line.split(" ")[3])
        to_stack = int(arr_line.split(" ")[5])

        instructions.append((num_crates, from_stack, to_stack))

    return stacks, instructions


def part1(data):
    """Solve part 1"""
    # What crate ends up on top of each stack after rearrangement?

    stacks, instructions = data

    for instruction in instructions:
        num_crates, from_stack, to_stack = instruction

        for _ in range(num_crates):
            stacks[to_stack].append(stacks[from_stack].pop())

    top_crates = "".join([stacks[stack_key].pop() for stack_key in stacks.keys()])

    return top_crates


def part2(data):
    """Solve part 2"""
    # Crane can pick up and move multiple crates at once

    stacks, instructions = data

    total_num_crates = sum([len(x) for x in stacks.values()])
    stacks
    for instruction in instructions:
        num_crates, from_stack, to_stack = instruction

        stacks[to_stack].extend(stacks[from_stack][-num_crates:])
        stacks[from_stack] = stacks[from_stack][:-num_crates]

    top_crates = ""
    for stack in stacks.values():
        if len(stack) > 0:
            top_crates += stack.pop()
        else:
            top_crates += " "

    return top_crates


def solve(puzzle_input):
    """Solve the entire puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(deepcopy(data))
    solution2 = part2(deepcopy(data))

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = Path(path).read_text()

        solutions = solve(puzzle_input)

        print("\n".join(str(solution) for solution in solutions))
