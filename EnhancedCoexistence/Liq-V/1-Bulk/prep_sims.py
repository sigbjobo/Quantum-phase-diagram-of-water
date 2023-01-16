#!/usr/bin/env python
# coding: utf-8

# # Prepare simulations

# In[2]:


import numpy as np
import os, sys


# ### Pressure values for simulations

# In[3]:


# Pressures in mpa
#P_mpa=np.round(np.linspace(0.1,200,11),1)

# Pressures in bar
P_bar=[3500,4000,5000,6000,7000] #np.round(P_mpa*10,0)
for p in P_bar:
    print(p)


# ### Make simulation folders

# In[4]:


for i, pbar in enumerate(P_bar):
    pbar=P_bar[i]
    fold='IceV_{}bar'.format(pbar)
    os.system('cp -r IceV {}'.format(fold))
    cmd='sed -i "" "s#variable .* pressure .*#variable        pressure equal {}#g" {}/in.pressure'.format(pbar,fold)
    os.system(cmd)
for i, pbar in enumerate(P_bar):
    pbar=P_bar[i]
    fold='Liquid_{}bar'.format(pbar)
    os.system('cp -r Liquid {}'.format(fold))
    cmd='sed -i "" "s#variable .* pressure .*#variable        pressure equal {}#g" {}/in.pressure'.format(pbar,fold)
    os.system(cmd)


# 

# In[3]:


get_ipython().system('jupyter nbconvert --to script prep_sims.ipynb')


# In[ ]:




