#! /usr/bin/env bash

script_dir="$(dirname "$0")"
cd "$script_dir"

echo "Testing library:"
python3 -m "unittest" "test_library.py"