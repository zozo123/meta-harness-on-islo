#!/usr/bin/env bash
set -u
expected=$'2\n3\n5\n7\n11\n13\n17\n19\n23\n29'
got="$(cat)"
if [[ "$got" == "$expected" ]]; then exit 0; fi
echo "primes: output mismatch" >&2
diff <(printf '%s' "$expected") <(printf '%s' "$got") | head -20 >&2
exit 1
