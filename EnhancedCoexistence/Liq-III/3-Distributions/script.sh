#module purge
#module load rh/devtoolset/4
#module load openmpi/gcc/3.1.3/64

#source /home/ppiaggi/Programs/Software-deepmd-kit-1.0/plumed2-git/sourceme.sh

for i in `seq 0.05 0.01 0.05`
do
        for phase in IceV Liquid
        do
                cd $phase
                sed "s/replace/$i/g" plumed-base.dat > plumed.dat
                timeout 60 plumed --no-mpi driver --plumed plumed.dat --mf_dcd dump.dcd > /dev/null
                cd ../
        done
        result=`python script.py`
        echo $i $result
        #gnuplot plot.gpi
        for phase in IceV Liquid
        do
                cd $phase
                rm COLVAR histo* analysis.*
                cd ../
        done
done
