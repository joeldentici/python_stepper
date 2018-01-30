import instrumenter
import unittest

class TestRef(unittest.TestCase):

	def test_ref_one(self):
		src = """
abc(x)
		""".strip()

		expected = """
abc(stepper_lib.ref('x', x))
		""".strip()

		actual = instrumenter.instrument(src, "ref").strip()

		self.assertEqual(actual, expected)

	def test_ref_one(self):
		src = """
y = 5
		""".strip()

		expected = """
y = 5
		""".strip()

		actual = instrumenter.instrument(src, "ref").strip()

		self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()