if [ -s DELTAFS ]
then
    cp plumed.restart.dat plumed.dat
else
    cp plumed.start.dat plumed.dat
fi
