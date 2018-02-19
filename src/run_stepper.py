#!/usr/bin/env python3
import sys
import tempfile
import instrumenter
import os
from shutil import copy2

'''
run_stepper.py
written by Joel Dentici
on 01/22/2018

Evaluate a python script with the
stepper.

Usage:
./run_stepper.py <script> ...<command-line-args>

The script is instrumented, and
placed into a temporary directory with the
stepper_lib runtime, then executed with the
specified command line arguments. It will have
its stdin and stdout appropriately piped to the
parent process stdin and stdout.
'''

def copy_lib(tmp):
	location = os.path.dirname(os.path.abspath(__file__))

	# todo: read this from fs
	files = [
		'assignment_statement.py',
		'binary_operation.py',
		'commandline_reporter.py',
		'expr_statement.py',
		'function_call.py',
		'function_def.py',
		'identifier.py',
		'if_expr.py',
		'if_stmt.py',
		'lambda_expression.py',
		'program.py',
		'reducible.py',
		'report_state.py',
		'return_statement.py',
		'statement_group.py',
		'stepper_lib.py',
		'value.py',
		'while_loop.py',
	]

	# TODO: Use platform specific paths
	paths = (location + '/include/' + file for file in files)

	for path in paths:
		copy2(path, tmp)

def run_stepper(script, src, args):
	# instrument source code
	instrumented = instrumenter.instrument(src)

	# created temporary directory to run in
	with tempfile.TemporaryDirectory() as tmp:
		# path to instrumented script
		script_path = tmp + '/' + os.path.basename(script)

		copy_lib(tmp)
		# TODO: Use platform specific paths
		# write instrumented script
		with open(script_path, 'w') as f:
			f.write(instrumented)

		# TODO: use subprocess and set up piped IO streams
		# run instrumented script
		os.system('python3 ' + script_path + ' ' + ' '.join(args))


# get command line arguments
if len(sys.argv) < 2:
	print("""Usage:
./run_stepper.py <script> ...<command-line-args>""")
args = sys.argv[2:] if len(sys.argv) > 2 else []
script = sys.argv[1]

with open(script, 'r') as f:
	src = f.read()
	run_stepper(script, src, args)