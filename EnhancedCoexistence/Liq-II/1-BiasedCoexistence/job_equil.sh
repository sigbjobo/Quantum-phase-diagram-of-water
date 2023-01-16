#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16# <- match to OMP_NUM_THREADS, 64 requests whole node
#SBATCH --partition=gpuA100x8# <- one of: gpuA100x4 gpuA40x4 gpuA100x8 gpuMI100x8
#SBATCH --account=bblh-delta-gpu
#SBATCH --job-name=EQUIL

### GPU options ###
#SBATCH --gpus=1
##SBATCH --gpus-per-node=1
#SBATCH --gpus-per-task=1
#SBATCH --gpu-bind=verbose,per_task:1
#SBATCH -t 0:30:00


cd $SLURM_SUBMIT_DIR

source ~/env/lmp_deepmd.sh
export PLUMED_NUM_THREADS=16
export OMP_NUM_THREADS=12
export TF_INTRA_OP_PARALLELISM_THREADS=2
export TF_INTER_OP_PARALLELISM_THREADS=2
export SLURM_CPU_BIND="cores"

export cycles=100





if [ -e restart.lmp.0 ] ; then
    if [ -s restart.lmp.0 ]; then
	echo restart.lmp.0 exists
    else
	echo restart.lmp.0 does not exists, copying restart2.lmp.0
	cp  restart2.lmp.0 restart.lmp.0
    fi

    nn=`tail -n 1 runno | awk '{print $1}'`
    srun $LAMMPS_EXE -in Restart.lmp
else
    nn=1
    srun $LAMMPS_EXE  -in start.lmp
fi

# set +e

# for j in $(seq 0 0)
# do
#     cp log.lammps log.lammps.${j}.${nn}
#     cp restart2.lmp.${j} restart2.lmp.${j}.${nn}
#     cp restart.lmp.${j} restart.lmp.${j}.${nn}
#     cp data.final.${j} data.final.${j}.${nn}
# done



# mm=$((nn+1))
# echo ${mm} > runno



# if [ ${nn} -ge ${cycles} ]; then
#   exit
# fi

# NUM_DONE=$(grep TIMESTEP -A1 dump.water.0 | tail -n1)
# NWALL=$(grep nsteps_wall procedure.lmp|head -n1 | grep equal |awk '{print $4}')
# NCOEX=$(grep nsteps_enhanced_coex procedure.lmp|head -n1 | grep equal |awk '{print $4}')
# let NUM_STOP=$NWALL+$NCOEX
# if [ ${NUM_DONE} -ge ${NUM_STOP} ]; then
#   exit
# fi

# sbatch --job-name="$SBATCH_JOB_NAME"  /projects/bblh/sigbjobo/PhaseDiagram/job.sh
