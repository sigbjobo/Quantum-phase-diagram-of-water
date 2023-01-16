import numpy as np
import sys
data1=np.genfromtxt(sys.argv[2])
data2=np.genfromtxt(sys.argv[3])
print(sys.argv[1],np.trapz(np.minimum(data1[:,1],data2[:,1]),x=data1[:,0]))

