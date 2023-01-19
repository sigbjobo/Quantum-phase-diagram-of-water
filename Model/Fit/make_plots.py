#!/usr/bin/env python
# coding: utf-8

# In[38]:


import os 
import math
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt



# energy scale factor 
# 1 kcal/mol = 4.3363*10^(-2) eV
# 1 eV = 23.061 kcal/mol

ev2km = 23.061
km2ev = 4.3363e-2



def cal_rmse(x, y):
    return np.sqrt(np.mean((x-y)**2))

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


# In[9]:


def plot_train(input_dir = './',
               train_log = 'lcurve.out',
               show_items = ["rmse_e_trn", "rmse_e_val", 
                              "rmse_f_trn", "rmse_f_val", 
                              "rmse_v_trn", "rmse_v_val",
                             ],
               scale = ev2km,
              ):


    curr_case = os.path.basename(os.path.realpath(input_dir))

    data_train = np.loadtxt(os.path.join(input_dir,train_log), skiprows=1)
    data_train[:, 1:-1] *= scale

    
    with open(os.path.join(input_dir,train_log), 'r') as f:
        headers = f.readline().rstrip()

    headers = headers.split()[1:]

    plot_dict = {
        'rmse_val': {
            'fmt': 'k--',
            'name': 'RMSE_total/atom val',
        },
        'rmse_trn': {
            'fmt': 'k-',
            'name': 'RMSE_total/atom train',
        },

        'rmse_e_val': {
            'fmt': 'c--',
            'name': 'RMSE_energy/atom val',
        },
        'rmse_e_trn': {
            'fmt': 'b-',
            'name': 'RMSE_energy/atom train',
        },    

        'rmse_f_val': {
            'fmt': 'm--',
            'name': 'RMSE_force/atom val',
        },
        'rmse_f_trn': {
            'fmt': 'r-',
            'name': 'RMSE_force/atom train',
        },        

        'rmse_v_val': {
            'fmt': 'y--',
            'name': 'RMSE_virial/atom val',
        },
        'rmse_v_trn': {
            'fmt': 'g-',
            'name': 'RMSE_virial/atom train',
        },            
    }


    window_size = 200
    batch_size = int( data_train.shape[0] / 1000 )
    

    plot_data = []
    plot_name = []
    plot_fmt = []


    fig2, ax2 = plt.subplots()

    for it in show_items:
        try: 
            idx = headers.index(it)
            plot_data.append(moving_average(data_train[:, idx], window_size) )  # data
            plot_name.append(plot_dict[it]['name'])
            plot_fmt.append(plot_dict[it]['fmt'])        
        except:
            pass    



    idx_step = headers.index('step')
    for i in range(len(plot_data)):
        step_end = plot_data[i].shape[0]
        ax2.plot(data_train[:step_end:batch_size, idx_step], plot_data[i][::batch_size], plot_fmt[i], label=plot_name[i])


    # # plot test 
    # # N_pts = plot_data[0].shape[0]    
    # # X_test = np.arange(N_pts)[::batch_size].shape[0]
    # X_test = data_train[step_end, idx_step]
    # y_test = rmse_atom_training
    # ax2.plot(X_test, y_test, 'd', markersize=12,label='Energy RMSE of all test sets')


    # ax2.set_xticklabels([])
    ax2.tick_params(axis='x', labelsize=15)
    ax2.set_xlabel("Training Steps", fontsize=16)

    
    plt.yscale('log')
    plt.ylabel('RMSE/atom in kcal/mol[/A]', fontsize=16)
    ax2.legend()


    plt.title('Training convergence for \n %s \n Unit: kcal/mol[/A]'%curr_case, fontsize=16, y=1)
    fig2.tight_layout()


    save_train = "Fig_train_" + curr_case + '.png'
    plt.savefig(os.path.join(input_dir, save_train), dpi=300, format='png')
    plt.close(fig2)


