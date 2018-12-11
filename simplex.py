import numpy as np

A = np.array([[2.,1.,1.,1.,0.,0.],[4.,2.,3.,0.,1.,0.],[2.,5.,5.,0.,0.,1.]])
b = np.array([[14.,28.,30.]])
c = np.array([1.,2.,-1.,0.,0.,0.,0.])

Ab = np.hstack((A,b.T))

i = 1
j = 2

print '1'
print Ab
print c

# b[j] = 1/A[j,i]*b[j]
Ab[j] = 1/Ab[j,i]*Ab[j]

print '2'
print Ab
print c

for k in range(A.shape[0]):
	if k==j: continue
	Ab[k] = Ab[k] - Ab[k,i]*Ab[j]
c = c - c[i]*Ab[j]

print '3'
print Ab
print c

i = 0
j = 1

print '1'
print Ab
print c

# b[j] = 1/A[j,i]*b[j]
Ab[j] = 1/Ab[j,i]*Ab[j]

print '2'
print Ab
print c

for k in range(A.shape[0]):
	if k==j: continue
	Ab[k] = Ab[k] - Ab[k,i]*Ab[j]
c = c - c[i]*Ab[j]

print '3'
print Ab
print c