import numpy as np

# A = np.array([[2.,1.,1.,1.,0.,0.],[4.,2.,3.,0.,1.,0.],[2.,5.,5.,0.,0.,1.]])
# b = np.array([[14.,28.,30.]])
# c = np.array([1.,2.,-1.,0.,0.,0.,0.])

# A = np.array([[1., 1., 1., 0., 0.], [2., 1., 0., 1., 0.], [1., 2., 0., 0., 1.]])
# b = np.array([[8., 12., 14.]])
# c = np.array([2., 3., 0., 0., 0., 0.])

# A = np.array([[1., 1.], [2., 1.]])
# b = np.array([[4., 5.]])
# c = np.array([3., 4.])

A = np.array([[1., 2., 1.], [3., 1., 1.], [1., 1., 2.], [1., 1., 1.]])
b = np.array([[2., 4., 4., 2.]])
c = np.array([1., 2., 1.])

def slack(A, c):
	m, _ = A.shape
	A = np.hstack((A,np.identity(m)))
	c = np.hstack((c, np.zeros(m+1)))
	return A, c


def solve(A, b, c, op, pivot):

	if op == 'min':
		c = -1*c

	_, n = A.shape
	A, c = slack(A, c)

	# soln = np.zeros(c.shape)
	soln = np.zeros(n)

	Ab = np.hstack((A,b.T))
	Abc = np.vstack((Ab,c))

	print 'Abc', Abc

	idx = np.where(Abc[-1] > 0)[0]
	print idx
	prevObj = None
	while len(idx) > 0:
		print '=================', idx

		if pivot == 'first':
			i = idx[0]
		elif pivot == 'random':
			i = np.random.choice(idx)
		else:
			minPivot = 0
			i = -1
			for index in idx:
				print 'index', index
				coeffs = np.divide(Abc[:,-1], Abc[:,index], out=np.full(Abc.shape[0], np.inf), where=Abc[:,index]!=0)
				coeffs[coeffs < 0] = np.inf
				minVal = np.amin(coeffs[:-1])
				if minVal > minPivot:
					minPivot = minVal
					i = index
					print 'i', i

		print i
		coeffs = np.divide(Abc[:,-1], Abc[:,i], out=np.full(Abc.shape[0], np.inf), where=Abc[:,i]!=0)
		coeffs[coeffs < 0] = np.inf

		assert len(np.where(coeffs != np.inf)[0]) > 0

		# coeffs = Abc[:,-1]/Abc[:,i]
		j = np.argmin(coeffs[:-1])
		print j
		Abc[j] = 1/Abc[j,i]*Abc[j]

		oldAbc = np.copy(Abc)
		for k in range(Abc.shape[0]):
			if k==j: continue
			Abc[k] = oldAbc[k] - oldAbc[k,i]*oldAbc[j]
		print Abc
		idx = np.where(Abc[-1] > 0)[0]

		if prevObj is not None and prevObj == Abc[-1,-1]:
			print 'exit loop'
			break
		prevObj = Abc[-1,-1]

		# 1/0

	UL = Abc[:-1, :-1]
	for i in range(UL.shape[1] - UL.shape[0]):
		nz = np.nonzero(UL[:, i])[0]
		print nz
		if len(nz) == 1:
			print Abc[nz[0], -1], Abc[nz[0], i]
			soln[i] = Abc[nz[0], -1] / Abc[nz[0], i]
		print '---'

	optVal = Abc[-1,-1]

	if op == 'max':
		optVal = -1*optVal 
	
	return optVal, soln

out = solve(A,b,c,'max','a')
print 'sol: ', out

# i = 1
# j = 2

# print '1'

# Abc[j] = 1/Abc[j,i]*Abc[j]

# print '2'
# print Abc

# oldAbc = np.copy(Abc)
# for k in range(Abc.shape[0]):
# 	if k==j: continue
# 	Abc[k] = oldAbc[k] - oldAbc[k,i]*oldAbc[j]

# print '3'
# print Abc

# i = 0
# j = 1

# print '1'
# print Abc

# Abc[j] = 1/Abc[j,i]*Abc[j]

# print '2'
# print Abc

# oldAbc = np.copy(Abc)
# for k in range(Abc.shape[0]):
# 	if k==j: continue
# 	Abc[k] = oldAbc[k] - oldAbc[k,i]*oldAbc[j]

# print '3'
# print Abc