import math
n = int(input())
s = int(input())
area = (n * s * s) / (4 * math.tan(math.pi / n))
print(int(area))