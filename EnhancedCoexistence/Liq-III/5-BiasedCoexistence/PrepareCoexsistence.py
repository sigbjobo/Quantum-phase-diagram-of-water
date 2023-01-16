#!/usr/bin/env python
# coding: utf-8

# # Preparation of biased coexsistence simulations

# In[2]:


import numpy as np, sys, os, glob
import matplotlib.pylab as plt
import MDAnalysis


# In[29]:


standard_sim=os.path.abspath('230K-3000atm')
sims={}
for sim in glob.glob('../4-PrepareCoexistenceConfiguration/COEX_BOXES/*.data'):
    sims[sim]={}
    fn=sim.split('/')[-1].replace('.data','')
    print(fn)
    P_n=fn.split('_')[0]
    T_n=fn.split('_')[1]
    T=T_n.strip('K')
    P=P_n.strip('atm')
    
    fold='COEX_'+P_n+'/'+T_n+'/'
    cmd='mkdir -p {}\n'.format(fold)
    cmd+='cp {}/* {}/\n'.format(standard_sim,fold)
    cmd+='cp {} {}/water.data\n'.format(sim,fold)
    cmd+='sed -i  \"s#variable.*temperature.*#variable        temperature equal {}#g\" {}/in.temp\n'.format(T,fold)
    cmd+='sed -i  \"s#TEMP=REPLACE_TEMP#TEMP={}#g\" {}/plumed*.dat\n'.format(T,fold)
    cmd+='sed -i    \"s#variable .* pressure .*#variable        pressure equal {}#g\" {}/in.pressure'.format(P,fold)
    print(cmd)
    os.system(cmd)
    


# ### Convert notebook to python script

# In[33]:


get_ipython().system('jupyter nbconvert --to script PrepareCoexsistence.ipynb')


# In[ ]:




