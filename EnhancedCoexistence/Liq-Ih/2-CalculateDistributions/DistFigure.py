#!/usr/bin/env python
# coding: utf-8

# # Distribution of order parameter

# In[1]:


import numpy as np
import matplotlib.pylab as plt
import matplotlib as mpl
 
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
dists=dict()



# IceIh-Liquid
dists['IceIh-Liquid']=dict()
dists['IceIh-Liquid']['mid']=0.7275
dists['IceIh-Liquid']['name']='Ice Ih'
dists['IceIh-Liquid']['hist-Liq']=np.loadtxt('../../IceIh-Liquid/2-CalculateDistributions/Liquid/histo')
dists['IceIh-Liquid']['hist_ice']=np.loadtxt('../../IceIh-Liquid/2-CalculateDistributions/IceIh/histo')
dists['IceIh-Liquid']['sigma']=np.loadtxt('../../IceIh-Liquid/2-CalculateDistributions/results.txt')
dists['IceIh-Liquid']['xlim']=(0.35,1.1)

# IceII-Liquid
dists['IceII-Liquid']=dict()
dists['IceII-Liquid']['mid']=0.96
dists['IceII-Liquid']['sigma']=0.0775
dists['IceII-Liquid']['name']='Ice II'
dists['IceII-Liquid']['hist-Liq']=np.loadtxt('../../IceII-Liquid/3-Distributions/Liquid_2000atm/Histo_0.0775')
dists['IceII-Liquid']['hist_ice']=np.loadtxt('../../IceII-Liquid/3-Distributions/IceII_2000atm/Histo_0.0775')
dists['IceII-Liquid']['sigma']=np.loadtxt('../../IceII-Liquid/3-Distributions/overlap_1000atm.dat')

dists['IceII-Liquid']['xlim']=(0.65,1.2)

# IceIII-Liquid
dists['IceIII-Liquid']=dict()
dists['IceIII-Liquid']['mid']=0.7675
dists['IceIII-Liquid']['sigma']=0.0675
dists['IceIII-Liquid']['name']='Ice III'
dists['IceIII-Liquid']['hist-Liq']=np.loadtxt('../../IceIII-Liquid/3-Distributions/Liquid_4000bar/Histo_0.0675')
dists['IceIII-Liquid']['hist_ice']=np.loadtxt('../../IceIII-Liquid/3-Distributions/IceIII_4000bar/Histo_0.0675')
dists['IceIII-Liquid']['sigma']=np.loadtxt('../../IceIII-Liquid/3-Distributions/results.txt')

dists['IceIII-Liquid']['xlim']=(0.45,1.1)

# IceV-Liquid
dists['IceV-Liquid']=dict()
dists['IceV-Liquid']['mid']=0.875
dists['IceV-Liquid']['sigma']=0.0725
dists['IceV-Liquid']['name']='Ice V'
dists['IceV-Liquid']['hist-Liq']=np.loadtxt('../../IceV-Liquid/2-CalculateDistributions/Liquid/histo')
dists['IceV-Liquid']['hist_ice']=np.loadtxt('../../IceV-Liquid/2-CalculateDistributions/IceV/histo')
dists['IceV-Liquid']['sigma']=np.loadtxt('../../IceV-Liquid/2-CalculateDistributions/results.txt')

dists['IceV-Liquid']['xlim']=(0.55,1.15)

# IceVI-Liquid
dists['IceVI-Liquid']=dict()
dists['IceVI-Liquid']['mid']=0.73
dists['IceVI-Liquid']['sigma']=0.0575
dists['IceVI-Liquid']['name']='Ice VI'
dists['IceVI-Liquid']['hist-Liq']=np.loadtxt('../../IceVI-Liquid/3-Distributions/Liquid/histo')
dists['IceVI-Liquid']['hist_ice']=np.loadtxt('../../IceVI-Liquid/3-Distributions/IceVI/histo')
dists['IceVI-Liquid']['sigma']=np.loadtxt('../../IceVI-Liquid/3-Distributions/results.txt')

dists['IceVI-Liquid']['xlim']=(0.3,1.05)


# In[2]:


