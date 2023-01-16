#!/usr/bin/env python
# coding: utf-8

# # Prepare simulations

# In[ ]:


import numpy as np
import matplotlib.pylab as plt
import os, sys


# In[ ]:


sims={}
sims['2000']=[250,255,260,265,270]
sims['4000']=[250,255,260,265,270]
sims['6000']=[255,260,265,270,275]
sims['8000']=[255,260,265,270,275]


# ### Make simulation folders

# In[ ]:


for p in sims.keys():
   # pbar=P_bar[i]
    for t in sims[p]:
        fold='IceIII_{}atm_{}K'.format(p,t)
        os.system('cp -r IceIII {}'.format(fold))
        cmd='sed -i  "s#variable .* pressure .*#variable        pressure equal {}#g" {}/in.pressure\n'.format(p,fold)
        cmd+='sed -i  "s#variable.*temperature equal.*#variable        temperature equal {}#g" {}/in.temp'.format(t,fold)
        os.system(cmd)


# In[1]:


get_ipython().system('jupyter nbconvert --to script PrepareCoexistence.ipynb')


# In[ ]:




