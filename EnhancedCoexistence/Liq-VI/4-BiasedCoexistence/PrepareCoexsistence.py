#!/usr/bin/env python
# coding: utf-8

# # Preparation of biased coexsistence simulations

# In[1]:


import numpy as np, sys, os, glob
import matplotlib.pylab as plt
import MDAnalysis


# In[2]:


standard_sim=os.path.abspath('template/')

press_box = np.genfromtxt('../4-PrepareCoexistenceConfiguration/avg_ice_box.dat')
print(press_box)
presures=np.unique(press_box[:,0])


# In[4]:


sims = dict()
for a in press_box[:]:
    fold='COEX_{}atm/{}K/'.format(a[0],a[1])
    os.system('mkdir -p {}'.format(fold))
    os.system('cp {}/* {}'.format(standard_sim,fold))
    sims[fold] = dict()
    p=a[0]
    t=a[1]
    
    cmd ='sed -i  \"s#REPLACE_PRESSURE#{}#g\" {}/in.pressure\n'.format(p,fold)
    cmd+='sed -i  \"s#REPLACE_TEMP#{}#g\" {}/in.temp\n'.format(t,fold)
    cmd+='sed -i  \"s#REPLACE_TEMP#{}#g\" {}/plumed*.dat'.format(t,fold)
    os.system(cmd)
    u = MDAnalysis.Universe('template/water.data', in_memory=True)
    print('before',u.dimensions)
    dimensions_new=a[2:]
    max_l=np.max(u.dimensions[:3])
    max_dim=np.where(u.dimensions==max_l)[0][0]
    dimensions_new[max_dim]=u.dimensions[max_dim]
    for dim in range(3):
        if not dim==max_dim:
            u.coord.positions[:,dim] = u.coord.positions[:,dim]*dimensions_new[dim]/u.dimensions[dim]
    u.dimensions=dimensions_new
    print('after',u.dimensions)

    u.atoms.write(fold+'/water.data')


# ### Convert notebook to python script

# In[11]:


get_ipython().system('jupyter nbconvert --to script PrepareCoexsistence.ipynb')


# In[ ]:




