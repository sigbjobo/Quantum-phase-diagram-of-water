# ls IV/COEX_*/*K  -d | xargs -l bash -c 'cd $0; pwd; sbatch ../../../job.sh'
# ls VII/COEX_*/*K XII/COEX_*/*K -d | xargs -l bash -c 'cd $0; pwd; sbatch ../../../job.sh'
#ls COEX_3*/*K  -d | xargs -l bash -c 'cd $0; pwd; sbatch --job-name=II ../../job.sh'
#Ih/COEX_*/*K


for fold in $(ls *atm/*K/ -d| grep -v COEX_3000atm/250K/ |xargs -l) #|  grep -v  COEX_3000atm/245K| grep -v  COEX_3000atm/250K| grep -v COEX_6000atm/245K  )
do
    ice=$(basename $(realpath $fold/../../))
    echo $fold
    T=$(basename $fold)
    echo $T
    P=$(echo $(basename $(realpath $fold/../))| sed 's#COEX_##g'|sed 's#000#k#g')
    echo $ice $T $P
    name=$ice$P$T
    echo $name

    cd $fold
    sbatch --job-name=$name ~/Jobscripts/CoexDeePMD/job.sh
    cd -

done
