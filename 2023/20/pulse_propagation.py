# pulse_propagation.py

from collections import deque
from math import gcd
import numpy as np
import parse
from pathlib import Path
import sys


def parse_input(puzzle_input):
    """Parse input"""

    parsed_input = []

    MODULE_TYPES = {"%": "flip-flop", "&": "conjunction"}

    for line in puzzle_input.split("\n"):
        curr_input = {}

        match = parse.parse("{type:W}{from} -> {to}", line)
        if match is None:
            match = parse.parse("{from} -> {to}", line)
            curr_input["type"] = "broadcaster"
        else:
            curr_input["type"] = MODULE_TYPES[match["type"]]

        curr_input["name"] = match["from"]
        curr_input["destinations"] = [x.strip() for x in match["to"].split(",")]

        parsed_input.append(curr_input)

    return parsed_input


class Node:
    def __init__(self, name: str, value, destinations):
        self.name = name
        self.destinations = destinations
        self.value = value

    def process_pulse_signal(self):
        raise NotImplemented

    def process_pulse(self, pulse: bool, input_from: str):
        """
        Return (from, to, pulse) for all destinations. This will be queued later.
        """

        if self.type in "conjunction":
            new_pulses = [
                (
                    self.name,
                    dest,
                    self.process_pulse_signal(pulse=pulse, input_from=input_from),
                )
                for dest in self.destinations
            ]

        else:
            new_pulse = self.process_pulse_signal(pulse=pulse)
            new_pulses = [(self.name, dest, new_pulse) for dest in self.destinations]

        cleansed_pulses = [x for x in new_pulses if x[2] is not None]

        return cleansed_pulses

    def __repr__(self):
        return f"{self.type} : -> {self.destinations}"


class FlipFlop(Node):
    """
    A flip-flop can be ON (True) or OFF (False)
    """

    def __init__(self, name: str, value=False, destinations=None):
        super().__init__(name, value, destinations)
        self.type = "flip-flop"

    def process_pulse_signal(self, pulse: bool, **kwargs):
        """
        High pulse (True) : do nothing
        Low pulse (False) : flip on/off

        Return
        ------
        None if high pulse
        When low pulse is received:
            If off: return high pulse
            If on: return low pulse
        """

        if pulse == True:
            return None
        elif pulse == False:
            if self.value == False:
                self.value = not self.value
                return True
            elif self.value == True:
                self.value = not self.value
                return False


class Conjunction(Node):
    """
    A conjunction remembers the most recent pulse from each of the input modules
    """

    def __init__(self, name: str, value, destinations, inputs):
        super().__init__(name, value, destinations)
        self.type = "conjunction"
        self.recent_pulse = {x: False for x in inputs}

    def process_pulse_signal(self, pulse: bool, input_from: str, **kwargs):
        self.recent_pulse[input_from] = pulse
        if all(self.recent_pulse.values()):
            return False
        else:
            return True


class Broadcaster(Node):
    """
    A broadcaster sends the same pulse to all its destinations
    """

    def __init__(self, name: str, value, destinations, *kwargs):
        super().__init__(name, value, destinations)
        self.type = "broadcaster"

    def process_pulse_signal(self, pulse: bool, **kwargs):
        return pulse


class Output(Node):
    """
    Dummy test output
    """

    def __init__(self, name: str, value, destinations, *kwargs):
        super().__init__(name, value, destinations)
        self.type = "output"

    def process_pulse_signal(self, pulse: bool, **kwargs):
        return None


