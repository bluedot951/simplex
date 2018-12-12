import numpy as np
import simplex as s

from scipy import optimize as opt

f = open('test3.txt', 'r').read().split('\n')

c = []
AB = []

m = 3
n = 3

stage = -1
for line in f:
	if line.strip() == 'C':
		print 'stage 0'
		stage = 0
		continue
	if line.strip() == 'A, B':
		print 'stage 1'
		stage = 1
		continue

	print line

	if stage == 0:
		c.extend([float(x) for x in line.split()])

	else:
		AB.extend([float(x) for x in line.split()])


c = np.array(c)
AB = np.array(AB).reshape((m, m+n+1))

A = AB[:, :-1]
b = AB[:, -1]

print 'A', A
print 'b', b
print 'c', c

1/0


def test(filename, m, n):
	f = open('test2.txt', 'r').read().split('\n')

	A = np.zeros((m, m+n))
	b = np.zeros((m,1))

	for i in range(1, 2):
		data = [float(x) for x in f[i].split()]
		data = [d for d in data]
		c = np.array([data])

	count = 0
	for i in range(3, m*2 + 3, 2):
		# print i
		# print f[i]
		row = np.array([float(x) for x in f[i].split()])
		bi = [float(x) for x in f[i+1].split()][0]
		A[count, :] = row
		b[count] = bi
		count += 1

	b = b.T

	# print 'A', A
	# print 'b', b
	# print 'c', c

	Aup = A[:m, :n]
	cup = c[0, :n]

	# print 'Aup', Aup
	# print 'cup', cup

	res = opt.linprog(-1 * cup, Aup, b)
	# print res['x'], -1 * res['fun']

	c = np.append(c, 0)

	# print A.shape
	# print b.shape
	# print c.shape



	optV, vec = s.solve(A, b, c, 'max', False)

	return np.allclose(optV, -1 * res['fun'])

print test('test.txt', 3, 2)
print test('test2.txt', 3, 2)
print 
