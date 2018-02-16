def fact(n):
	acc = 1
	while n > 1:
		acc = acc * n
		n = n - 1
	return acc

fact(5)