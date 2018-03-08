

def factorial(n):
	if (n < 2):
		n = n + 1
		return 1

	return n * factorial(n - 1)

factorial(5)
