import MDAnalysis
import MDAnalysis.transformations
import sys, numpy as np


def extract_form_log(fn):
    lines=open(fn,'r').readlines()
    start=np.where([('Step' in l) for l in lines])[-1][0]
    data={keyi.lower(): []  for keyi in lines[start].split()}
    for l in lines[start+1:]:
        ls=l.split()
        if ls[0].isdigit():
            for i, key in enumerate(data.keys()):
                data[key].append(float(ls[i]))
        else:
            break
    
    for key in data.keys():
        data[key]=np.array(data[key])

    return data

offset=3.0
mobile=3.0
# Read ice
u1 = MDAnalysis.Universe(sys.argv[1], in_memory=True)    
u2 = MDAnalysis.Universe(sys.argv[2], in_memory=True)


# Create bonds to unwrap coordinates
bonds = []
for o in range(0, len(u1.atoms), 3):
    bonds.extend([(o, o+1), (o, o+2)])
u1.add_TopologyAttr('bonds', bonds)
transform = MDAnalysis.transformations.unwrap(u1.atoms)
u1.trajectory.add_transformations(transform)
u1.add_TopologyAttr('bonds', [])

u2.add_TopologyAttr('bonds', bonds)
transform = MDAnalysis.transformations.unwrap(u2.atoms)
u2.trajectory.add_transformations(transform)

u2.add_TopologyAttr('bonds', [])


# Save original box dimensions
u1_dim_orig=u1.dimensions
u2_dim_orig=u2.dimensions

# Find dimensions not matching between the two boxes
dim_l=np.where( (u1.dimensions!=u2.dimensions))[0][0]

# Translate ice box
translation=MDAnalysis.lib.mdamath.triclinic_vectors(u1.dimensions)[dim_l]

# Correct for skewness to make offset extra long box in perp direction
#offset=offset*np.linalg.norm(translation)/translation[dim_l]


u2.atoms.positions+=translation +offset*translation/np.linalg.norm(translation)
u2.dimensions[dim_l]=u1.dimensions[dim_l]+u2.dimensions[dim_l]+2*offset

# Merge the two boxes
u = MDAnalysis.Merge(u1.atoms, u2.atoms)
u.dimensions=u2.dimensions

# Size of box1 in scaled coordinates
l1=u1_dim_orig[dim_l]/u2.dimensions[dim_l]

# How much to shift ice box
offset_scaled=offset/u2.dimensions[dim_l]

# Threshold for counting as liquid surface
mobile_scaled=mobile/u2.dimensions[dim_l]

# Scaled coordinates
scaled_coord=MDAnalysis.lib.distances.transform_RtoS(u.atoms.positions,u.dimensions)[:,dim_l]

# Atoms to be thermostatted
mobile=(scaled_coord<mobile_scaled)+(scaled_coord>l1-mobile_scaled)*(scaled_coord<l1+offset_scaled*0.5)

# Liquid atoms to remain imobile during simulation
rigid1=(scaled_coord>mobile_scaled)*(scaled_coord<l1-mobile_scaled)

# Ice atoms to remain rigid, but moved towards liquid
rigid2=(scaled_coord>l1+offset_scaled/2)
print(sum(mobile),sum(rigid1),sum(rigid2))
# Store as three seprate LAMMPS data files
u.atoms[mobile].write('mobile.data')
u.atoms[rigid1].write('rigid1.data')
u.atoms[rigid2].write('rigid2.data')
 
