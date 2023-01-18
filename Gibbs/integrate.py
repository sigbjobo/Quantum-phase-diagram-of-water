import numpy as np
from scipy import integrate
import  os, glob
import argparse
import numpy as np
parser = argparse.ArgumentParser(description='Set settings for Gibbs-Duhem integration.')

parser.add_argument('--initial_point_folder', type=str,
                    help='Folder containing initial point used for Gibbs-Duhem', default='Clausius')
 
parser.add_argument('--integration_variable', type=str,
                    help='Specify whether T or P is used as dependent variable.', default='P')

parser.add_argument('--end_variable', type=float,
                    help='Where to stop intergration.', default=3000.0)

parser.add_argument('--steps_per_sim', type=int,
                    help='Number of steps per simulation.', default=10000)
parser.add_argument('--left', type=str,
                    help='Left side phase.', default='IceIh')
parser.add_argument('--right', type=str,
                    help='Right side phase.', default='Liquid')

parser.add_argument('--percent_equilibration', type=float,
                    help='Percent of simulation dedicated to equilibration.', default=20.0)

parser.add_argument('--root_fold', type=str,
                    help='Folder used to store all simulations.', default='Gibbs_Duhem_Simulations/')

parser.add_argument('--step', type=float,
                    help='Integration step length used for integration.', default=100)

parser.add_argument('--initial_equilibration_steps', type=int,
                    help='Perform an initial simulation to equilibrate to desired pressure and temperature.', default=0)

parser.add_argument('--initial_TP', type=float,nargs=2,
                    help='Initial values for melting point T and P', default=[None,None])

parser.add_argument('--lmp_exe', type=str,
                    help='Path to lammps executable.', default='$LAMMPS_EXE') 

parser.add_argument('--run_cmd', type=str,
                    help='Command for running lammps', default='srun -n 2 ')
 
parser.add_argument('--lmp_options', type=str,
                    help='Options used by lammps. ', default='')

parser.add_argument('--integrator', type=str,
                    help='Integrator used by Gibbs-Duhem, either RK4 or Euler. ', default='RK4')

parser.add_argument('--max_error_vol', type=float,
                    help='Maximum error tolerated for volume.', default=0.1)

parser.add_argument('--n_error_blocks', type=float,
                    help='Number of blocks used for error etimate.', default=4)
 
parser.add_argument('--parallel', type=bool,
                    help='Run the two simulations in parallel or sequentially.', default=False)
parser.add_argument('--max_num_runs', type=int,
                    help='Maximum number of iterations to achieve volume average before giving up.', default=100)
parser.add_argument('--out_freq', type=int,
                    help='How often to print thermo data.', default=1000)

parser.add_argument('--mode', type=str,
                    help='Integration mode, options are gibbs or iso. The iso option will depending on the integration variable be isotherm or isobar.', default='gibbs')


parser.add_argument('--units', type=str,
                    help='Unit used by lammps. ', default='metal')

parser.add_argument('--restart_if_possible', type=bool,
                    help='Use previous simulation if it exists.', default=True)

args = parser.parse_args()
args.root_fold+='/'
args.left='/'+args.left+'/'
args.right='/'+args.right+'/'
print(args)

if args.units=='metal':
    pconv=1.01325
else:
    pconv=1.0


I=0
dt=0

def rungekutta4(f, y0, t, args=()):
    # Classic RK4 integrator
    n = len(t)
    y = np.zeros((n, len(y0)))
    y[0] = y0
    for i in range(n - 1):
        h = t[i+1] - t[i]
        k1 = f(y[i], t[i], *args)
        k2 = f(y[i] + k1 * h / 2., t[i] + h / 2., *args)
        k3 = f(y[i] + k2 * h / 2., t[i] + h / 2., *args)
        k4 = f(y[i] + k3 * h, t[i] + h, *args)
        y[i+1] = y[i] + (h / 6.) * (k1 + 2*k2 + 2*k3 + k4)
    f(y[-1], t[-1], *args)
    return y

def euler(f, y0, t, args=()):
    # Forward Euler integrator
    n = len(t)
    y = np.zeros((n, len(y0)))
    y[0] = y0
    for i in range(n - 1):
        h = t[i+1] - t[i]
        k1 = f(y[i], t[i], *args)
        y[i+1] = y[i] + h*k1

    return y

