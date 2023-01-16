import numpy as np
import sys, os

overlap=np.genfromtxt('overlap.txt')
sigma=overlap[np.where(overlap[:,1]==overlap[:,1].min())[0][0],0]
print(sigma)
hist_liquid=np.loadtxt('histo_liq_{}'.format(sigma))
hist_ice=np.loadtxt('histo_ice_{}'.format(sigma))

max_liq=hist_liquid[hist_liquid[:,1]==hist_liquid[:,1].max()][0][0]
max_ice=hist_ice[hist_ice[:,1]==hist_ice[:,1].max()][0][0]

diff_bin = hist_liquid[:,0]
diff_val = np.abs(hist_liquid[:,1]-hist_ice[:,1])
diff_val = diff_val[(diff_bin>max_liq) * (diff_bin<max_ice)]
diff_bin = diff_bin[(diff_bin>max_liq) * (diff_bin<max_ice)]
min_order= diff_bin[diff_val.min()==diff_val][0]

print("Liquid max:",max_liq)
print("Ice max:",max_ice)
print("Midpoint:",min_order)


os.system('sed -i \'s/MORE_THAN1=.*/MORE_THAN1={{CUBIC D_0={} D_MAX={}}}/g\' ../plumed.order.dat'.format(max_liq,max_ice))
os.system('sed -i \'s/MORE_THAN2=.*/MORE_THAN2={{CUBIC D_0={} D_MAX={}}}/g\' ../plumed.order.dat'.format(min_order,min_order+0.0001))

os.system('python3 SetSigma.py {} {}'.format(sigma,'../plumed.order.dat'))
os.system('cd ../;  python3 EquilBox/MakeNames.py water.data')
