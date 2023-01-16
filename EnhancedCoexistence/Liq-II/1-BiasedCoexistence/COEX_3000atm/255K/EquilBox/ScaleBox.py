import MDAnalysis
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
    #data['time_ps']=dt*data['step']/1000
    return data


# Read ice
u = MDAnalysis.Universe(sys.argv[1], in_memory=True)    
data=extract_form_log(sys.argv[2])

# Determine average box
last=len(data['cella'])//10
dimensions_new=[data['cella'][last:].mean(),data['cellb'][last:].mean(),data['cellc'][last:].mean(),data['cellalpha'][last:].mean(),data['cellbeta'][last:].mean(),data['cellgamma'][last:].mean()]

# Set new box size
max_dim=['x','y','z'].index(sys.argv[3])
#max_dim=np.where(u.dimensions==max_l)[0][0]
dimensions_new[max_dim]=u.dimensions[max_dim]
print(dimensions_new)
# Scaled coordinates
scaled_coord=MDAnalysis.lib.distances.transform_RtoS(u.atoms.positions,u.dimensions)

# Scale coordinates and box size
dimensions_new[max_dim]=u.dimensions[max_dim]
u.dimensions=dimensions_new
u.atoms.positions=MDAnalysis.lib.distances.transform_StoR(scaled_coord,u.dimensions)

# Store ice
u.atoms.write(sys.argv[1].replace('.data','_scaled.data'))
