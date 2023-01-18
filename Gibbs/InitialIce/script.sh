genice --rep 3 3 2 Ih --format g --seed $RANDOM > ice.gro
vmd -dispdev none -e script-vmd.tcl
cp ice.data IceIh.data

genice --rep 3 3 4 II --format g --seed $RANDOM > ice.gro
vmd -dispdev none -e script-vmd.tcl
cp ice.data IceII.data

genice --rep 3 3 3 III --format g --seed $RANDOM > ice.gro
vmd -dispdev none -e script-vmd.tcl
cp ice.data IceIII.data

genice --rep 3 3 2 V --format g --seed $RANDOM > ice.gro
vmd -dispdev none -e script-vmd.tcl
cp ice.data IceV.data

genice --rep 4 4 4 VI --format g --seed $RANDOM > ice.gro
vmd -dispdev none -e script-vmd.tcl
cp ice.data IceVI.data

rm ice.data ice.gro
