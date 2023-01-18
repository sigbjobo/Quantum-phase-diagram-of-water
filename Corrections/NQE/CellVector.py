import sys
import MDAnalysis

u = MDAnalysis.Universe('water.pdb',dt='ps')
print(', '.join([str(l) for l in MDAnalysis.lib.mdamath.triclinic_vectors(u.dimensions).flatten()]))
