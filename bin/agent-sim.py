#!/usr/bin/env python3
"""
Deterministic stand-in for an LLM agent. Reads the harness system prompt and
the task prompt, then produces stdout for the task. Each task has a known
"buggy default" output that gets corrected when the harness contains the
relevant hint keyword. This lets the meta-harness loop run end-to-end offline
in seconds, with the same wiring you would use against a real agent in an
islo sandbox.

Usage: agent-sim.py <harness_dir> <task_dir>
"""
import sys
import re
from pathlib import Path


def _fb(i: int) -> str:
    if i % 15 == 0: return "FizzBuzz"
    if i % 3 == 0:  return "Fizz"
    if i % 5 == 0:  return "Buzz"
    return str(i)


TASKS = {
    "fizzbuzz": {
        "buggy":   "\n".join(_fb(i) for i in range(15)),       # 0..14: off-by-one
        "hint":    r"\b1-?indexed\b|start (?:at|from) 1\b",
        "correct": "\n".join(_fb(i) for i in range(1, 16)),
    },
    "primes": {
        "buggy":   "1\n2\n3\n5\n7\n11\n13\n17\n19\n23",        # treats 1 as prime
        "hint":    r"smallest prime is 2|2 is the first prime|1 is not prime",
        "correct": "2\n3\n5\n7\n11\n13\n17\n19\n23\n29",
    },
    "reverse": {
        "buggy":   "5,4,3,2,1",
        "hint":    r"space[- ]separated|use space separator",
        "correct": "5 4 3 2 1",
    },
    "sum-evens": {
        "buggy":   "20",                                        # exclusive upper bound
        "hint":    r"\binclusive\b|include both endpoints",
        "correct": "30",
    },
    "palindrome": {
        "buggy":   "Yes",                                       # wrong case
        "hint":    r"lowercase only|exact case|all lowercase",
        "correct": "yes",
    },
}


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: agent-sim.py <harness_dir> <task_dir>", file=sys.stderr)
        return 2
    harness_dir = Path(sys.argv[1])
    task_dir = Path(sys.argv[2])
    task_name = task_dir.name
    if task_name not in TASKS:
        print(f"unknown task: {task_name}", file=sys.stderr)
        return 2

    system_md = (harness_dir / "system.md").read_text()
    spec = TASKS[task_name]
    hint_present = bool(re.search(spec["hint"], system_md, flags=re.IGNORECASE))
    print(f"[sim] harness={harness_dir.name} task={task_name} hint_present={hint_present}", file=sys.stderr)
    sys.stdout.write(spec["correct"] if hint_present else spec["buggy"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
