

class CommandlineReporter:
	def __init__(self):
		self.prev = None

	def report(self, val):
		src = state_to_string(val)
		if src != self.prev:
			self.prev = src
			print(src)
			input()

def indent(what):
	lines = what.split("\n")
	indentation = '\t'
	return "\n".join(indentation + x for x in lines)

def dict_state_to_string(state):
	if (state["type"] == "statement_group"):
		return "\n".join(state_to_string(x) for x in state["statements"] if x)
		#return "\n".join(indent(x, 1) for x in stmts)
	elif (state["type"] == "function_activation"):
		return "{|\n" + indent(state_to_string(state["value"])) + "\n" + "|}"
	elif (state["type"] == "statement"):
		return state_to_string(state["value"])

	raise NotImplementedError("Type " + state["type"])

def list_state_to_string(state):
	return "".join(state_to_string(x) for x in state)

def state_to_string(state):
	if (isinstance(state, dict)):
		return dict_state_to_string(state)
	elif (isinstance(state, list)):
		return list_state_to_string(state)
	else:
		return state

#import re
'''
class CommandlineReporter:
	def __init__(self):
		pass

	def report(self, val):
		BOLD = '\033[1m'
		ENDC = '\033[0m'
		YELLOW = '\033[93m'

		START = BOLD + YELLOW

		val = re.sub(
			r"(.*)\(\*\)(.*)\(\*\)(.*)",
			r"\1" + START + r"\2" + ENDC + r"\3",
			val,
			flags=re.DOTALL
		)

		print(val)
		input()

'''