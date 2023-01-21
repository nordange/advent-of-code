# monkey_middle.py
from copy import deepcopy
import numpy as np
from pathlib import Path
import sys


class Monkey:
    def __init__(self, text_lines: list):

        parsed_data = self._parse(text_lines)
        self.monkey_id = parsed_data["monkey_id"]
        self.items = parsed_data["items"]
        self.operation = parsed_data["operation"]
        self.test_recipe = parsed_data["test"]

        self.next_monkey_true = parsed_data["next_monkey_true"]
        self.next_monkey_false = parsed_data["next_monkey_false"]

        self.num_inspections = 0

    def _parse(self, text_lines: list):
        for curr_line in text_lines.split("\n"):
            if curr_line.split(" ")[0] == "Monkey":
                monkey_id = int(curr_line.split(" ")[1][:-1])
            elif "Starting items" in curr_line:
                items = [
                    int(item)
                    for item in curr_line.lstrip("Starting items:").split(", ")
                ]
            elif "Operation" in curr_line:
                operation = curr_line.split(" ")[-3:]
            elif "Test" in curr_line:
                test = curr_line.split(" ")[-3:]
            elif "If true" in curr_line:
                next_monkey_true = int(curr_line.split(" ")[-1])
            elif "If false" in curr_line:
                next_monkey_false = int(curr_line.split(" ")[-1])

        return {
            "monkey_id": monkey_id,
            "items": items,
            "operation": operation,
            "test": test,
            "next_monkey_true": next_monkey_true,
            "next_monkey_false": next_monkey_false,
        }

    def update_worry_level(
        self, old_worry_level: int, reduction: int = 3, supermodulo: int = 1
    ):
        """
        Update worry level as monkey inspects item
        """

        first_variable, oper, second_variable = self.operation

        if first_variable == "old":
            first_val = old_worry_level
        else:
            first_val = int(first_variable)

        if second_variable == "old":
            second_val = old_worry_level
        else:
            second_val = int(second_variable)

        if oper == "*":
            new_worry_level = first_val * second_val
        elif oper == "+":
            new_worry_level = first_val + second_val
        elif oper == "-":
            new_worry_level = first_val - second_val
        elif oper == "/":
            new_worry_level = first_val / second_val

        # Increase number of inspections
        self.num_inspections += 1

        # Reduce worry level due to monkey not damaging the item:
        if reduction == 1:
            return new_worry_level % supermodulo
        else:
            return new_worry_level // reduction

    def perform_test(self, worry_level: int):
        """
        Test worry level to determine where to throw the item

        Returns
        -------
        int
            The next monkey to throw to
        """

        if self.test_recipe[0] == "divisible":
            if worry_level % int(self.test_recipe[-1]) == 0:
                return self.next_monkey_true
            else:
                return self.next_monkey_false

    def take_turn(self, reduction: int = 3, supermodulo: int = 1):
        """
        Do a complete turn for monkey
         - inspects and throws all of the items it is holding one at a time and in
           the order listed

        Returns
        -------
        list of dicts
            Format: [{next_monkey: int, item: int}]
        """

        throws = []
        # print(f"Monkey {self.monkey_id}:")

        for i in range(len(self.items)):
            worry_level = self.items.pop(0)
            # print(f"  Monkey inspects an item with a worry level of {worry_level}.")
            new_worry_level = self.update_worry_level(
                worry_level, reduction, supermodulo
            )
            # print(f"    New worry level: {new_worry_level}")
            next_monkey = self.perform_test(new_worry_level)
            # print(
            #     f"    Item with worry level {new_worry_level} is thrown to monkey {next_monkey}"
            # )
            throws.append({"next_monkey": next_monkey, "item": new_worry_level})

        return throws


class MonkeyInTheMiddle:
    def __init__(self, text):
        self.monkeys = []

        self._parse(text)
        self.supermodulo = self.calculate_supermodulo()

    def _parse(self, text):

        for monkey_text in text.split("\n\n"):

            self.monkeys.append(Monkey(monkey_text))

    def play_single_round(self, print_inventory: bool = False, reduction=3):

        for monkey in self.monkeys:
            throws = monkey.take_turn(reduction, supermodulo=self.supermodulo)

            for throw_instructions in throws:
                next_monkey = throw_instructions["next_monkey"]
                new_item = throw_instructions["item"]

                self.monkeys[next_monkey].items.append(new_item)

        if print_inventory:
            self.print_inventory()

    def play_rounds(self, rounds: int, print_inventory: bool = False, reduction=3):

        for i in range(rounds):
            self.play_single_round(print_inventory, reduction)

    def print_inventory(self):
        print("###")
        for monkey in self.monkeys:
            worry_levels = ", ".join([str(x) for x in monkey.items])
            print(f"Monkey {monkey.monkey_id}: {worry_levels}")

    def calculate_supermodulo(self):

        return np.product([int(monkey.test_recipe[-1]) for monkey in self.monkeys])

    def calculate_monkey_business(self):
        inspections = [monkey.num_inspections for monkey in self.monkeys]

        sorted_inspections = sorted(inspections)

        return sorted_inspections[-1] * sorted_inspections[-2]


def parse(puzzle_input):
    """Parse input"""

    game = MonkeyInTheMiddle(puzzle_input)

    return game


def part1(data):
    """Solve part 1"""

    data.play_rounds(20, print_inventory=False, reduction=3)

    return data.calculate_monkey_business()


def part2(data):
    """Solve part 2"""

    data.play_rounds(10000, print_inventory=False, reduction=1)

    return data.calculate_monkey_business()


def solve(puzzle_input):
    """Solve the entire puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(deepcopy(data))
    solution2 = part2(deepcopy(data))

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = Path(path).read_text().strip()

        solutions = solve(puzzle_input)

        print("\n".join(str(solution) for solution in solutions))