def prepare_modules(data):
    """
    Create all nodes
    1. Dict node_name : actual_node
    2. Create inputs for conjunctions

    """

    conjunctions = [x for x in data if x["type"] == "conjunction"]

    conjunction_inputs = {}
    for conjunction in conjunctions:
        curr_inputs = [
            x["name"] for x in data if conjunction["name"] in x["destinations"]
        ]

        conjunction_inputs[conjunction["name"]] = curr_inputs

    modules = {}
    destinations = set()
    for module in data:
        destinations.update(module["destinations"])
        if module["type"] == "flip-flop":
            modules[module["name"]] = FlipFlop(
                module["name"], value=False, destinations=module["destinations"]
            )
        elif module["type"] == "conjunction":
            modules[module["name"]] = Conjunction(
                module["name"],
                value=None,
                destinations=module["destinations"],
                inputs=conjunction_inputs[module["name"]],
            )
        elif module["type"] == "broadcaster":
            modules[module["name"]] = Broadcaster(
                module["name"], value=None, destinations=module["destinations"]
            )

    # Add outputs
    sources = set(modules.keys())

    outputs = destinations.difference(sources)

    for output in outputs:
        modules[output] = Output(output, value=None, destinations=[])

    return modules


def press_button(modules, debug_output=False):
    pulse_queue = deque()

    # Queue elements: (from, to, pulse)

    pulse_queue.append(("Button", "broadcaster", False))

    num_low_pulses = 1  # Button is the first
    num_high_pulses = 0

    if debug_output:
        print("\n#####")

    while len(pulse_queue) > 0:
        from_module, to_module, curr_pulse = pulse_queue.popleft()

        new_pulses = modules[to_module].process_pulse(curr_pulse, from_module)

        for new_pulse in new_pulses:
            pulse_queue.append(new_pulse)

            if new_pulse[2]:
                num_high_pulses += 1
            else:
                num_low_pulses += 1

            if debug_output:
                pulse_str = "-high" if new_pulse[2] else "-low"
                print(f"{new_pulse[0]} {pulse_str}-> {new_pulse[1]}")

    return num_low_pulses, num_high_pulses


def press_button_first_high_pulse(modules, conjuction_module, input_module):
    """
    Returns True if a single low pulse is delivered to module rx
    """

    pulse_queue = deque()

    # Queue elements: (from, to, pulse)
    pulse_queue.append(("Button", "broadcaster", False))

    while len(pulse_queue) > 0:
        from_module, to_module, curr_pulse = pulse_queue.popleft()

        new_pulses = modules[to_module].process_pulse(curr_pulse, from_module)

        for new_pulse in new_pulses:
            pulse_queue.append(new_pulse)

            if (
                new_pulse[0] == input_module
                and new_pulse[1] == conjuction_module
                and new_pulse[2] == True
            ):
                return True

    return False


def part1(data):
    """Solve part 1"""

    num_button_pushes = 1000

    modules = prepare_modules(data)

    overall_low_pulses = 0
    overall_high_pulses = 0

    for button_push_idx in range(num_button_pushes):
        num_low_pulses, num_high_pulses = press_button(modules, debug_output=False)

        overall_low_pulses += num_low_pulses
        overall_high_pulses += num_high_pulses

    return overall_low_pulses * overall_high_pulses


def part2(data):
    """Solve part 2"""

    modules = prepare_modules(data)

    # Find the module sending to rx
    module_to_rx = [x.name for x in modules.values() if "rx" in x.destinations][0]

    # The inputs to this module
    inputs = list(modules[module_to_rx].recent_pulse.keys())

    # We need to find the greatest common divisor among these input modules
    # As the module (ql) that sends to rx is a conjunction module, all its inputs need
    # to have high as the most recent signal for it to send a low pulse

    # 1. Find the number of button presses required for each of the inputs
    # 2. Calculate the gcd

    button_presses = {}
    for module_input in inputs:
        modules = prepare_modules(data)

        searching = True
        num_button_pushes = 0

        while searching:
            num_button_pushes += 1
            searching = not press_button_first_high_pulse(
                modules, module_to_rx, module_input
            )

        button_presses[module_input] = num_button_pushes

    steps_per_module = np.array([*button_presses.values()])

    min_presses_overall = np.prod(
        np.array(steps_per_module) // gcd(*steps_per_module)
    ) * gcd(*steps_per_module)

    return min_presses_overall


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
