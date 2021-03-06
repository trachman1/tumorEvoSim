import main
import sys
first= int(sys.argv[1])
last = int(sys.argv[2])
for r in [0,20,40,50]:
        exp_path = f'radial_s=.1/r={r}_di=.1_do=.9'
        dr_params = {'radius':r ,'inner_rate': .1 ,'outer_rate': .9}
        main.simulateTumor(dim =2, driver_advantage = .1,n_cells = 20000,exp_path = exp_path, driver_prob = 1e-2, dr_function = 'radial', dr_params = dr_params, first_rep = first, last_rep = last, reps = last-first+1)
        exp_path = f'radial_s=.1/r={r}_di=.9_do=.1'
        dr_params = {'radius':r ,'inner_rate': .9 ,'outer_rate': .1}
        main.simulateTumor(dim =2, driver_advantage = .1,n_cells = 20000,exp_path = exp_path, driver_prob = 1e-2, dr_function = 'radial', dr_params = dr_params, first_rep = first, last_rep = last, reps = last-first+1)
