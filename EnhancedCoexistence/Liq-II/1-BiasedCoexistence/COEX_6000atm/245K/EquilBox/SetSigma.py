import os
import sys
import glob
os.system('sed -i \'s#SIGMA=.*#SIGMA={}#g\' {}'.format(sys.argv[1],sys.argv[2]))


envs=glob.glob('env*.pdb')
lines=''
for i, env in enumerate(sorted(envs)):
    lines+=' REFERENCE_{}={}\\n'.format(i+1,env)

os.system('sed -i \'s#SIGMA=.*#SIGMA={}#g\' {}'.format(sys.argv[1],sys.argv[2]))
os.system('sed -i \'s#REPLACE_REFERENCE#{}#g\' {}'.format(lines,sys.argv[2]))

