#!/bin/bash                                                                                                                                  
#SBATCH --mem=16g
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16     # <- match to OMP_NUM_THREADS, 64 requests whole node
#SBATCH --partition=gpuA100x4 # <- one of: gpuA100x4 gpuA40x4 gpuA100x8 gpuMI100x8
#SBATCH --account=bblh-delta-gpu
#SBATCH --job-name=deepmd
### GPU options ###
#SBATCH --gpus-per-node=1
#SBATCH --gpus-per-task=1
#SBATCH --gpu-bind=verbose,per_task:1
#SBATCH -t 2:00:00

cd $SLURM_SUBMIT_DIR
source ~/env/lmp_deepmd.sh


INPUT_FILE=start.lmp
RESTART_FILE=Restart.lmp
DATA_RESTART=restart.new
CHECKFILE=JOBFINISHEDSTEPS





START=$(date)
if [ ! -e $DATA_RESTART ] ; then
    #########################################################################                                                   
    # First run commands
    #########################################################################   
    echo "first run"
    rm -f  thermo.out  lmp.lammpstrj  log.lammps
    # lmp -in start.lmp
    $LAMMPS_EXE -in $INPUT_FILE

    
else
    #########################################################################                                                   
    # Restart
    ######################################################################### 
    echo "restarting"

    ########################
    # Writing restart input
    ########################
    rm -f $RESTART_FILE
    echo "writing restart file"
    awk -v ut=${RESTART_FILE} -v data=${DATA_RESTART} '
    $1=="read_data" {
        printf("#%s \n", $0) >> ut
        printf("read_restart    %s \n", data) >> ut
    } 
    $1!="read_data" && $1!="velocity" {
        print $0 >> ut
    }
    ' ${INPUT_FILE}      

    
    ########################                                                   
    # Restart run commands
    ########################     
    # lmp -in Restart.lmp
    $LAMMPS_EXE -in $RESTART_FILE
fi
END=$(date)
Time_diff_in_secs=$(($(date -d "$END" +%s) - $(date -d "$START" +%s)))


chmod -R u+rwx,go+rxw .



######################################################################### 
# check the finished steps after running 
#########################################################################

# if not finished successfully, exit
if [ ! -e $CHECKFILE ] ; then
    echo "Not finished successfully"
    exit 1
fi



# current finished steps
currstep=`tail -n 1 $CHECKFILE | awk '{print $1}'`
echo finished steps: $currstep


# # total steps
# totalstep=`awk '
# $1 == "variable" && $2 ==  "nsteps" && $3 == "equal" {
#     print $4
# }' ${INPUT_FILE}`
# echo total steps: $totalstep

# ######################################################################### 
# # if not finished, do something again
# #########################################################################
# if [ $currstep -lt $totalstep ] ; then
#     echo resubmitting 
#     mv stdout stdout_$currstep & 
#     mv lmp_running.lammpstrj lmp.lammpstrj.$currstep &  

#     if [ "$Time_diff_in_secs" -le "600" ]; then
# 	echo FINISHED, run exited premeaturely.
#     else
	
# 	sbatch --job-name $SLURM_JOB_NAME   ../../job.sh
#     fi
# fi
# ######################################################################### 

