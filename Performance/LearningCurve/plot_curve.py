import matplotlib.pyplot as plt
import numpy as np,os

input_dir = './' #It3_re3'
train_log = 'It3_re3_lcurve.out'
show_items = ["rmse_e_trn", "rmse_e_val", 
              "rmse_f_trn", "rmse_f_val", 
              "rmse_v_trn", "rmse_v_val",
             ]
ev2km=23.0605419
scale = ev2km


def cal_rmse(x, y):
    return np.sqrt(np.mean((x-y)**2))

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w



curr_case = os.path.basename(os.path.realpath(input_dir))

data_train = np.loadtxt(os.path.join(train_log), skiprows=1)
data_train[:, 1:-1] *= scale


with open(os.path.join(input_dir,train_log), 'r') as f:
    headers = f.readline().rstrip()

headers = headers.split()[1:]

# blue
# green
# red
# orange
# olive

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
        'fmt': 'g--',
        'name': 'Energy val.',
    },
    'rmse_e_trn': {
        'fmt': 'b-',
        'name': 'Energy train.',
    },    

    'rmse_f_val': {
        'fmt': 'm--',
        'color': 'tab:orange',
        'linestyle': '--',
        'name': 'Force val.',
    },
    'rmse_f_trn': {
        'fmt': 'r-',
        'name': 'Force train.',
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


fig2, ax2 = plt.subplots(figsize=(3.4, 2.5))

for it in show_items:
    try: 
        idx = headers.index(it)
        plot_data.append(moving_average(data_train[:, idx], window_size) )  # data
        plot_name.append(plot_dict[it]['name'])
        plot_fmt.append(plot_dict[it]['fmt'])        
    except:
        pass    



idx_step = headers.index('step')
plot_items = []

# for i in range(len(plot_data)):
for i in range(2):
    step_end = plot_data[i].shape[0]
    _l = ax2.plot(data_train[:step_end:batch_size, idx_step], plot_data[i][::batch_size], plot_fmt[i], label=plot_name[i])
    plot_items = [*plot_items, *_l]
    
    
ax2tw = ax2.twinx()
for i in range(2, 3):
    step_end = plot_data[i].shape[0]
    _l = ax2tw.plot(data_train[:step_end:batch_size, idx_step], plot_data[i][::batch_size], plot_fmt[i], label=plot_name[i])
    plot_items = [*plot_items, *_l]

for i in range(3, 4):
    step_end = plot_data[i].shape[0]
    _l = ax2tw.plot(data_train[:step_end:batch_size, idx_step], plot_data[i][::batch_size], 
                    color=plot_dict['rmse_f_val']['color'],
                    linestyle = '--',
                    label=plot_name[i],
                   )
    plot_items = [*plot_items, *_l]
    

# ax2.set_xticklabels([])
# ax2.tick_params(axis='x', labelsize=15)
# ax2.set_xlabel("Training Steps (Million)", fontsize=16)
ax2.tick_params(axis='x', labelsize=8)
ax2.set_xlabel("Training steps ($10^6$)", fontsize=9)




xtickslocs = ax2.get_xticks()
ax2.set_xticklabels(['-1', '0', '', '1', '', '2'])


ax2.set_yscale('log')
ax2.set_ylabel(r'Energy/atom RMSE (kcal mol$^{-1}$)', fontsize=9)
ax2.tick_params(axis='y', labelsize=8)
ax2tw.tick_params(axis='y', labelsize=8)


plt.legend(frameon=False, 
           handles=plot_items,
           fontsize = 8,
          )


ax2tw.set_yscale('log')
# ax2tw.set_ylabel('Force RMSE per atom (kcal/mol Å)', fontsize=16)
ax2tw.set_ylabel('Force RMSE (kcal$\,$mol$^{-1}$Å$^{-1}$)', fontsize = 9)
ax2tw.set_ylim([0.5, 10])




#     plt.title('Training convergence for \n %s \n Unit: kcal/mol[/A]'%curr_case, fontsize=16, y=1)
fig2.tight_layout()


save_train = "PaperFig_train_" + curr_case[:-4]
plt.savefig(os.path.join('./', save_train + '.png'), dpi=600, format='png', bbox_inches='tight')
plt.savefig(os.path.join('./', save_train + '_lowdpi.png'), dpi=100, format='png', bbox_inches='tight')

plt.savefig(os.path.join('./', save_train + '.pdf'), dpi=600, format='pdf', bbox_inches='tight')
#     plt.close(fig2)
