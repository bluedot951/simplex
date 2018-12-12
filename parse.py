import numpy as np
import simplex as s

from scipy import optimize as opt

# f = open('test3.txt', 'r').read().split('\n')




# print 'A', A
# print 'b', b
# print 'c', c

# 1/0


def test(filename, m, n):
	f = open(filename, 'r').read().split('\n')

	c = []
	AB = []

	stage = -1
	for line in f:
		if line.strip() == 'C':
			# print 'stage 0'
			stage = 0
			continue
		if line.strip() == 'A, B':
			# print 'stage 1'
			stage = 1
			continue

		# print line

		if stage == 0:
			c.extend([float(x) for x in line.split()])

		else:
			AB.extend([float(x) for x in line.split()])


	c = np.array(c)
	AB = np.array(AB).reshape((m, m+n+1))

	A = AB[:, :-1]
	b = AB[:, -1]

	b = np.expand_dims(b, axis=1)
	c = np.expand_dims(c, axis=0)

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

	return np.allclose(optV, -1 * res['fun']), optV

print test('test.txt', 3, 2)
print test('test2.txt', 3, 2)
print test('test3.txt', 3, 3)
print test('test4.txt', 10, 15)
print test('test5.txt', 20, 35)
print test('test6.txt', 200, 350)
print test('test8.txt', 500, 500)
