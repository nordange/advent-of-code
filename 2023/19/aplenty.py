# aplenty.py

from collections import deque
import numpy as np
import parse
from pathlib import Path
import sys


def parse_input(puzzle_input):
    """Parse input"""

    workflows, parts = puzzle_input.split("\n\n")

    parsed_input = {"workflows": {}, "parts": []}

    for line in workflows.split("\n"):
        match = parse.search("{name}{{{rules}}}", line)

        rule_defs = []
        for rule in match["rules"].split(","):
            if ":" in rule:
                rule_match = parse.parse("{cat}{op}{value:d}:{next}", rule)
                rule_def = {
                    "cat": rule_match["cat"],
                    "op": rule_match["op"],
                    "value": rule_match["value"],
                    "next": rule_match["next"],
                }
            else:
                rule_def = {"next": rule}
            rule_defs.append(rule_def)

        parsed_input["workflows"][match["name"]] = rule_defs

    for line in parts.split("\n"):
        match = parse.search("x={x:d},m={m:d},a={a:d},s={s:d}", line)

        parsed_input["parts"].append(
            {"x": match["x"], "m": match["m"], "a": match["a"], "s": match["s"]}
        )

    return parsed_input


def process_part(part, workflows, start_workflow):
    curr_workflow = workflows[start_workflow]

    rule_id = 0

    while rule_id < len(curr_workflow):
        curr_rule = curr_workflow[rule_id]

        if "cat" in curr_rule.keys():
            rule_exp = f"{part[curr_rule['cat']]}{curr_rule['op']}{curr_rule['value']}"
            rule_exp_eval = eval(rule_exp)

            if rule_exp_eval:
                if curr_rule["next"] in "AR":
                    return curr_rule["next"]
                else:
                    curr_workflow = workflows[curr_rule["next"]]
                    rule_id = 0
            else:
                rule_id += 1

        else:
            if curr_rule["next"] in "AR":
                return curr_rule["next"]
            else:
                curr_workflow = workflows[curr_rule["next"]]
                rule_id = 0


def get_num_accept_combos(workflows, start_workflow):
    min_rating = 1
    max_rating = 4000

    intervals = {
        "x": (min_rating, max_rating),
        "m": (min_rating, max_rating),
        "a": (min_rating, max_rating),
        "s": (min_rating, max_rating),
    }

    wf_queue = deque()

    wf_queue.append({"workflow": start_workflow, "intervals": intervals, "rule_id": 0})

    accepted = []

    while len(wf_queue):
        curr_data = wf_queue.popleft()
        curr_workflow = workflows[curr_data["workflow"]]
        curr_rule = curr_workflow[curr_data["rule_id"]]
        curr_intervals = curr_data["intervals"]

        if "cat" in curr_rule.keys():
            cat = curr_rule["cat"]

            new_true_intervals = curr_intervals.copy()
            new_false_intervals = curr_intervals.copy()

            if curr_rule["op"] == ">":
                new_true_intervals[cat] = (
                    max(curr_intervals[cat][0], curr_rule["value"] + 1),
                    curr_intervals[cat][1],
                )
                new_false_intervals[cat] = (
                    curr_intervals[cat][0],
                    min(curr_intervals[cat][1], curr_rule["value"]),
                )

            elif curr_rule["op"] == "<":
                new_true_intervals[cat] = (
                    curr_intervals[cat][0],
                    min(curr_rule["value"] - 1, curr_intervals[cat][1]),
                )
                new_false_intervals[cat] = (
                    max(curr_rule["value"], curr_intervals[cat][0]),
                    curr_intervals[cat][1],
                )

            if curr_rule["next"] == "A":
                accepted.append(
                    np.prod([x[1] - x[0] + 1 for x in new_true_intervals.values()])
                )

            elif curr_rule["next"] == "R":
                accepted.append(0)

            elif curr_rule["next"] != "R":
                wf_queue.append(
                    {
                        "workflow": curr_rule["next"],
                        "intervals": new_true_intervals,
                        "rule_id": 0,
                    }
                )

            if (curr_data["rule_id"] + 1) < len(curr_workflow):
                if curr_workflow[curr_data["rule_id"] + 1] == "A":
                    accepted.append(
                        np.prod([x[1] - x[0] + 1 for x in new_false_intervals.values()])
                    )

                elif curr_workflow[curr_data["rule_id"] + 1] == "R":
                    accepted.append(0)

                elif curr_workflow[curr_data["rule_id"] + 1] != "R":
                    wf_queue.append(
                        {
                            "workflow": curr_data["workflow"],
                            "intervals": new_false_intervals,
                            "rule_id": curr_data["rule_id"] + 1,
                        }
                    )

        else:
            if curr_rule["next"] == "A":
                accepted.append(
                    np.prod([x[1] - x[0] + 1 for x in curr_intervals.values()])
                )
            elif curr_rule["next"] == "R":
                accepted.append(0)
            elif curr_rule["next"] not in "AR":
                wf_queue.append(
                    {
                        "workflow": curr_rule["next"],
                        "intervals": curr_intervals,
                        "rule_id": 0,
                    }
                )

    return accepted


def part1(data):
    """Solve part 1"""

    verdict = []

    sum_ratings = 0

    for part in data["parts"]:
        curr_verdict = process_part(part, data["workflows"], "in")
        verdict.append(curr_verdict)

        if curr_verdict == "A":
            sum_ratings += sum(part.values())

    return sum_ratings


def part2(data):
    """Solve part 2"""

    num_combos = get_num_accept_combos(data["workflows"], "in")

    return sum(num_combos)


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
