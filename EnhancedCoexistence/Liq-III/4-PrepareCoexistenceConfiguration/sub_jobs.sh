# Setup all the tasks                                                                                                                        
                                                                                                                                               
ls */ -d |xargs -l > task.lst

# Shuffle task.lst to get about equal time per job                                                                                             
shuf task.lst -o task.lst

# Choose number of jobs to use and split up tasks                                                                                              
NJOBS=5
split --lines $(( $(wc -l < task.lst) / $NJOBS)) task.lst task_  --additional-suffix .lst -d

# Submit all jobs                                                                                                                              
ls task_*.lst | xargs -l bash -c 'sbatch --export=task_file=$0 job_task.sh'
