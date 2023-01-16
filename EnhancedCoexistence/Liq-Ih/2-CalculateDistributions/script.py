import numpy as np
import sys
data1=np.genfromtxt("IceIh_{}/histo".format(sys.argv[1]))
data2=np.genfromtxt("Liquid_{}/histo".format(sys.argv[1]))
print(np.trapz(np.minimum(data1[:,1],data2[:,1]),x=data1[:,0]))

