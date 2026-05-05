#!/usr/bin/env bash
# Grades stdout from an agent run for the fizzbuzz task.
# Exit 0 = pass, non-zero = fail. Writes a 1-line reason to stderr on failure.
set -u
expected=$'1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz'
got="$(cat)"
if [[ "$got" == "$expected" ]]; then exit 0; fi
echo "fizzbuzz: output mismatch" >&2
diff <(printf '%s' "$expected") <(printf '%s' "$got") | head -20 >&2
exit 1
