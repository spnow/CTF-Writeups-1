def is2(n):
	if (n <= 3): 
		if (n <= 1): 
			return False
		return True
	if (n % 2 == 0 or n % 3 == 0):
		return False;
	n2 = 5;
	while (n2 * n2 <= n):
		if (n % n2 == 0 or n % (n2 + 2) == 0) :
			return False
		n2 += 6;
	return True


count = 200000
k = 0
while(count):
	if is2(count):
		k += 100
	else:
		k -= 1
	#print k,count
	count -= 1
print k, count, hex(k)
