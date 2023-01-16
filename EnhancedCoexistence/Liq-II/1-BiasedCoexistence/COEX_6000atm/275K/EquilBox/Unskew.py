import os
import subprocess
  
import MDAnalysis

u=MDAnalysis.Universe('ice_liq_coex.data',in_memory=True)
u.atoms.write('ice_liq_coex.pdb')
sp = subprocess.Popen(["/bin/bash", "-i", "-c",' atomsk ice_liq_coex.pdb -unskew -wrap -ow pdb '])
sp.communicate()

u2=MDAnalysis.Universe('ice_liq_coex.pdb',format='pdb')
u.dimensions=u2.dimensions
u.atoms.positions=u2.atoms.positions
u.atoms.write('ice_liq_coex_unskewed.data')



