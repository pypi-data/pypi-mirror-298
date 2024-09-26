import subprocess
import time
import logging
import os
from spice_utils import create_symbolic_link, remove_symbolic_link, modify_cir_file_with_parameters, modify_output_filename, read_parameters_from_cir
from data_processing import calculate_power_consumption, calculate_total_power_dissipation, calculate_total_energy, interpolate_to_regular_timestep, evaluate_objective_waveforms, replace_functional_waveforms_with_tvps
from spice_utils import parse_outtran
import numpy as np
import pandas as pd
import spice_utils
import uuid
import multiprocessing
import io
import itertools
import workers
import gui
import tkinter as tk
from threading import Thread
import asyncio
import matplotlib.pyplot as plt

def manage_progress_updates(progress_queue, gui_app, work_completed):
    '''
    This function manages the progress updates from the worker processes.
    '''
    while True:
        try:
            if work_completed.is_set():
                return
            while not progress_queue.empty():
                if work_completed.is_set():
                    return
                update_dict = progress_queue.get_nowait()
                gui_app.update_progress(update_dict)

        except queue.Empty:
            continue  # No new results, continue checking

        except Exception as e:
            logging.error(f"Error in manage_progress_updates: {str(e)}")
            continue

def manage_updates(results_queue, gui_app, work_completed):
    '''
    This function manages the result updates from the worker processes.
    '''
    best_result = None
    best_score = float('inf')
    
    while True:
        try:
            if work_completed.is_set():
                return
            while not results_queue.empty():
                if work_completed.is_set():
                    return
                progress_dict = results_queue.get_nowait()

                current_score = progress_dict['score']
                
                if current_score < best_score:
                    best_score = current_score
                    best_result = progress_dict
                    logging.info(f"New best result: Worker {best_result['worker_id']}, Iteration {best_result['iteration']}, Score {best_score:.6f}, Parameters: {best_result['params']}")
                    gui_app.update_best_result(best_result)
                else:
                    logging.info(f"Result of last iteration: no new best result found.")
                    continue
        
        except queue.Empty:
            continue  # No new results, continue checking

        except Exception as e:
            logging.error(f"Error in manage_updates: {str(e)}")
            continue

# def manage_text_io(text_queue, gui_app, work_completed):
#     '''
#     This function manages the text output from the worker processes.
#     '''
#     while True:
#         try:
#             if work_completed.is_set():
#                 return
#             while not text_queue.empty():
#                 if work_completed.is_set():
#                     return
#                 text_output = text_queue.get_nowait()
#                 gui_app.update_text_output(text_output)
        
#         except queue.Empty:
#             continue
        
#         except Exception as e:
#             logging.error(f"Error in manage_text_io: {str(e)}")
#             continue

