states = []
envs = []

def push_env(fn, ext):
	global env, states
	newEnv = dict(envs[-1]) if len(envs) > 0 else {}
	newEnv.update(ext)
	states.append(('Call', fn, newEnv))
	envs.append(newEnv)

def pop_env(fn, ret):
	global env, states
	states.append(('Return', fn, ret))
	envs.pop()

def print_state():
	for (t, f, v) in states:
		print t, f, v