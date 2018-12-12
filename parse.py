import numpy as np
import simplex as s

from sys import argv

from scipy import optimize as opt

# f = open('test3.txt', 'r').read().split('\n')


# method = argv[1]

# print 'A', A
# print 'b', b
# print 'c', c

# 1/0

def test(A, b, c, m, n):
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



	optV, vec, num_pivots = s.solve(A, b, c, 'max', method, False)
	if not np.allclose(optV, -1 * res['fun']):
		print opt, vec, num_pivots
		print 'NOT THE SAME AS SCIPY'
		1/0

	return np.allclose(optV, -1 * res['fun']), optV, num_pivots

def test_random(m, n):
	A = 100 * np.random.rand(m, n)
	b = 100 * np.random.rand(1, m)
	c = 100 * np.random.rand(n)

	A = np.hstack((A, np.identity(m)))
	c = np.hstack((c, np.zeros(m)))
	c = np.expand_dims(c, axis=0)

	# print 'A', A.shape
	# print 'b', b.shape
	# print 'c', c.shape

	return test(A, b, c, m, n)

def parse_file(filename, m, n):
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

	print 'A', A.shape
	print 'b', b.shape
	print 'c', c.shape

	return test(A, b, c, m, n)

# print parse_file('test/test.txt', 3, 2)
# print parse_file('test/test2.txt', 3, 2)
# print parse_file('test/test3.txt', 3, 3)
# print parse_file('test/test4.txt', 10, 15)
# print parse_file('test/test5.txt', 20, 35)
# print parse_file('test/test6.txt', 200, 350)
# print parse_file('test/test7.txt', 500, 500)

np.random.seed(0)


# for method in ['first', 'smart', 'random', 'dumb']:
for method in ['random', 'dumb']:
	np.random.seed(0)
	print 'Method', method
	for size in ((x, 100) for x in range(500, 10500, 500)):
		total_pivots = 0
		for trial in range(25):
			_, _, num_pivots = test_random(*size)
			total_pivots += num_pivots
			# print size, num_pivots

		# print 'avg', size, (total_pivots / 10.0)
		print size[0], ',', (total_pivots / 10.0)

# for size in ((100, x) for x in range(2000, 11000, 1000)):
# 	total_pivots = 0
# 	for trial in range(25):
# 		_, _, num_pivots = test_random(*size)
# 		total_pivots += num_pivots
# 		# print size, num_pivots

# 	print 'avg', size, (total_pivots / 10.0)

# print test_random(5000, 3500)
# print test_random(5000, 3500)
# print test_random(5000, 3500)
# print test_random(5000, 3500)
# print test_random(5000, 3500)
