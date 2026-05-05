#!/usr/bin/env bash
set -u
expected="5 4 3 2 1"
got="$(cat)"
if [[ "$got" == "$expected" ]]; then exit 0; fi
echo "reverse: output mismatch — expected '$expected', got '$got'" >&2
exit 1
