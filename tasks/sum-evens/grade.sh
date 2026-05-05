#!/usr/bin/env bash
set -u
expected="30"
got="$(cat)"
if [[ "$got" == "$expected" ]]; then exit 0; fi
echo "sum-evens: expected '$expected', got '$got'" >&2
exit 1
