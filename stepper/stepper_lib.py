import sys
'''
stepper_lib

Python library for the stepper. Like many debugging/profiling tools,
the stepper works by emitting calls to this library in a user's code.

The functions in this library record the evaluation of the program.
'''

#call history for entire program!
call_history = []
#environment stack (like call stack, only
#the active activation records are stored)
envs = [({}, '')]
#store environments (for closures)
stored_envs = {}

'''
push_call :: (any, Dict string any) -> ()

Pushes a call onto the environment stack and
records it in the call history.
'''
def push_call(fid, env):
	global envs, call_history, stored_envs

	if fid in stored_envs:
		tmp = dict(stored_envs[fid])
		tmp.update(env)
		env = tmp

	if callable(fid):
		fid = fid.__name__

	call_history.append(('Call', fid, env))
	envs.append((env, fid))
	print_stack('call')

'''
pop_call :: (any, Dict string any) -> ()

Pops a call off the environment stack and
records the return value of the function
in the call history.
'''
def pop_call(fid, ret):
	global env, call_history

	if callable(ret):
		ret = ret.__name__

	if callable(fid):
		fid = fid.__name__

	call_history.append(('Return', fid, ret))
	print_stack('return', ret)
	envs.pop()


'''
store_env :: any -> ()

Stores an environment for a function id.

We need this to properly report the environment
for higher order functions that return functions
(upward funargs/currying). This is essentially the
same as creating a closure, but we store the environment
in a table and look it up when the function is evaluated.
'''
def store_env(fid):
	global stored_envs
	stored_envs[fid] = envs[-1][0]

'''
print_call_history :: () -> ()

Called as the last statement by the program,
which prints out the historical call stack since
the program started.
'''
def print_call_history():
	return
	for (t, f, v) in call_history:
		print(t, f, v)

def errprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def print_stack(what, ret = None):
	top_border = '-' * 5
	bot_border = '-' * (10 + len(what))

	errprint(top_border + what + top_border)
	for depth,(env,name) in enumerate(envs[1:]):
		tab = '\t' * depth
		if ret and depth == len(envs[1:]) - 1:
			errprint(tab + name, ret)
		else:
			errprint(tab + name, env)

	errprint(bot_border)
	errprint('')