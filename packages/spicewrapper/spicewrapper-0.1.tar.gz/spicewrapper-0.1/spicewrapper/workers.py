import subprocess
import time
import logging
import os
import spice_utils
import data_processing
import simulation_runner
import numpy as np
import pandas as pd
import spice_utils
import uuid
import multiprocessing
import io
import itertools
import random  
import sys
from scipy.optimize import basinhopping

def worker_grid(args):
    ''' 
    This is a worker function for grid sweeps or optimization. It takes a tuple of worker_essentials and input_params, and returns the result of the simulation.
    The input_params dict consists of key:value pairs for the parameters to be optimized, with each parameter having only one value.
    It does not represent all the parameters in the circuit, just the ones being varied or optimized.
    It is assumed that other workers will be assigned different sets of parameters.
    '''
    worker_essentials, input_params, results_queue, progress_queue= args
    worker_id = multiprocessing.current_process().pid
    timeout = worker_essentials.timeout
    interpolation_timestep = worker_essentials.interpolation_timestep
    original_contents = worker_essentials.original_contents
    user_function = worker_essentials.user_function

    logging.info(f"starting worker grid")
    result_df = simulation_runner.prepare_and_run_new_job(original_contents, input_params, timeout, interpolation_timestep, progress_queue, worker_essentials.temp_folder)
    logging.info(f"simulation finished on worker grid")

    score = 0
    if user_function is not None:
        score = user_function(result_df)
    
    if result_df is None or result_df.empty:
        print(f"Result dataframe is None or empty for parameters: {input_params}")
        logging.error(f"Result dataframe is None or empty for parameters: {input_params}")
    
    progress_dict = {
        'worker_id': worker_id,
        'iteration': 0,
        'score': score,
        'params': input_params,
        'result_df': result_df
    }
    results_queue.put(progress_dict)
    # worker_progress_callback(progress_dict)
    if result_df is None or result_df.empty or result_df.isnull().any().any():  
        logging.error(f"Result dataframe is None or empty for parameters: {input_params}")
        return pd.DataFrame(), np.inf
    logging.info(f"Done with worker grid")
    return result_df, score


def worker_basinhopping(args):
    worker_essentials, input_params, seed, basinhopping_params,results_queue, progress_queue= args
    worker_id = multiprocessing.current_process().pid
    best_result_df = None
    best_score = float('inf')
    iteration_count = [0]
    scores = []
    
    class CustomStepTaker:
        def __init__(self, scores, best_score, trapped_threshold, trapped_iterations, stepsize):
            self.scores = scores
            self.best_score = best_score
            self.trapped_threshold = trapped_threshold
            self.trapped_iterations = trapped_iterations
            self.stepsize = stepsize

        def __call__(self, x):
            if len(self.scores) >= self.trapped_iterations:
                recent_scores = self.scores[-self.trapped_iterations:]
                if (min(recent_scores) / max(recent_scores)) > (1 - self.trapped_threshold):
                    print(f"Trapped in local minimum. Returning random step. old x: {x}")
                    x = np.random.uniform(0.001, 0.999, size=x.shape)
                    print(f"new x: {x}")
                    return x
        
            # Default perturbation similar to basinhopping's default step taker
            x_new = x + np.random.uniform(-self.stepsize, self.stepsize, size=x.shape)
            x_new = np.clip(x_new, 0.001, 0.999)  # Ensure x_new stays within bounds [0, 1]
            return x_new
    
    def normalize_params(x):
        return np.array([(val - param[0]) / (param[2] - param[0]) if param[2] != param[0] else 0.5 
                         for val, param in zip(x, input_params.values())])
    
    def denormalize_params(x_norm):
        return np.array([param[0] + x_norm_i * (param[2] - param[0]) if param[2] != param[0] else param[1] 
                         for x_norm_i, param in zip(x_norm, input_params.values())])
        
    def objective_function(x_norm):
        nonlocal best_result_df, best_score, scores
        try:
            
            if(np.isnan(x_norm).any()):
                # print("x_norm contains NaN values")
                return np.inf
            
            x = denormalize_params(x_norm)
            # logging.error(f"x_norm: {x_norm}")
            # logging.error(f"x: {x}")
            params = dict(zip(input_params.keys(), x))
            result_df = simulation_runner.prepare_and_run_new_job(worker_essentials.original_contents, params, worker_essentials.timeout, worker_essentials.interpolation_timestep, progress_queue, worker_essentials.temp_folder)
            if result_df is None or result_df.empty or result_df.isnull().any().any():
                # print(f"Basinhopping run returned None. Parameters: {params}") 
                return np.inf
            
            if worker_essentials.user_function is not None:
                score = worker_essentials.user_function(result_df)
                scores.append(score)
                if score < best_score:
                    best_score = score
                    best_result_df = result_df
                iteration_count[0] +=1
                
                
                progress_dict = {
                    'worker_id': worker_id,
                    'iteration': iteration_count[0],
                    'score': score,
                    'params': params,
                    'result_df': result_df
                }
                results_queue.put(progress_dict)
                # worker_progress_callback(progress_dict)
                return score
            else:
                raise ValueError("User function not provided for optimization.")
        except Exception as e:
            print(f"Error in objective function: {str(e)}")
            return np.inf
    
    initial_values = np.array([param[1] for param in input_params.values()])
    initial_values_norm = normalize_params(initial_values)
    # print(f"initial_values_norm: {initial_values_norm}")
    bounds = [(0, 1) for _ in input_params]
    
    minimizer_kwargs = basinhopping_params.minimizer_kwargs.copy()
    minimizer_kwargs['bounds'] = bounds
    
    try:
        optimizer_result = basinhopping(
            objective_function, 
            initial_values_norm, 
            seed=seed,
            niter=basinhopping_params.niter,
            T=basinhopping_params.T,
            stepsize=basinhopping_params.stepsize,
            minimizer_kwargs=minimizer_kwargs,
            take_step=CustomStepTaker(scores, best_score, basinhopping_params.trapped_threshold, basinhopping_params.trapped_iterations, basinhopping_params.stepsize),
        )
        # Denormalize the result
        optimizer_result.x = denormalize_params(optimizer_result.x)
        
        # Add the best_result_df to the optimization result
        optimizer_result.best_result_df = best_result_df
        
        return best_result_df, best_score,optimizer_result
    except Exception as e:
        print(f"Error in basinhopping: {str(e)}")
        return best_result_df,best_score,None

