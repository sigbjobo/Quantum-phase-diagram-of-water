
ls COEX_*/*K  -d | xargs -l|grep -v 6000.0atm/255.0K| grep -v COEX_5000.0atm/270.0K  bash -c 'cd $0; pwd; sbatch --job-name=III ../../job.sh'
## ls III/COEX_*/*K  -d | xargs -l bash -c 'cd $0; pwd; sbatch ../../../job.sh'
#Ih/COEX_*/*K
