#giai phuong trinh bat 2
import math


#aaaa
def find_x(a,b,c):
	
	if (b**2) - (4 *a *c) < 0 or a == b == 0:
		return "false"
	elif (b**2) - (4 *a *c) == 0:
		x = -b/(2*a)
		return x
	else:
		if a != 0:
			delta = (b**2) - (4 *a *c)
			delta =  int(math.sqrt(delta))
			x1 = (-b - delta)/(2*a)
			x2 = (-b + delta)/ (2 *a)
			return x1, x2
		
		elif a == 0:
			x = c/b
			return x
		
while True:
	a , b,c = [int(a) for a in input("abc: ").split()]
	print(find_x(a,b,c))

 