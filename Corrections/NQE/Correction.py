import numpy as np
import sys
import os


deepmd = np.loadtxt(sys.argv[1]+'/simulation.kin')
N = int(int(os.popen('head -n1 {}/water.xyz'.format(sys.argv[1])).read())//3)

deepmd = deepmd[int(len(deepmd)//5):][:,1]/N*27.2114*1000 # to meV


n=4

print(deepmd.mean(),np.std([ai.mean() for ai in np.split(deepmd[:int(n*(len(deepmd)//n))], n)])*1.96)

exit()
