#!/usr/bin/env python3
"""
Proposer: read the latest iteration's diagnostic runs and emit an improved
harness. POC implementation — looks at which tasks failed, picks one whose
fix-hint is not yet present in the system prompt, and emits harness/v{N+1}.

In a real meta-harness, this is replaced by:
  islo use --snapshot meta-base --agent claude --task \\
    "Examine /workspace/runs/iter-{N}, find a common failure mode, write
     a better /workspace/harness/v{N+1}/system.md"

The orchestrator keeps the same wiring either way — only this file changes.

Usage: proposer.py <repo_root> <current_harness_version>
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Per-task fix hint. Order matters: earlier failures get fixed first
# so the demo progression reads cleanly: simplest failures first.
HINTS = [
    ("fizzbuzz",   "Loops are 1-indexed: count from 1 through N inclusive."),
    ("primes",     "The smallest prime is 2 — 1 is not prime."),
    ("reverse",    "When asked for separated values, use space-separated output."),
    ("sum-evens",  "Range bounds are inclusive — include both endpoints."),
    ("palindrome", "Format constraints are exact-case — produce all lowercase only when required."),
]


def latest_iter(runs_dir: Path) -> Path | None:
    iters = sorted(runs_dir.glob("iter-*"), key=lambda p: int(p.name.split("-")[1]))
    return iters[-1] if iters else None


def failing_tasks(iter_dir: Path) -> set[str]:
    fails = set()
    for task_dir in iter_dir.iterdir():
        if not task_dir.is_dir():
            continue
        result = task_dir / "result.json"
        if not result.exists():
            continue
        meta = json.loads(result.read_text())
        if not meta.get("pass", False):
            fails.add(task_dir.name)
    return fails


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: proposer.py <repo_root> <current_harness_version>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1])
    cur_version = sys.argv[2]
    cur_dir = root / "harness" / cur_version
    runs_dir = root / "runs"

    iter_dir = latest_iter(runs_dir)
    if iter_dir is None:
        print("no iter-* runs found; nothing to propose", file=sys.stderr)
        return 1

    fails = failing_tasks(iter_dir)
    if not fails:
        print("[propose] all tasks passing; converged", file=sys.stderr)
        print("CONVERGED")
        return 0

    cur_system = (cur_dir / "system.md").read_text()
    chosen = None
    for task, hint in HINTS:
        if task in fails and hint not in cur_system:
            chosen = (task, hint)
            break
    if chosen is None:
        print(f"[propose] failing tasks {sorted(fails)} have no unused hint", file=sys.stderr)
        print("STUCK")
        return 0

    task, hint = chosen
    n = int(cur_version.lstrip("v"))
    new_version = f"v{n+1}"
    new_dir = root / "harness" / new_version
    new_dir.mkdir(parents=True, exist_ok=True)
    new_system = cur_system.rstrip() + (
        f"\n\n## Added in {new_version} (from {iter_dir.name} → {task} failure)\n"
        f"- {hint}\n"
    )
    (new_dir / "system.md").write_text(new_system)
    (new_dir / "meta.json").write_text(json.dumps({
        "version": new_version,
        "parent": cur_version,
        "rationale": f"Diagnostic from {iter_dir.name}: '{task}' failed; added a hint targeting that failure.",
        "diagnostic_basis": sorted(fails),
        "added_hint": hint,
        "target_task": task,
        "created": datetime.now(timezone.utc).isoformat(),
    }, indent=2) + "\n")
    print(new_version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
