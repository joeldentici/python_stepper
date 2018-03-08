import re

def indent(what):
	lines = what.split("\n")
	indentation = '   '
	return "\n".join(indentation + x for x in lines)

def dict_state_to_string(state, active_transform):
	if (state["type"] == "statement_group"):
		return "\n".join(state_to_string(x, active_transform) for x in state["statements"] if x)
		#return "\n".join(indent(x, 1) for x in stmts)
	elif (state["type"] == "function_activation"):
		return "{|\n" + indent(state_to_string(state["value"], active_transform)) + "\n|}"
	elif (state["type"] == "block"):
		return indent(state_to_string(state["value"], active_transform))
	elif (state["type"] == "statement"):
		return state_to_string(state["value"], active_transform)
	elif (state["type"] == "active_component"):
		val = state_to_string(state["value"], active_transform)
		return active_transform(val)

	raise NotImplementedError("Type " + state["type"])

def list_state_to_string(state, active_transform):
	return "".join(state_to_string(x, active_transform) for x in state)

def state_to_string(state, active_transform = lambda x: x):
	if (isinstance(state, dict)):
		return dict_state_to_string(state, active_transform)
	elif (isinstance(state, list)):
		return list_state_to_string(state, active_transform)
	else:
		return state

def rename_statements(scope, stmts):
	print(stmts)
	return [rename_statement(scope, x) for x in stmts]

def rename_statement(scope, stmt):
	x = re.sub(r'<@ (.*?) @>', lambda o: scope.resolve_name(o.group(1)), stmt)
	return x.replace('\n\n', '\n')
