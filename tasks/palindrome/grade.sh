#!/usr/bin/env bash
set -u
expected="yes"
got="$(cat)"
if [[ "$got" == "$expected" ]]; then exit 0; fi
echo "palindrome: expected '$expected', got '$got'" >&2
exit 1