# def worker_progress_callback(args):
#     logging.info(f"\nWorker {args['worker_id']}: Iterations: {args['iteration']}, Best Score: {args['score']:.6f}, Parameters: {args['params']}")
#     pass
  
def generate_basinhopping_work_list(worker_essentials, optimizer_param_dict, basinhopping_params, n_processes):
    """
    Generates a list of work items for a basinhopping sweep with random perturbations.
    Args:
        worker_essentials (worker_essentials): Contains essential information for workers.
        optimizer_param_dict (dict): Dictionary of parameters to optimize.
        basinhopping_params (basinhopping_params): Parameters for the basinhopping algorithm.
        n_processes (int): Number of workers to generate work items for.
        initial_perturbation (float): Maximum relative perturbation to apply to initial values.
    Returns:
        list: List of work items for basinhopping workers.
    
    Example optimizer_param_dict to pass in:
    Keys are parameter names, and the value is a list of [lower bound, initial value, upper bound].
    
    parameters_to_optimize = {
        'rdelay': [200e3, 220e3, 240e3],
        'snspd_mos_width': [4e-6, 4.5e-6, 8e-6],
        'ntron_mos_width': [9e-6, 11e-6, 25e-6],
        'vdd_val': [0.8, 1, 1.1]
    }
    """
    work_list = []
    for _ in range(n_processes):
        perturbed_params = {}
        for param_name, param_values in optimizer_param_dict.items():
            lower_bound, initial_value, upper_bound = param_values
            
            # Calculate the perturbation range
            perturbation_range = initial_value * basinhopping_params.initial_perturbation
            # Generate a random perturbation within the range
            perturbation = np.random.uniform(-perturbation_range, perturbation_range)
            # Apply the perturbation to the initial value
            perturbed_value = initial_value + perturbation
            # Ensure the perturbed value is within bounds
            perturbed_value = max(lower_bound, min(perturbed_value, upper_bound))
            perturbed_params[param_name] = [lower_bound, perturbed_value, upper_bound]
        # Generate a random seed for each worker
        seed = np.random.randint(0, 2**32 - 1)
        work_list.append((worker_essentials, perturbed_params, seed, basinhopping_params))
    return work_list
  
    
def generate_grid_work_list(worker_essentials, params_grid,randomize=True):
    """
    Generates a list of work items for a grid sweep.  This will be assigned to different workers during parallel simulations.
    The combinations of parameters will be split up.  Everything else is the same for each worker.
    
    Example params_grid to pass in:
    Keys are parameter names, and the value is a list of [lower bound, upper bound, number of points, spacing_type].
    spacing_type is optional and can be 'lin' (default) or 'log'.
    
    parameters_to_grid_optimize = {
        'rdelay': [200e3, 350e3, 8, 'log'],
        'snspd_mos_width': [4e-6, 6e-6, 8],
        'ntron_mos_width': [9e-6, 16e-6, 8, 'lin'],
        'vdd_val': [0.8, 1.1, 4]
    }
    """
    param_names = list(params_grid.keys())
    param_ranges = []
    
    for param in params_grid.values():
        start, stop, num = param[:3]
        spacing_type = param[3] if len(param) > 3 else 'lin'
        
        if spacing_type == 'log':
            param_range = np.geomspace(start, stop, int(num))
        else:  # default to linear spacing
            param_range = np.linspace(start, stop, int(num))
        
        param_ranges.append(param_range)
    
    param_combinations = list(itertools.product(*param_ranges))
    
    if(randomize):
        random.shuffle(param_combinations)  # Shuffle the parameter combinations
    
    work_list = []
    for param_values in param_combinations:
        args = (worker_essentials, dict(zip(param_names, param_values)))
        work_list.append(args)
    
    print(f"Length of work list: {len(work_list)}")
    return work_list

############################################################
#Classes for data storage
############################################################

class BasinhoppingParams:
    def __init__(self,niter,T,stepsize,minimizer_kwargs,initial_perturbation,trapped_threshold,trapped_iterations):
        self.niter = niter
        self.T = T
        self.stepsize = stepsize
        self.minimizer_kwargs = minimizer_kwargs
        self.initial_perturbation = initial_perturbation
        self.trapped_threshold = trapped_threshold
        self.trapped_iterations = trapped_iterations

class worker_essentials:
    def __init__(self, original_contents, timeout, interpolation_timestep, user_function, temp_folder = 'temp_sim_files/'):
        self.original_contents = original_contents
        self.timeout = timeout
        self.interpolation_timestep = interpolation_timestep
        self.user_function = user_function
        self.temp_folder = temp_folder

