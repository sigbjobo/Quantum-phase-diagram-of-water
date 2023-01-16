natoms=$(grep atoms ice_final.data | awk '{print $1}')
sed -i "s/SPECIESA=.*/SPECIESA=1-${natoms}:3/g" plumed.order.dat
sed -i "s/SPECIESB=.*/SPECIESB=1-${natoms}/g" plumed.order.dat
sed -i "s/SPECIES=.*/SPECIES=1-${natoms}:3/g" plumed.order.dat

let natoms=${natoms}*2
sed -i "s/SPECIESA=.*/SPECIESA=1-${natoms}:3/g" ../plumed.order.dat
sed -i "s/SPECIESB=.*/SPECIESB=1-${natoms}/g" ../plumed.order.dat
sed -i "s/SPECIES=.*/SPECIES=1-${natoms}:3/g" ../plumed.order.dat


