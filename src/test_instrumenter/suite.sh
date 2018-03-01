#!/usr/bin/env bash
cd "$(dirname "$0")"

run_test() {
	echo "Running tests in $1"
	python3 "$1"
	echo "Done"
	echo ""
	echo ""
}

for test_file in *.py; do
	run_test "$test_file"
done