def multiprocessing_manager(worker_function, work_list, n_processes=4, global_timeout=None, waveforms=None, original_duration=None):
    # Start the GUI in the main thread
    root = tk.Tk()
    app = gui.ProgressGUI(waveforms, global_timeout, original_duration, root)
    # Create a manager and a shared queue
    manager = multiprocessing.Manager()
    results_queue = manager.Queue()
    progress_queue = manager.Queue()

    final_output_queue = multiprocessing.Queue()
    work_completed = multiprocessing.Event()
    
    def run_manager():
        start_time = time.time()
        results = []
        total_jobs = len(work_list)
        completed_jobs = 0
        failed_jobs = 0
        best_score = float('inf')
        best_result = None
        logging.info('starting manager')
        with multiprocessing.Pool(processes=n_processes) as pool:
            args_list = [(*work_item, results_queue, progress_queue) for work_item in work_list]
            for worker_output in pool.imap_unordered(worker_function, args_list):
                if app.stop_requested:
                    logging.info("Stop requested. Exiting gracefully.")
                    break

                completed_jobs += 1
                # logging.info(f"worker output: {worker_output}")
                if worker_output[0] is not None and not worker_output[0].empty and not worker_output[0]['spice_df'].isnull().any().any():
                    results.append(worker_output[0].squeeze())

                    if isinstance(worker_output, tuple) and len(worker_output) > 1:
                        score = worker_output[1]
                        if score < best_score:
                            best_score = score
                            best_result = worker_output[0].squeeze()
                else:
                    if(worker_output[0] is None or worker_output[0].empty or worker_output[0]['spice_df'] is None):
                        logging.error(f"Run failed without a result.")

                    else:
                        logging.error(f"Run failed. Parameters: {worker_output[2].x}")
                    failed_jobs += 1

                elapsed_time = time.time() - start_time
                remaining_jobs = total_jobs - completed_jobs
                estimated_time_left = (elapsed_time / completed_jobs) * remaining_jobs if completed_jobs > 0 else 0

                update_progress(total_jobs, completed_jobs, failed_jobs, best_score, estimated_time_left, app)

                if global_timeout and elapsed_time > global_timeout:
                    logging.warning("\nGlobal timeout reached. Stopping further processing.")
                    pool.terminate()
                    break
        
        print()  # New line after progress bar
        logging.info(f"Total time taken: {time.time() - start_time:.2f} seconds")
        logging.info(f"Total jobs: {total_jobs}, Completed: {completed_jobs}, Failed: {failed_jobs}")
        
        if results:
            # Ensure each result is a DataFrame with at least one row
            dataframe_results = [result.to_frame().T if isinstance(result, pd.Series) else result for result in results]
            all_results = pd.concat(dataframe_results, ignore_index=True)
        else:
            all_results = pd.DataFrame()

    # Check if all_results is a Series and convert it to a DataFrame if necessary
        if isinstance(all_results, pd.Series):
            logging.warning("all_results is a Series.")
        elif not isinstance(all_results, pd.DataFrame):
            logging.warning("all_results is neither a DataFrame nor a Series. It may be empty or invalid.")
            all_results = pd.DataFrame()  # Create an empty DataFrame as a fallback

        # Check if best_result is a Series and convert it to a DataFrame if necessary
        if isinstance(best_result, pd.Series):
            # logging.warning("best_result is a Series.")
            best_result = best_result.to_frame().T
        elif not isinstance(best_result, pd.DataFrame):
            logging.warning("best_result is neither a DataFrame nor a Series. It may be empty or invalid.")
            best_result = pd.DataFrame()  # Create an empty DataFrame as a fallback
        return best_result, all_results

    # Define a function to run the manager and put results in the queue
    def run_manager_and_store_results(final_output_queue, work_completed):
        final_output = run_manager()
        logging.info('done with manager')
        final_output_queue.put(final_output)
        work_completed.set()  # Signal that work is completed

    # Function to check if work is completed and close the GUI
    def check_work_completed():
        if work_completed.is_set():
            root.quit()
            root.destroy()
        else:
            root.after(1000, check_work_completed)  # Check again after 1000ms

    # Start threads for managing progress updates and results
    progress_thread = Thread(target=manage_progress_updates, args=(progress_queue, app, work_completed))
    results_thread = Thread(target=manage_updates, args=(results_queue, app, work_completed))
    manager_thread = Thread(target=run_manager_and_store_results, args=(final_output_queue, work_completed))
    progress_thread.start()
    results_thread.start()
    manager_thread.start()

    # Start checking for work completion
    root.after(1000, check_work_completed)

    # Start the GUI main loop
    root.mainloop()

    # After GUI is closed, wait for the manager thread to finish
    manager_thread.join()
    progress_thread.join()
    results_thread.join()
    # Retrieve the results from the queue
    best_result, all_results = final_output_queue.get()

    return best_result, all_results

def default_user_function(df):
    '''
    A default user function that returns 1. 
    This is used if no user function is provided for optimization (such as in a single simulation scenario)
    '''
    return 1

def run_spicemanager_single(
                        cir_file_path,
                        interpolation_timestep,
                        temp_folder = 'temp_sim_files/',
                    ):
    '''
    Run a SPICE simulation on a single circuit file without any modifications.  
    Extracts output data and returns it as a dataframe.
    '''
    return run_spicemanager(cir_file_path, None, None, 1e7, 1e7, interpolation_timestep, None, None, 1, temp_folder,None,False)[1]
    


