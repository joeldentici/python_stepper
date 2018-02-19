from report_state import state_to_string

class CommandlineReporter:
	def __init__(self):
		self.prev = None
		self.history = []

	def report(self, old, new):
		self.history.append((old, new))
		self.show(self.history[-1])

	def show(self, reduction):
		print(chr(27) + "[2J")

		old,new = reduction

		old_str = state_to_string(old, self.highlight(Color.YELLOW))
		new_str = state_to_string(new, self.highlight(Color.YELLOW))

		old_lines = old_str.split("\n")
		new_lines = new_str.split("\n")

		old_orig_lines = state_to_string(old).split("\n")
		old_max = max(len(line) for line in old_orig_lines)

		num_lines = max(len(old_lines), len(new_lines))
		i = 0
		while i < num_lines:
			old_line = old_lines[i] if i < len(old_lines) else ""
			old_orig = old_orig_lines[i] if i < len(old_orig_lines) else ""
			new_line = new_lines[i] if i < len(new_lines) else ""
			print(self.pad(old_line, old_orig, old_max) + '\t|\t' + new_line)
			i = i + 1

		self.get_next_action()

	def pad(self, line, orig, length):
		padding_amount = length - len(orig)
		return line + (" " * padding_amount)


	def highlight(self, color):
		return lambda what: "\n".join(color + x + Color.ENDC for x in what.split("\n"))

	def 


class Color:
	BOLD = '\033[1m'
	ENDC = '\033[0m'
	YELLOW = '\033[93m'

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