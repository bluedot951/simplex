import numpy as np

def testManual():
	A = np.array([[2.,1.,1.,1.,0.,0.],[4.,2.,3.,0.,1.,0.],[2.,5.,5.,0.,0.,1.]])
	b = np.array([[14.,28.,30.]])
	c = np.array([1.,2.,-1.,0.,0.,0.,0.])

	solve(A, b, c, 'min', 'first', True)

	A = np.array([[1., 1., 1., 0., 0.], [2., 1., 0., 1., 0.], [1., 2., 0., 0., 1.]])
	b = np.array([[8., 12., 14.]])
	c = np.array([2., 3., 0., 0., 0., 0.])

	solve(A, b, c, 'min', 'first', True)

	A = np.array([[1., 1.], [2., 1.]])
	b = np.array([[4., 5.]])
	c = np.array([3., 4.])

	solve(A, b, c, 'min', 'first', True)

	A = np.array([[1., 2., 1.], [3., 1., 1.], [1., 1., 2.], [1., 1., 1.]])
	b = np.array([[2., 4., 4., 2.]])
	c = np.array([1., 2., 1.])

	solve(A, b, c, 'min', 'first', True)


def slack(A, c):
	m, _ = A.shape
	A = np.hstack((A,np.identity(m)))
	c = np.hstack((c, np.zeros(m+1)))
	return A, c

def solve(A, b, c, op, pivot, addSlack):
	if op == 'min':
		c = -1*c

	_, n = A.shape
	if addSlack:
		A, c = slack(A, c)

	soln = np.zeros(n)

	Ab = np.hstack((A,b.T))
	Abc = np.vstack((Ab,c))

	idx = np.where(Abc[-1] > 0)[0]
	prevObj = None
	num_pivots = 0
	while len(idx) > 0:
		num_pivots += 1

		if pivot == 'first':
			i = idx[0]
		elif pivot == 'random':
			i = np.random.choice(idx)
		elif pivot == 'smart':
			minPivot = 0
			i = -1
			for index in idx:
				coeffs = np.divide(Abc[:,-1], Abc[:,index], out=np.full(Abc.shape[0], np.inf), where=Abc[:,index]!=0)
				coeffs[coeffs < 0] = np.inf
				minVal = np.amin(coeffs[:-1])
				if minVal > minPivot:
					minPivot = minVal
					i = index
		elif pivot == 'dumb':
			minPivot = np.inf
			i = -1
			for index in idx:
				coeffs = np.divide(Abc[:,-1], Abc[:,index], out=np.full(Abc.shape[0], np.inf), where=Abc[:,index]!=0)
				coeffs[coeffs < 0] = np.inf
				minVal = np.amin(coeffs[:-1])
				if minVal < minPivot:
					minPivot = minVal
					i = index
		else:
			print "No pivot rule", pivot
			exit()

		coeffs = np.divide(Abc[:,-1], Abc[:,i], out=np.full(Abc.shape[0], np.inf), where=Abc[:,i]!=0)
		coeffs[coeffs < 0] = np.inf

		assert len(np.where(coeffs != np.inf)[0]) > 0

		j = np.argmin(coeffs[:-1])
		Abc[j] = 1/Abc[j,i]*Abc[j]

		oldAbc = np.copy(Abc)
		for k in range(Abc.shape[0]):
			if k==j: continue
			Abc[k] = oldAbc[k] - oldAbc[k,i]*oldAbc[j]

		idx = np.where(Abc[-1] > 0)[0]

		prevObj = Abc[-1,-1]

	UL = Abc[:-1, :-1]
	for i in range(UL.shape[1] - UL.shape[0]):
		nz = np.nonzero(UL[:, i])[0]
		if len(nz) == 1:
			soln[i] = Abc[nz[0], -1] / Abc[nz[0], i]

	optVal = Abc[-1,-1]

	if op == 'max':
		optVal = -1*optVal 
	
	return optVal, soln, num_pivots