# In[36]:
 

def plot_test_energy(input_dir = './',
                     max_cols = 8,
                     max_dots = 0,
                     range_margin = 0.05,
                     scale = ev2km,
                    ):


    curr_case = os.path.basename(os.path.realpath(input_dir))
    
# get all cases
    _tests = [x for x in os.listdir(input_dir) if x.endswith(".e.out") ]
    all_tests = []
    for _x in _tests:
        _idx = _x.find(".e.out")
        _name = _x[:_idx]
        all_tests.append(_name)
    all_tests.sort()

    Eshape = {}
    RMSE = {}

    
# make figure with subplots    
    if len(all_tests) == 0:
        return

    if len(all_tests) > max_cols:
        num_cols = max_cols
        num_rows = int( (len(all_tests)-1)/num_cols ) + 1
    else:
        num_cols = len(all_tests)
        num_rows = 1

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(4*num_cols, 4*num_rows))
    try:
        axs = axs.reshape((num_rows, num_cols))
    except:
        pass
    
    
# iterate through all cases
    i = 0
    for case in all_tests:
        e = 0
        try:
            file = os.path.join(input_dir ,case) + '.e.out'
            e = np.loadtxt(file, skiprows=1)
            e *= scale
            if e.ndim == 1:
                e = e.reshape(1, -1)
        except:
            continue

            
        if 'Ctrb' in curr_case:
            if '2B' in curr_case:
                e[:, 1] /= 2
            elif '3B' in curr_case:
                e[:, 1] /= 3
            
            
        rmse = cal_rmse(e[:, 0], e[:, 1])
        RMSE[case] = rmse
        Eshape[case] = e.shape
        
        
            
        xloc = int(i/num_cols)
        yloc = i - xloc*num_cols
        try:
            ax = axs[xloc, yloc]
        except:
            ax = axs


            
        if max_dots > 0 and max_dots < len(e):
            _idx = np.arange(len(e))
            idx_show = np.random.choice(_idx, max_dots, False)
            idx_show.sort()
            e = e[idx_show]
        
        
        ax.plot(e[:, 0], e[:, -1], 'bo')
    
        ref_x_min = np.min(e)
        ref_x_max = np.max(e)
        
        dref = (ref_x_max - ref_x_min) * range_margin
        
        
        ref_x_min -= dref 
        ref_x_max += dref
        
        ref_x = np.arange(ref_x_min, ref_x_max+dref, dref)
        ref_y = ref_x

        ax.plot(ref_x, ref_y, 'k-')
        
        ax.set_title('%s \n RMSE : %f ' % (case.replace('MB-polRef',''), rmse), fontsize=18)
        ax.tick_params(axis="x", labelsize=16)
        ax.tick_params(axis="y", labelsize=16)
        
        i+=1

        
        
    while i < num_cols * num_rows:
        xloc = int(i/num_cols)
        yloc = i - xloc*num_cols
        try:
            ax = axs[xloc, yloc]
        except:
            ax = axs
        ax.set_axis_off()
        i += 1
        
        
    fig.suptitle('Test result for case \n %s \nX: reference energy, Y: predicted energy \n Unit: kcal/mol'%curr_case, fontsize=32, y=1)
    # plt.rcParams['axes.facecolor'] = 'silver'
    fig.tight_layout()


    save_test = "Fig_test_" + curr_case + '.png'
    plt.savefig(os.path.join(input_dir, save_test))

    plt.close(fig)

    
    return RMSE, Eshape
    


# In[37]:


def plot_test_force(input_dir = './',
                     max_cols = 8,
                     max_dots = 0,
                     range_margin = 0.05,
                     scale = ev2km,
                    ):



    curr_case = os.path.basename(os.path.realpath(input_dir))