plt.figure(figsize=(3.3,2.25))
dist=dists['IceIh-Liquid']
plt.plot(dist['hist-Liq'][:,0],dist['hist-Liq'][:,1],color='b')
plt.fill(dist['hist-Liq'][:,0],dist['hist-Liq'][:,1], color="b",alpha=0.15)
plt.plot(dist['hist_ice'][:,0],dist['hist_ice'][:,1],color='r')
plt.fill(dist['hist_ice'][:,0],dist['hist_ice'][:,1], color="r",alpha=0.15)
plt.xlim(dist['xlim'])
plt.ylim(bottom=0)
#plt.xlabel(r'$k_\chi$')
plt.xlabel(r'Environment similarity index')
plt.ylabel(r'Probability')
#plt.annotate('Liquid',xy=[dist['mid'],0.5*plt.gca().get_ylim()[1]])
#plt.annotate(dist['name'],xy=[dist['mid'],0.5*plt.gca().get_ylim()[1]],rotate=90)
height=plt.gca().get_ylim()[1]
width=plt.gca().get_xlim()[1]-plt.gca().get_xlim()[0]

plt.text(dist['mid']+0.075*width,0.75*height,dist['name'], ha="center", va="center", rotation=90,color='r')
plt.text(dist['mid']-0.075*width,0.75*height,'Liquid', ha="center", va="center", rotation=90,color='b')

#plt.ylabel(r'$P(k_\chi)$')
plt.axvline(x=dist['mid'], color='k', linestyle='--')
plt.tight_layout()
plt.savefig('DistIceIh.png',dpi=300)


# In[3]:


fig, ax=plt.subplots(5,figsize=(3.4,3))
axs=ax.flatten()
for i, key in enumerate(dists.keys()):
    print(key)
    dist=dists[key]
    axs[i].plot(dist['hist-Liq'][:,0],dist['hist-Liq'][:,1],color='b')
    axs[i].fill(dist['hist-Liq'][:,0],dist['hist-Liq'][:,1], color="b",alpha=0.15)
    axs[i].plot(dist['hist_ice'][:,0],dist['hist_ice'][:,1],color='r')
    axs[i].fill(dist['hist_ice'][:,0],dist['hist_ice'][:,1], color="r",alpha=0.15)
    axs[i].set_xlim(dist['xlim'])
    axs[i].set_ylim(bottom=0,top=20)
    axs[i].set_xlim([0.3,1.2])
    height=axs[i].get_ylim()[1]
    width=axs[i].get_xlim()[1]-axs[i].get_xlim()[0]
    dx=0.09
    dy=0.65
    axs[i].set_yticks([0,10])
    axs[i].text(dist['mid']+dx*width,dy*height,dist['name'], ha="center", va="center", rotation=0,color='r')
    axs[i].text(dist['mid']-dx*width,dy*height,'Liquid', ha="center", va="center", rotation=0,color='b')
    axs[i].axvline(x=dist['mid'], color='k', linestyle='--')
    axs[i].set_zorder(5-i)
for i in range(4):
    axs[i].tick_params(axis='x',label1On=False)
plt.xlim([0.3,1.2])
axs[4].set_xlabel(r'Environment similarity kernel')
axs[2].set_ylabel(r'Probability')
plt.tight_layout()

plt.subplots_adjust(top = 0.995, bottom = 0.15, right = 0.95, left = 0.2, 
            hspace = 0, wspace = 0)
plt.savefig('Distributions_alt.png',dpi=300)


# ## Overlap

# In[14]:


from matplotlib.ticker import FormatStrFormatter
fig, ax=plt.subplots(2,3,figsize=(5.5,2.5))
axs=ax.flatten()
#ax.yaxis.set_major_formatter(FormatStrFormatter('%g'))
plt.ticklabel_format(axis='y', style='sci')
for i, key in enumerate(dists.keys()):
    j=i
    if i>1:
        j=i+1
    dist=dists[key]
    sigma=np.array(dist['sigma'])
    axs[j].plot(sigma[:,0],sigma[:,1])
    index=np.where(sigma[:,1].min()==sigma[:,1])[0][0]

    axs[j].scatter(np.atleast_1d(sigma[index,0]),np.atleast_1d(sigma[index,1]),color='r')
    axs[j].set_title(dist['name'],y=1.0, pad=-14)
    axs[j].yaxis.major.formatter.set_powerlimits((0,0))
    

axs[2].set_visible(False)
axs[0].figure
axs[0].figure.text(0.5,-0.04, r'$\sigma$', ha="center", va="center",size=12)
axs[0].figure.text(-0.025,0.5, "Overlap", ha="center", va="center", rotation=90.,size=12)

plt.tight_layout()
plt.savefig('Overlap.png',dpi=300, bbox_inches="tight")


# In[ ]:





# In[ ]:




