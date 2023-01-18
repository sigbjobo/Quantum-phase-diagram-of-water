import sys
import MDAnalysis

u = MDAnalysis.Universe('water.pdb',dt='ps',in_memory=True)

masses=u.atoms.masses
y =float(sys.argv[1])
fac_hydrogen=1
if len(sys.argv)>2:
    masses[1::3]=0*masses[1::3]+float(sys.argv[2])
    masses[2::3]=0*masses[2::3]+float(sys.argv[2])

print(', '.join([str(l) for l in masses/(y**2)]))
