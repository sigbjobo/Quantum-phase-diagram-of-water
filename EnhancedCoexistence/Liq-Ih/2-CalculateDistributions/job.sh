 

unset PLUMED_KERNEL
unset PLUMED_ROOT     
unset PLUMED_VIMPATH

export OMP_NUM_THREADS=20
export PLUMED_NUM_THREADS=20

pwd; hostname; date

#module purge                                                                                                                                                                                                      

ice=Ih
folder=../1-Bulk/
for j in 2000atm_240K
do

    rm -rf Ice${ice}_$j #I_$j Liquid_$j                                                                                                                                                                                
    cp -r Ice${ice} Ice${ice}_$j
    cp ${folder}/Ice${ice}_$j/dump.water.0 Ice${ice}_$j/
    cp -r Liquid Liquid_$j
    cp ${folder}/Liquid_$j/dump.water.0 Liquid_$j/
    rm -rf overlap_$j.dat
    for i in `seq 0.04 0.0025 0.10`
    do
        for phase in Ice${ice}_$j Liquid_$j
        do
            cd $phase
            sed "s/replace/$i/g" plumed-base.dat > plumed.dat
	    NSTEPS=$(grep -A1 TIMESTEP dump.water.0  | tail -n1)
	    sed -i "s/REPLACE_NSTEPS/$NSTEPS/g" plumed.dat 

            ~/software/miniconda3/envs/deepmd2.1.1/bin/lmp -in start.lmp -screen none
            cd ../
        done
        result=`python script.py $j`
        echo $i $result >>overlap_$j.dat
        for phase in Ice${ice}_$j Liquid_$j
        do
            cd $phase
            cp histo Histo_$i
            cp COLVAR COLVAR_$i
            rm COLVAR *histo*
            cd ../
        done
    done
done
