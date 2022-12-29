# device_space.py

from pathlib import Path
import sys


class Node:
    def __init__(self, name, size=0, parent=None):
        self.name = name
        self.children = []
        self.size = int(size)
        self.parent = parent

    def add_child(self, name, size=0):
        self.children.append(Node(name, size, parent=self))

    def move_down(self, name):
        for child in self.children:
            if child.name == name:
                return child

    def get_structure(self, offset=0):
        """Generate text output for structure from this node and below"""

        structure_lines = []

        if self.size == 0:
            node_spec = "(dir)"
        else:
            node_spec = f"(file, size={self.size})"

        structure_lines.append(" " * offset + f"- {self.name} {node_spec}")
        for child in self.children:
            structure_lines.extend(child.get_structure(offset + 2))

        return structure_lines

    def get_size(self):
        """Determine size of this and all children nodes"""

        if len(self.children) > 0:
            return sum([child.get_size() for child in self.children])
        else:
            return self.size


def parse(puzzle_input):
    """Parse input"""

    # Create new nodes after ls
    # Track ls and each cd command
    # Pointer to current node and use cd .. for backtracking

    puzzle_input_lines = puzzle_input.split("\n")

    root_node = None
    curr_parent = None

    for puzzle_input_line in puzzle_input_lines:
        if puzzle_input_line[0] == "$":
            # Command
            curr_command_and_params = puzzle_input_line[1:].strip().split(" ")
            curr_command = curr_command_and_params[0]
            curr_params = curr_command_and_params[1:]

            if curr_command == "cd":
                if root_node is None:
                    curr_node = Node(name=curr_params[0], size=0, parent=curr_parent)
                    root_node = curr_node
                elif curr_params[0] == "..":
                    curr_node = curr_node.parent
                else:
                    curr_node = curr_node.move_down(curr_params[0])

            elif curr_command == "ls":
                # Directory listing to come next
                pass
        else:
            if curr_command == "ls":
                input_params = puzzle_input_line.strip().split(" ")

                if input_params[0] == "dir":
                    curr_node.add_child(name=input_params[1])
                else:
                    curr_node.add_child(name=input_params[1], size=input_params[0])

    return root_node


def get_all_dirs(root_node):

    all_dirs = []

    if len(root_node.children) > 0:
        all_dirs.append(root_node)
        for child in root_node.children:
            all_dirs.extend(get_all_dirs(child))

    return all_dirs


def part1(root_node):
    """Solve part 1"""

    # Find the sum of the directories with size at most 100000

    all_dirs = get_all_dirs(root_node)
    sizes = [curr_dir.get_size() for curr_dir in all_dirs]

    part1_sum = sum(size for size in sizes if size <= 100000)

    return part1_sum


def part2(root_node):
    """Solve part 2"""
    # Delete the smallest directory such that the unused space is at least 30000000

    free_space_desired = 30000000
    space_available = 70000000

    all_dirs = get_all_dirs(root_node)
    sizes = [curr_dir.get_size() for curr_dir in all_dirs]

    unused_space = space_available - root_node.get_size()
    free_space_missing = free_space_desired - unused_space

    part2_dir_size = min(size for size in sizes if size >= free_space_missing)

    return part2_dir_size


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