def block_error(x,n):
    # Returns error estiumate using standard deviation for n blocks
    # Reverse to use last part of x
    x=x[::-1]
    return np.std([np.mean(x[len(x)//n*i:len(x)//n*(i+1)]) for i in range(n)])*1.96


def AppendVolEnth(fn1,fn2):
    # Fail-safe appending of volume and enthalpy files
    # Avoids crashes when LAMMPS outputs corrupted files
    steps=set()
    try:
        with open(fn1,'r') as fp1:
            lines1 = fp1.readlines()
    except:
        lines1=[]

    with open(fn2,'r') as fp2:
        lines2 = fp2.readlines()

    
    with open(fn1,'w') as fp:
        for l in lines1[:]:
            ls=l.split()
            try:
                if ls[0]=='#':
                    fp.write(l)
                elif (len(ls)==3 and 3==sum([li.replace('.','').replace('-','').isdecimal() for li in ls]) and (not int(ls[0]) in steps)):
                      
                    steps.add(int(ls[0]))
                    fp.write(l)
            except:
                pass
        for l in lines2[:]:
            ls=l.split()
            try:
                print(len(lines1))
                if ls[0]=='#' and len(lines1)==0:
                    fp.write(l)
                elif (len(ls)==3 and 3==sum([li.replace('.','').replace('-','').isdecimal() for li in ls]) and (not int(ls[0]) in steps)):
                    steps.add(int(ls[0]))
                    fp.write(l)
            except:
                pass
            

def extract_form_log(fn):
    lines=open(fn,'r').readlines()
    start=np.where([('Step' in l) for l in lines])[-1][0]
    data={keyi.lower(): []  for keyi in lines[start].split()}
    for l in lines[start+1:]:
        ls=l.split()
        if ls[0].isdigit():
            for i, key in enumerate(data.keys()):
                try:
                    data[key].append(float(ls[i]))
                except:
                    pass
        else:
            break
    for key in data.keys():
        data[key]=np.array(data[key])
    return data

def fn(y,x):
    # This function simulates two phases for a single state point,
    # and calculates DP/DT from differences in average enthalpy and volume.
    global I
    global args
    global dt
    global pconv
    if args.integration_variable=='P':
        P_str='{:.1f}'.format(x)
        T_str='{:.2f}'.format(y[-1])    
    elif args.integration_variable=='T':
        P_str='{:.1f}'.format(y[-1])
        T_str='{:.2f}'.format(x)     
    else:
        exit
    
    if args.units=='real':
        P_num=float(P_str)
    elif args.units=='metal':
        P_num=float(P_str)*1.01325
    else:
        print('ERROR: unit {} is not supported'.format(args.units))

    name_sim=args.root_fold+str(I)+'_'+T_str+'_'+P_str
        
    
    # Create directory for Gibbs-Duhem simulations
    # if simulations does not already exist
    if not os.path.exists(name_sim+'/FINISHED') and args.restart_if_possible:
        # Make new folder if no folder exists
        if not os.path.exists(name_sim):
            os.system('mkdir -p {}'.format(name_sim))
    
 
            # Replace starting configuration by previous
            os.system('cp -r  {}/{} {}/'.format(args.initial_point_folder,args.left,name_sim))
            os.system('cp -r  {}/{} {}/'.format(args.initial_point_folder,args.right,name_sim))
            if abs(I)>0:
                closest=glob.glob(args.root_fold+str(int(I-np.sign(dt)))+'_*_*/')[0]
                os.system('cp -r  {}/{}/restart.* {}/{}/'.format(closest,args.left,name_sim,args.left))
                os.system('cp -r  {}/{}/restart.* {}/{}/'.format(closest,args.right,name_sim,args.right))
            else:
                closest=args.initial_point_folder
                
            
            # Specify pressure and tempreature
            cmd=''
            cmd+='sed -i  "s#variable .* pressure .*#variable        pressure equal {}#g" {}/in.pressure\n'.format(P_num,name_sim+args.right)
            cmd+='sed -i  \"s#variable.*temperature.*#variable        temperature equal {}#g\" {}/in.temp\n'.format(T_str,name_sim+args.right)
            cmd+='sed -i  \"s#thermo_style.*#thermo_style    custom step temp pe etotal epair emol press lx ly lz vol pxx pyy pzz pxy pxz pyz enthalpy#g\" {}/in.setup\n'.format(name_sim+args.right)
            cmd+='sed -i  \"s#out_freq equal.*#out_freq equal {}#g\" {}/in.setup\n'.format(args.out_freq,name_sim+args.right)

            cmd+='sed -i  "s#variable .* pressure .*#variable        pressure equal {}#g" {}/in.pressure\n'.format(P_num,name_sim+args.left)
            cmd+='sed -i  \"s#variable.*temperature.*#variable        temperature equal {}#g\" {}/in.temp\n'.format(T_str,name_sim+args.left)
            cmd+='sed -i  \"s#thermo_style.*#thermo_style    custom step temp pe etotal epair emol press lx ly lz vol pxx pyy pzz pxy pxz pyz enthalpy#g\" {}/in.setup\n'.format(name_sim+args.left)
            cmd+='sed -i  \"s#out_freq equal.*#out_freq equal {}#g\" {}/in.setup\n'.format(args.out_freq,name_sim+args.left)
            os.system(cmd)



            with open(name_sim+'/start_both.lmp','w') as fp_temp: 
                fp_temp.write("""echo both
variable        pid world 0 1
variable        phase world {} {}

shell cd ${{phase}}
include start.lmp""".format(args.left.strip('/'),args.right.strip('/')))

            with open(name_sim+'/Restart_both.lmp','w') as fp_temp: 
                fp_temp.write("""echo both
variable        pid world 0 1
variable        phase world {} {}

shell cd ${{phase}}
include Restart.lmp""".format(args.left.strip('/'),args.right.strip('/')))        
        
        
            if args.initial_equilibration_steps>0 and abs(I)==0:
                cmd  ='sed -i  \"s#run .*#run             {}#g\" {}/start.lmp\n'.format(args.initial_equilibration_steps,name_sim+args.right)
                cmd  +='sed -i  \"s#run .*#run             {}#g\" {}/start.lmp\n'.format(args.initial_equilibration_steps,name_sim+args.left)    
                os.system(cmd)
                if args.parallel:
                # Run equilibration
                    cmd= 'cd {}\n {} {} {}  -in start_both.lmp -screen none\n'.format(name_sim,args.run_cmd,args.lmp_exe,args.lmp_options) 
                    os.system(cmd)
                else:
                    cmd = 'cd {}\n {} {} {}  -in start.lmp -screen none\n'.format(name_sim+args.left,args.run_cmd,args.lmp_exe,args.lmp_options)
                    os.system(cmd)
                 
                    cmd = 'cd {}\n {} {} {}  -in start.lmp -screen none\n'.format(name_sim+args.right,args.run_cmd,args.lmp_exe,args.lmp_options)
                    os.system(cmd)
                   
                
        
        vol_err_left=1E20
        vol_err_right=1E20
        #Starting Error (only volume supported)                                                                                                                                             
        nruns=0

        #Iterations with two parallel simulations
        if args.parallel:
            while (vol_err_left>args.max_error_vol and vol_err_right>args.max_error_vol ):
                  # Run simulation         
                  cmd  = 'sed -i  \"s#run .*#run             {}#g\" {}/Restart.lmp\n'.format(args.steps_per_sim,name_sim+args.right)
                  cmd += 'sed -i  \"s#run .*#run             {}#g\" {}/Restart.lmp\n'.format(args.steps_per_sim,name_sim+args.left)
                  cmd += 'cd {}\n {} {} {}  -in Restart_both.lmp -screen none\n'.format(name_sim,args.run_cmd,args.lmp_exe,args.lmp_options)
                  os.system(cmd)

                  AppendVolEnth(name_sim+args.right+'/vol_enthalpy_total.dat',name_sim+args.right+'/vol_enthalpy.dat')
                  AppendVolEnth(name_sim+args.left+'/vol_enthalpy_total.dat',name_sim+args.left+'/vol_enthalpy.dat')
                  
                  log_right = np.loadtxt(name_sim+args.right+'/vol_enthalpy_total.dat')
                  log_left  = np.loadtxt(name_sim+args.left+'/vol_enthalpy_total.dat')
                  production=int(len(log_left[:,0])*args.percent_equilibration/100.)
                  vol_err_left=block_error(log_left[:,1][production:],args.n_error_blocks)
                  vol_err_right=block_error(log_right[:,1][production:],args.n_error_blocks)
                  nruns+=1
                  if nruns>args.max_num_runs:
                      print('Volume error did not converge below {} error threshold in {} iterations.'.format(args.max_error_vol,nruns))
                      exit()

        else:
            #Iterations on left phase
            nruns=0
            cmd  = 'sed -i  \"s#run .*#run             {}#g\" {}/Restart.lmp\n'.format(args.steps_per_sim,name_sim+args.left)
            os.system(cmd)
            while(vol_err_left>args.max_error_vol):
                 
                cmd = 'cd {}\n {} {} {}  -in Restart.lmp \n'.format(name_sim+args.left,args.run_cmd,args.lmp_exe,args.lmp_options)
                os.system(cmd)
                AppendVolEnth(name_sim+args.left+'/vol_enthalpy_total.dat',name_sim+args.left+'/vol_enthalpy.dat')
                
                log_left  = np.loadtxt(name_sim+args.left+'/vol_enthalpy_total.dat')
                production=int(len(log_left[:,0])*args.percent_equilibration/100.)
                vol_err_left=block_error(log_left[:,1][production:],args.n_error_blocks)
                nruns+=1
                if nruns>args.max_num_runs:
                    print('Volume error did not converge below {} error threshold in {} iterations.'.format(args.max_error_vol,nruns))
                    exit()
            

            #Iterations on right phase
            nruns=0
            cmd  = 'sed -i  \"s#run .*#run             {}#g\" {}/Restart.lmp\n'.format(args.steps_per_sim,name_sim+args.right)
            os.system(cmd)
                
            while(vol_err_right>args.max_error_vol):
                print('Right error:',vol_err_right)
                cmd = 'cd {}\n {} {} {}  -in Restart.lmp\n'.format(name_sim+args.right,args.run_cmd,args.lmp_exe,args.lmp_options)
                os.system(cmd)
                AppendVolEnth(name_sim+args.right+'/vol_enthalpy_total.dat',name_sim+args.right+'/vol_enthalpy.dat')
                                
                log_right  = np.loadtxt(name_sim+args.right+'/vol_enthalpy_total.dat')
                production=int(len(log_right[:,0])*args.percent_equilibration/100.)
                vol_err_right=block_error(log_right[:,1][production:],args.n_error_blocks)
                nruns+=1
                if nruns>args.max_num_runs:
                    print('Volume error did not converge below {} error threshold in {} iterations.'.format(args.max_error_vol,nruns))
                    exit()
       

    # Gather result
    log_right = np.loadtxt(name_sim+args.right+'/vol_enthalpy_total.dat')
    log_left  = np.loadtxt(name_sim+args.left+'/vol_enthalpy_total.dat') 
      
    production=int(len(log_left[:,0])*args.percent_equilibration/100.)
    h_iceIh  = np.mean(log_left[:,2][production:])
    v_iceIh  = np.mean(log_left[:,1][production:])
    h_liquid = np.mean(log_right[:,2][production:])
    v_liquid = np.mean(log_right[:,1][production:])
    
    # Change in volume from iceIh to right
    dv=v_liquid-v_iceIh #Å^3
    if args.units=='real' or  args.units=='metal':
        dv_si = dv*1E-10**3 #m^3
    else:
        print("ERROR: Unit not supported!")
        exit()
 

    # Change in enthalpy from iceIh to right
    dh=h_liquid-h_iceIh #kcal/mol
    if args.units=='real':
        dh_si = dh*6.9477E-21
    elif args.units=='metal':
        dh_si = dh*1.602176634E-19

    DPDT_si = (dh_si)/(dv_si*T)

    # Derivative
    DPDT_atm=DPDT_si/101325
    DTDP_atm=1./DPDT_atm

    if args.mode=='iso':
        DPDT_atm=0
        DTDP_atm=0


    I = I + int(np.sign(dt))

    with open(name_sim+'/FINISHED','w') as fp:
        fp.write('Gibbs-Duhem step successfully finished.')

    # Return depending on integration variable
    if args.integration_variable=='P':
        return DTDP_atm
    elif args.integration_variable=='T':
        return DPDT_atm



    
# Set initial point
if args.initial_TP[0]  is None:
    T = np.array([float(os.popen('grep temperature {}/{}/in.temp'.format(args.initial_point_folder,args.left)).read().split()[-1])])
    P = np.array([float(os.popen('grep " pressure " {}/{}/in.pressure'.format(args.initial_point_folder,args.left)).read().split()[-1])])*pconv
else:
    T=np.array([args.initial_TP[0]])
    P=np.array([args.initial_TP[1]])


    
# Run integration
if args.integration_variable=='P':   
    if P[0]<args.end_variable:
        dt=args.step
    else:
        dt=-args.step
    
    if args.integrator=='RK4':
        t=np.arange(P[0],args.end_variable,dt)
        y=rungekutta4(fn,T,t)
    elif args.integrator=='Euler':
        t=np.arange(P[0],args.end_variable+dt,dt)
        y=euler(fn,T,t)
    last=fn(np.array(y[-1]),t[-1])
    
if args.integration_variable=='T':
    if T[0]<args.end_variable:
        dt=args.step
    else:
        dt=-args.step

    if args.integrator=='RK4':
        t=np.arange(T[0],args.end_variable,dt)
        y=rungekutta4(fn,P,t)
    elif args.integrator=='Euler':
        t=np.arange(T[0],args.end_variable+dt,dt)
        y=euler(fn,P,t)
    last=fn(np.array(y[-1]),t[-1])

