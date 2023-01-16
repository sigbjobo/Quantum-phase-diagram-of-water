import MDAnalysis
import sys


u = MDAnalysis.Universe(sys.argv[1])
u.add_TopologyAttr('names',['O','H','H']*int(len(u.atoms)//3))
u.atoms[::3].write('ox.pdb')
u.atoms[:].write('ox_hy.pdb')

with open('names.pdb','w') as fp_out, open('ox.pdb','r') as fp_1, open('ox_hy.pdb','r') as fp_2 :
    lines1=fp_1.readlines()[2:-1]
    lines2=fp_2.readlines()[2:-1]

    lines=lines1+lines2
    for l in lines:
        fp_out.write(l)
