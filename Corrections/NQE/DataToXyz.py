import numpy as np
import MDAnalysis
import sys

u = MDAnalysis.Universe(sys.argv[1],format='DATA',in_memory=True,dt='ps')

u.add_TopologyAttr('names',['O','H','H']*int(len(u.atoms)//3))
u.add_TopologyAttr('types',['O','H','H']*int(len(u.atoms)//3))

u.atoms.write(sys.argv[2])
