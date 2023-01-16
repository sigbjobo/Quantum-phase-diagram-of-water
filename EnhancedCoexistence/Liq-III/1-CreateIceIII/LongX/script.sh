# This script creates an ice III configuration using GenIce.
# The configuration is converted into a lammps data file
# suitable for TIP4P using VMD
genice --rep 7 3 3 III --format g --seed $RANDOM > iceIII.gro
vmd -dispdev none -e script-vmd.tcl