def run_spicemanager(
                        cir_file_path,
                        params_to_vary,
                        user_function,
                        process_timeout,
                        global_timeout,
                        interpolation_timestep,
                        mode,
                        mode_args,
                        n_processes=4,
                        temp_folder = 'temp_sim_files/',
                        waveforms = None,
                        randomize_params = True,
                    ):
    '''
    Automates the process of running simulations for a range of parameters and user-defined functions.
    Args:
        cir_file_path (str): The path to the circuit file to be simulated.
        params_to_vary (dict): A dictionary where keys are parameter names and values are lists of parameter values to try.
        user_function (function): A function that takes a DataFrame and returns a scalar value for optimization.
        process_timeout (float): The timeout for each individual simulation process.
        global_timeout (float): The maximum time for the entire simulation to run (it will stop all simulations at the end of this time)
        interpolation_timestep (float): The timestep for interpolation of the simulation results in the output file.
        mode (str): The mode of simulation, either 'basinhopping' or 'grid'.
        mode_args (object): Additional arguments specific to the mode of simulation.
        n_processes (int): The number of processes to run in parallel.
        temp_folder (str): The folder to store temporary files such as modified circuits and output files.
        waveforms (list): A list of dictionaries specifying the objective waveforms for waveform-matching optimization.
    '''
    #get rid of old temp files if they exist
    spice_utils.cleanup_temp_files(temp_folder)
    
    #set default values for optional parameters
    if(params_to_vary is None):
        params_to_vary = {'dummy_param': [0,0.5,1]}
    if(mode is None):
        mode = 'grid'
        mode_args = None
    if(user_function is None):
        user_function = default_user_function
    if(waveforms is None):
        waveforms = []
    else:
        waveforms = replace_functional_waveforms_with_tvps(waveforms, interpolation_timestep)

    
    # Read the contents of the circuit file
    with open(cir_file_path, 'r') as file:
        original_contents = file.read()
    worker_essentials_instance = workers.worker_essentials(original_contents, process_timeout, interpolation_timestep, user_function, temp_folder)
    
    original_duration = spice_utils.read_simulation_duration(original_contents)
    if original_duration is not None:
        print(f"Simulation duration: {original_duration} seconds")
    else:
        logging.error("Simulation duration not found in the circuit file.")
        return None,None
    
    #generate the work list and worker function based on the mode
    #this determines the manner of how the parameter space is explored
    if mode == 'basinhopping':
        if isinstance(mode_args, workers.BasinhoppingParams):
            work_list = workers.generate_basinhopping_work_list(worker_essentials_instance, params_to_vary, mode_args, n_processes)
        else:
            raise ValueError("mode_args must be an instance of BasinhoppingParams for basinhopping mode")
        worker_function = workers.worker_basinhopping   
    elif mode == 'grid':
        work_list = workers.generate_grid_work_list(worker_essentials_instance, params_to_vary, randomize=randomize_params)
        worker_function = workers.worker_grid
    else:
        raise ValueError(f"Invalid mode: {mode}")
    
    if multiprocessing.get_start_method() != 'fork':
        multiprocessing.set_start_method('fork', force=True)

    #run the simulations and collect the results
    best_result, all_results = multiprocessing_manager(worker_function, work_list, n_processes, global_timeout, waveforms, original_duration)
    
    plt.close()
    
    #two dataframes are returned, one containing the best result, relevant to the case where an optimization was performed, and all the results, which can be used to visualize the parameter space exploration
    return best_result, all_results

def submit_new_job(cir_file_contents,timeout,progress_queue,temp_folder = 'temp_sim_files/'):

    this_uuid = str(uuid.uuid4())
    output_file_name = "outtran" + this_uuid + ".raw"
    cir_file_contents = spice_utils.modify_output_filename(cir_file_contents,output_file_name)
    temp_cir = temp_folder + 'temp_circuit' + this_uuid + ".cir"

    # Write using io.open with explicit encoding and line ending
    with io.open(temp_cir, 'w', encoding='utf-8', newline='\n') as file:
        file.write(cir_file_contents)
        
    new_process = ngspice_process(temp_cir,timeout)
    new_process.run_simulation()
    result = new_process.check_for_errors_and_update_progress(progress_queue)
    if result:
        spice_df = parse_outtran(output_file_name, temp_folder)
        try:
            os.remove(temp_cir)
        except OSError:
            pass
        try:
            # print('test')
            os.remove(temp_folder + output_file_name)
        except OSError:
            pass
        return spice_df
    else:
        try:
            os.remove(temp_cir)
        except OSError:
            pass
        try:
            # print('test')
            os.remove(temp_folder + output_file_name)
        except OSError:
            pass
        return None

