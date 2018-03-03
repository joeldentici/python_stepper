def fact_acc(n, acc):
	return acc if n < 2 else fact_acc(n - 1, acc * n)

def fact(n):
	return fact_acc(n, 1)

result = fact(5)
