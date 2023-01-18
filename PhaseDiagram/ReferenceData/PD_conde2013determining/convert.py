# read files using sys.argv

import sys
import numpy as np
# read file using sys.argv
files = sys.argv[1:]

for fn in files:
    data = np.loadtxt(fn)

    # Convert y data from bar to GPa
    data[:, 1] = data[:, 1]*0.0001

    np.savetxt(fn, data, fmt='%10.5f')
