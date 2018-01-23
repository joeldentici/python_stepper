import instrumenter
import unittest

class TestModuleDef(unittest.TestCase):

	def test_module_def(self):
		src = """
def add(x, y):
	return x + y
		""".strip()

		expected = """
import stepper_lib


def add(x, y):
	return x + y
		""".strip()

		actual = instrumenter.instrument(src, "module").strip()

		self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()