# This script creates an ice VI configuration using GenIce.
for i in `seq 1 1`
do
	echo $i
	genice --rep 8 4 4 VI --format g --seed $RANDOM > iceVI.gro
	vmd -dispdev none -e script-vmd.tcl
done
