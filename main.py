#file with end-user functions to set parameters and run simulation 
import numpy as np
import pickle
import classes
import os
from pathlib import Path
import simulation
#absolute path to parameter file 
PARAMS_PATH = '/Users/trachman/Documents/current/tumor_stuff/tumorEvoSim' #change to program directory 
#defualt parameters: 
DIM = 2
INIT_BIRTH_RATE = np.log(2)
FIXED_DEATH_RATE = False
DRIVER_ADVANTAGE = .1
INIT_DEATH_RATE = .95*INIT_BIRTH_RATE
MAX_DEATH_RATE = INIT_BIRTH_RATE

PAD = 5 #fraction of radius to pad boundary 
MUTATOR_FACTOR = .01
BOUNDARY = 300
MAX_ITER = int(1e9)
MAX_POP = 50000
PUSH = 0
INIT_MUT_PROB = .02 #taken from Waclaw et al. 2015 
DRIVER_PROB = 4e-5

MUTATOR_PROB = 0#4e-6 #need to implement way of increasing mutation probability in individual cell lines 
PROGRAMMED_DEATH_RATE = False
SEED = 123
SAVE_INTERVAL = 1000 #number of cells to save after 


def set_nbrs(neighborhood = 'moore', dim = DIM):
    NBRS = []
    if neighborhood == 'moore':
            for i in [0,-1,1]:
                for j in [0,-1,1]:
                    if dim ==2:
                        NBRS.append([i,j])
                    else:
                        for k in [0,-1,1]:
                            NBRS.append([i,j,k])
            NBRS = np.array(NBRS)[1:]
    else:   
        if dim==3:
            NBRS = np.array([[1,0,0], [-1,0,0], [0,1,0],[0,-1,0],[0,0,1],[0,0,-1]])
        else:
            NBRS = np.array([[1,0],[-1,0],[0,1],[0,-1]])
    return NBRS
def set_params(*args):
    return args
    
NBRS = set_nbrs()
def get_kwargs_from_file(path):
    #TODO
    raise(NotImplementedError)
def calc_radius(n_cells, dim):
    if dim==2:
        return np.sqrt(n_cells/np.pi)
    else:
        return np.cbrt(3*n_cells/4/np.pi)
"""wrapper to take user parameters. Accepts a file or a set of keyword arguments """
def config_params(kwargs):
    if 'filePath' in kwargs:
        kwargs = get_kwargs_from_file(kwargs['filePath'])
    if 'dim' not in kwargs:
            kwargs['dim']=DIM
    if 'n_cells' not in kwargs:
            kwargs['n_cells'] = MAX_POP
    if 'neighborhood' not in kwargs:
            kwargs['neighborhood'] = 'moore'
    if kwargs['neighborhood']!= 'moore':
        kwargs['neighborhood'] = 'von_neumann'
    if 'fixed_death_rate' not in kwargs:
            kwargs['fixed_death_rate'] = False
    if 'init_death_rate' not in kwargs:
            kwargs['init_death_rate'] = INIT_DEATH_RATE
    if 'init_birth_rate' not in kwargs:
            kwargs['init_birth_rate'] = INIT_BIRTH_RATE
    if 'driver_advantage' not in kwargs:
            kwargs['driver_advantage'] = DRIVER_ADVANTAGE
    if 'driver_prob' not in kwargs:
            kwargs['driver_prob'] = DRIVER_PROB
    if 'max_death_rate' not in kwargs:
        kwargs['max_death_rate'] = MAX_DEATH_RATE
    if 'mutator_factor' not in kwargs:
        kwargs['mutator_factor']= MUTATOR_FACTOR
    if 'max_iter' not in kwargs:
        kwargs['max_iter'] = MAX_ITER
    if 'init_mut_prob' not in kwargs:
        kwargs['init_mut_prob'] = INIT_MUT_PROB
    if 'mutator_prob' not in kwargs:
        kwargs['mutator_prob'] = MUTATOR_PROB
    if 'progression' not in kwargs:
        kwargs['progression'] = None
    if 'exp_path' not in kwargs:
        kwargs['exp_path'] = PARAMS_PATH
    if 'reps' not in kwargs:
        kwargs['reps'] = 1
    if 'save_interval' not in kwargs:
        kwargs['save_interval'] = SAVE_INTERVAL
    if 'rep_start' not in kwargs:
        kwargs['rep_start'] = 0
    



    
    #set dependent parameters, sanity checks
    kwargs['driver_dr_factor'] = 1-kwargs['driver_advantage'] #death rate factor
    r = calc_radius(kwargs['n_cells'],kwargs['dim'])
    kwargs['boundary'] = int(r*(1+PAD))
    if kwargs['fixed_death_rate']: kwargs['driver_prob'] = 0 
    kwargs['neighbors'] = set_nbrs(kwargs['neighborhood'],kwargs['dim'])
   

    #write params to pkl file for rest of simulation to use
    
    with open(os.path.join(PARAMS_PATH,'params.pkl'), 'wb') as outfile:
        pickle.dump(kwargs, outfile, protocol=pickle.HIGHEST_PROTOCOL)    
    #write params to experiment location 
    Path(kwargs['exp_path']).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(kwargs['exp_path'],'params.pkl'), 'wb') as outfile:
        pickle.dump(kwargs, outfile, protocol=pickle.HIGHEST_PROTOCOL)    
    return kwargs
  
    
def simulateTumor(**kwargs):
    params = config_params(kwargs)
    rep = params['rep_start']
    sim_list = []
    while rep<params['reps']:
        sim = classes.Simulation(params)
        sim.run(rep) 
        #simulation.plot_slice(sim.tumor)
        sim_list.append(sim)
        rep+=1
    return sim

if __name__ == '__main__': 
    import simulation
    #exp_path = 'Documents/current/tumor_stuff/hi_s_2d'
    #out = simulateTumor(dim =2, driver_advantage = 4,n_cells = 100000,exp_path = exp_path)
    #print(out.tumor.hit_bound)
    #simulation.plot_slice(out.tumor,ax = 'x')
    #simulation.plot_slice(out.tumor,ax = 'y')
    #simulation.plot_slice(out.tumor,ax = 'z')
    exp_path = 'Documents/current/tumor_stuff/driv_demo'
    out = simulateTumor(dim =2, driver_advantage = .1,n_cells = 100000,exp_path = exp_path,save_interval = 100000)
    simulation.plot_tumor(out.tumor)
    
    