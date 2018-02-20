from report_state import state_to_string
import sys

class CommandlineReporter:
	def __init__(self):
		self.prev = None
		self.history = []

	def report(self, old, new):
		self.history.append((old, new))
		self.location = len(self.history) - 1
		self.interact()

	def show(self):
		print(chr(27) + "[2J")

		old,new = self.current_reduction()

		old_str = state_to_string(old, self.highlight(Color.RED))
		new_str = state_to_string(new, self.highlight(Color.GREEN))

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

	def pad(self, line, orig, length):
		padding_amount = length - len(orig)
		return line + (" " * padding_amount)


	def highlight(self, color):
		return lambda what: "\n".join(color + x + Color.ENDC for x in what.split("\n"))

	def interact(self):
		while self.location < len(self.history):
			self.show()
			while True:
				print("\n")
				step = input(self.get_message()).lower()
				if self.is_valid(step):
					self.increment(step)
					break
				else:
					print("Invalid step: " + step)

	def current_reduction(self):
		return self.history[self.location]

	def increment(self, step):
		increments = {
			'n': 1,
			'p': -1
		}
		self.location += increments[step]

	def is_valid(self, step):
		valid_steps = {'n', 'p', 'e'}
		if step not in valid_steps:
			return False
		if step == "p" and self.location == 0:
			return False
		if step == "e":
			sys.exit(0)

		return True

	def get_message(self):
		if self.location == 0:
			return "e: Exit Stepper    n: Next Step> "
		else:
			return "e: Exit Stepper    p: Previous Step    n: Next Step> "



class Color:
	ENDC = '\033[0m'
	GREEN = '\033[102m'
	RED = '\033[101m'