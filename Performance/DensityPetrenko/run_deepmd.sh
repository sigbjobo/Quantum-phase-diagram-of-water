export CUDA_VISIBLE_DEVICES="0"
export OMP_NUM_THREADS=4
export TF_INTRA_OP_PARALLELISM_THREADS=2
export TF_INTER_OP_PARALLELISM_THREADS=2

conda activate deepmd2.1.1
ls DeePMD/*/ -d | xargs -l -P1 bash -c 'cd $0; pwd; ~/software/miniconda3/envs/deepmd2.1.1/bin/lmp  -in start.lmp'

