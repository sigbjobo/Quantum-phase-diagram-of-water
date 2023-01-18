import numpy as np
import sys
import os

deepmd = np.loadtxt(sys.argv[1])
mbpol = np.loadtxt(sys.argv[2])


N=int(sys.argv[3])
T=float(sys.argv[4])
steps, index_deepmd, index_mbpol = np.intersect1d(deepmd[:,0], mbpol[:,0], assume_unique=True, return_indices=True)

conv_fac=1000.0/23.060542

deepmd=deepmd[index_deepmd][:,1]
mbpol=mbpol[index_mbpol][:,1]

#kt=8.617333262E-5*T # eV
kt=2.479/298.*T
n=4

A = np.split(deepmd[:int(n*(len(deepmd)//n))], n)
B = np.split(mbpol[:int(n*(len(mbpol)//n))], n)
mean=-kt/N*np.log(np.mean(np.exp(-N*(mbpol-deepmd)/kt)))

chem_pot=[]
for i in range(n):
    chem_pot.append(-kt/N*np.log(np.mean(np.exp(-N*(B[i]-A[i])/kt))))
    
print(mean*conv_fac,np.std(chem_pot)*1.96*conv_fac)

exit()