# get all cases
    _tests = [x for x in os.listdir(input_dir) if x.endswith(".f.out") ]
    all_tests = []
    for _x in _tests:
        _idx = _x.find(".f.out")
        _name = _x[:_idx]
        all_tests.append(_name)
    all_tests.sort()

    Fshape = {}
    RMSE = {}

    
# make figure with subplots    
    if len(all_tests) == 0:
        return

    if len(all_tests) > max_cols:
        num_cols = max_cols
        num_rows = int( (len(all_tests)-1)/num_cols ) + 1
    else:
        num_cols = len(all_tests)
        num_rows = 1

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(4*num_cols, 4*num_rows))
    try:
        axs = axs.reshape((num_rows, num_cols))
    except:
        pass
    
    
# iterate through all cases
    i = 0
    for case in all_tests:
        e = 0
        try:
            file = os.path.join(input_dir ,case) + '.f.out'
            f = np.loadtxt(file, skiprows=1)
            f *= scale
            if f.ndim == 1:
                f = f.reshape(1, -1)
        except:
            continue

            
        ncomp = int(f.shape[-1]/2)
        rmse = cal_rmse(f[:, :ncomp], f[:, ncomp:])
        RMSE[case] = rmse
        Fshape[case] = f.shape
        
        
            
        xloc = int(i/num_cols)
        yloc = i - xloc*num_cols
        try:
            ax = axs[xloc, yloc]
        except:
            ax = axs


            
        if max_dots > 0 and max_dots < len(f):
            _idx = np.arange(len(f))
            idx_show = np.random.choice(_idx, max_dots, False)
            idx_show.sort()
            f = f[idx_show]
        

        for ii in range(ncomp):
            ax.plot(f[:, ii], f[:, ii+ncomp], 'go')
        
        ref_x_min = np.min(f)
        ref_x_max = np.max(f)
        
        
        dref = (ref_x_max - ref_x_min) * range_margin
        ref_x_min -= dref 
        ref_x_max += dref
        
        
        ref_x = np.arange(ref_x_min, ref_x_max+dref, dref)
        ref_y = ref_x

        ax.plot(ref_x, ref_y, 'k-')
        print(curr_case)
        ax.set_title('%s \n RMSE : %f ' % (case.replace('MB-polRef',''), rmse), fontsize=18)
        ax.tick_params(axis="x", labelsize=16)
        ax.tick_params(axis="y", labelsize=16)
        
        i+=1

        
        
    while i < num_cols * num_rows:
        xloc = int(i/num_cols)
        yloc = i - xloc*num_cols
        try:
            ax = axs[xloc, yloc]
        except:
            ax = axs
        ax.set_axis_off()
        i += 1
        
        
    fig.suptitle('Test result for case \n %s \nX: reference force, Y: predicted force \n Unit: kcal/(mol*A)'%curr_case, fontsize=32, y=1)
    # plt.rcParams['axes.facecolor'] = 'silver'
    fig.tight_layout()


    save_test = "Fig_test_force_" + curr_case + '.png'
    plt.savefig(os.path.join(input_dir, save_test))
    plt.close(fig)

    
    return RMSE, Fshape
    

    
    

    
if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Plot DeePMD training and test results')
    
    parser.add_argument('folder', metavar='dir', 
                        type=str, nargs='?',
                        default='./',
                        help='the directory to plot, default: current folder')
    parser.add_argument('--no_train', action='store_true',
                        help='if plot training learning curve, default:to plot')
    parser.add_argument('--no_test_e', action='store_true',
                        help='if create test E correlation plots, default:to plot')
    parser.add_argument('--no_test_f', action='store_true',
                        help='if create test F correlation plots, default:to plot')

    
    args = parser.parse_args()

    path=args.folder
    noTrain = args.no_train
    noTestE = args.no_test_e
    noTestF = args.no_test_f
    print(path)
    if not noTrain:
        plot_train(path)
    
    if not noTestE:
        plot_test_energy(path)
        
    if not noTestF:
        plot_test_force(path)