def build_result_df(original_contents,spice_df,params,voltage_sources,interpolation_timestep):
    #first add the time-dependent postprocessing columns
    df = interpolate_to_regular_timestep(spice_df,interpolation_timestep)
    df = calculate_power_consumption(df,voltage_sources,params)
    df = calculate_total_power_dissipation(df)
    

    result_df = pd.DataFrame({
        'cir_file_orig_contents': [original_contents],
        'total_energy': [calculate_total_energy(df)],
        'spice_df': [df]
    })

    # Add parameters as separate columns
    for key, value in params.items():
        result_df[f'{key}'] = [value]

    return result_df

def prepare_and_run_new_job(original_contents,input_params,timeout,interpolation_timestep, progress_queue, temp_folder = 'temp_sim_files/'):
    new_contents = spice_utils.modify_cir_with_param_dict(original_contents, input_params)
    all_params = spice_utils.read_parameters_from_cir_contents(new_contents)
    voltage_sources = spice_utils.identify_voltage_sources(new_contents)
    
    spice_df = submit_new_job(new_contents,timeout,progress_queue,temp_folder)
    
    if(spice_df is None):
        return pd.DataFrame()
    
    result_df =  build_result_df(original_contents,spice_df,all_params,voltage_sources,interpolation_timestep)
    if(result_df is None):
        return pd.DataFrame()
    return result_df
    

def update_progress(total_jobs, completed_jobs, failed_jobs, best_score, remaining_time, gui_app):
    progress_bar_length = 50
    progress = completed_jobs / total_jobs
    filled_length = int(progress_bar_length * progress)
    bar = '=' * filled_length + '-' * (progress_bar_length - filled_length)
    text_output = f'\rProgress: [{bar}] {completed_jobs}/{total_jobs} | Failed: {failed_jobs} | Best Score: {best_score:.6f} | Time left: {remaining_time:.2f}s'
    gui_app.update_text_output(text_output)
    #might need to use the text io queue later to make it thread safe, but it seems to work fine without it for now


class ngspice_process:
    """Interface for running NGSpice in batch mode."""
    def __init__(self, cir_file, timeout):
        self.cir_file=cir_file
        self.timeout=timeout
        self.process = None
        self.start_time = 0
        
    def run_simulation(self):
        self.start_time = time.time()
        self.process = subprocess.Popen(['ngspice', '-b', self.cir_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def check_for_errors_and_update_progress(self, progress_queue):
        start_time = time.time()
        while self.process.poll() is None:
            if time.time() - start_time > self.timeout:
                logging.error("NGSpice simulation timed out.")
                self.process.kill()
                return False
            
            time.sleep(0.05)  # Wait for 50 ms
            
            # Check for any output
            output = self.process.stdout.readline().strip()

            if output and ("reference value" in output.lower()):
                # Extract the reference value after the string
                reference_value = float(output.split("Reference value :  ")[1].strip())
                progress_queue.put({'worker_id': self.process.pid, 'progress': reference_value})
            
            if output and ("error" in output.lower() and ( "timestep too small" in output.lower() or "simulation(s) aborted"  or "no simulations run" or "fatal error" in output.lower())):
                logging.error(f"Error detected in NGSpice output: {output}")
                self.process.kill()
                return False

        # Process has exited, check return code and any remaining output
        return_code = self.process.returncode
        remaining_output, errors = self.process.communicate()

        if return_code != 0:
            logging.error(f"NGSpice process exited with non-zero return code: {return_code}")
            if errors:
                logging.error(f"NGSpice errors: {errors}")
            return False

        if errors and not errors.startswith("Using"):
            logging.error(f"NGSpice errors: {errors}")
            return False

        # logging.info("NGSpice simulation completed successfully.")
        return True
        