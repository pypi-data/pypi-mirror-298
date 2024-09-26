import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline, PchipInterpolator
import logging
import matplotlib.pyplot as plt
from spice_utils import parse_outtran, parse_variable_names

def calculate_power_consumption(df, voltage_sources,all_params):
    """Calculate power consumption over the simulation duration."""
    if df is None:
        return None
    power_columns = {}
    for source in voltage_sources:
        current_col = f"i({source.name.lower()})"
        if current_col in df.columns:
            voltage_value = all_params.get(source.parameter_name, None)
            if voltage_value is None:
                logging.error(f"Parameter value for {source.parameter_name} not found. Skipping power calculation for {source.name}.")
                continue
            power_column = f"p({source.name})"
            try:
                df[power_column] = df[current_col] * (-1) *voltage_value
                power_columns[power_column] = power_column
            except Exception as e:
                logging.error(f"Error calculating power for {source.name}: {e}")
        else:
            logging.error(f"Current column {current_col} not found in simulation data. Skipping power calculation for {source.name}.")
    return df

def calculate_total_power_dissipation(df):
    """Calculate total power dissipation over the simulation duration."""
    if df is None:
        return None
    power_columns = [col for col in df.columns if col.startswith('p(')]
    if power_columns:
        df['p(total)'] = df[power_columns].sum(axis=1)
    else:
        logging.error("No power columns found to calculate total power dissipation.")
    return df

def calculate_total_energy(df):
    """Calculate total energy consumed by the circuit over the entire simulation."""
    if df is None:
        return None
    if 'p(total)' not in df.columns:
        logging.error("Total power dissipation column 'p(total)' not found in the DataFrame.")
        return float('inf')
    try:
        energy = np.trapz(df['p(total)'], df['time'])
        return energy
    except Exception as e:
        logging.error(f"Error calculating total energy: {e}")
        return float('inf')

def interpolate_to_regular_timestep(df, timestep):
    """
    Interpolate the DataFrame to a regular timestep.

    Parameters:
    df (pd.DataFrame): The input DataFrame with simulation results.
    timestep (float): The desired regular timestep.

    Returns:
    pd.DataFrame: The interpolated DataFrame.
    """
    if df is None:
        # logging.error("Input DataFrame is None.")
        return None
    
    if 'time' not in df.columns:
        logging.error("The DataFrame does not contain a 'time' column.")
        return df

    if df.empty:
        logging.warning("Input DataFrame is empty.")
        return df

    if timestep <= 0:
        logging.error("Timestep must be positive.")
        return df

    # Create a new time index with regular intervals
    min_time = df['time'].min()
    max_time = df['time'].max()
    regular_time_index = np.arange(min_time, max_time + timestep, timestep)

    # Create a new DataFrame with the regular time index
    interpolated_df = pd.DataFrame({'time': regular_time_index})

    # Interpolate each column separately
    for column in df.columns:
        if column != 'time':
            interpolated_df[column] = np.interp(regular_time_index, df['time'], df[column])

    return interpolated_df

def generate_waveform(function, fixed_timestep):
    """
    Generate a waveform based on a given function and fixed timestep.

    Parameters:
    function (callable): A function that takes time as input and returns the waveform value.
    fixed_timestep (float): The desired fixed timestep for the output waveform.

    Returns:
    numpy.ndarray: A 2D array with columns [time, value] representing the generated waveform.
    """
    # Determine the time range (assuming 0 to 1 second, adjust as needed)
    start_time = 0
    end_time = 1

    # Create a time array with the fixed timestep
    times = np.arange(start_time, end_time + fixed_timestep, fixed_timestep)

    # Calculate the waveform values using the provided function
    values = np.array([function(t) for t in times])

    # Combine time and values into a 2D array
    return np.column_stack((times, values))

def replace_functional_waveforms_with_tvps(waveforms, timestep):
    for waveform in waveforms:
        if 'function' in waveform:
            try:
                function = waveform['function']
                time_start = waveform.get('time_start', 0)
                time_end = waveform.get('time_end', 0)
                times = np.arange(time_start, time_end + timestep, timestep)
                values = np.array([function(t) for t in times])
                time_value_pairs = list(zip(times, values))
                waveform['time_value_pairs'] = time_value_pairs
                del waveform['function']
            except Exception as e:
                logging.error(f"Error replacing functional waveform with time-value pairs: {e}")
    return waveforms

def generate_waveform(time_value_pairs, fixed_timestep, interpolation_method='linear'):
    """
    Generate a waveform based on user-specified time-value pairs and a fixed timestep.

    Parameters:
    time_value_pairs (list of tuples): List of (time, value) pairs defining the waveform.
    fixed_timestep (float): The desired fixed timestep for the output waveform.
    interpolation_method (str): The interpolation method to use ('linear', 'bezier', or 'hermite').

    Returns:
    numpy.ndarray: A 2D array with columns [time, value] representing the interpolated waveform.
    """
    # Sort the time-value pairs by time
    sorted_pairs = sorted(time_value_pairs, key=lambda x: x[0])

    # Extract times and values
    times, values = zip(*sorted_pairs)

    # Create a new time array with the fixed timestep
    start_time = times[0]
    end_time = times[-1]
    new_times = np.arange(start_time, end_time + fixed_timestep, fixed_timestep)

    if interpolation_method == 'linear':
        # Linear interpolation
        interpolated_values = np.interp(new_times, times, values)
    elif interpolation_method == 'bezier':
        # Bezier interpolation
        spline = make_interp_spline(times, values, k=3)
        interpolated_values = spline(new_times)
    elif interpolation_method == 'hermite':
        # Hermite spline interpolation
        pchip = PchipInterpolator(times, values)
        interpolated_values = pchip(new_times)
    else:
        raise ValueError("Invalid interpolation method. Choose 'linear', 'bezier', or 'hermite'.")

    # Combine time and interpolated values into a 2D array
    return np.column_stack((new_times, interpolated_values))

def deviational_loss(y_true, y_pred, deviation_size, power=2):
    """
    Calculate the deviational loss between true and predicted values.
    This method is used to penalize absolute deviations from the desired waveform.
    It allows functions with widely ranging values to be accommodated more neutrally.
    
    The scale of the return value is related to the average number of deviations between 
    the desired and actual waveforms. Values on the order of 1 indicate well-matched 
    functions with about one deviation of error. The loss increases substantially 
    for each additional deviation.
    
    Parameters:
    y_true (array-like): True values.
    y_pred (array-like): Predicted values.
    deviation_size (float): The size of the deviation considered significant.
    power (int, optional): The power to which the loss is raised when the error is greater than 1 deviation. Default is 2.
    
    Returns:
    float: The deviational loss.
    
    Raises:
    ValueError: If y_true and y_pred have different lengths.
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if len(y_true) == 0:
        raise ValueError("Input arrays cannot be empty")
    error = y_true - y_pred
    normalized_error = np.abs(error) / deviation_size
    thresholded_error = np.where(normalized_error > 1, normalized_error ** power, normalized_error)
    normalized_total_loss = np.sum(thresholded_error) / len(y_true)
    # logging.info(f"Final deviational loss: {normalized_total_loss}")
    return normalized_total_loss

def evaluate_objective_waveforms(waveforms, df):
    """
    Evaluate how well the simulation results match the specified waveforms.  Uses a heuristic loss function that penalizes deviations from the desired waveform.
    
    Parameters:
    waveforms (list): List of dictionaries specifying desired waveforms.
    df (pd.DataFrame): DataFrame containing simulation results.
    
    Returns:
    float: Product of scores for all waveforms.
    """
    # Check if the DataFrame contains a single-simulation DataFrame as one of its columns
    if 'spice_df' in df.columns:
        df = df['spice_df'].iloc[0]
    elif 'time' in df.columns:
        df = df
    else:
        logging.error("No time column found in the DataFrame, or invalid DataFrame format. Skipping waveform evaluation.")
        return float('inf')
    
    # Convert all waveforms to time-value pairs
    timestep = df['time'].diff().mean()
    waveforms = replace_functional_waveforms_with_tvps(waveforms, timestep)
    
    scores = []
    
    for waveform in waveforms:
        variable = waveform['variable']
        
        if variable not in df.columns:
            logging.warning(f"Variable {variable} not found in simulation results. Skipping this waveform.")
            continue
        
        time_value_pairs = waveform['time_value_pairs']
        desired_waveform = generate_waveform(time_value_pairs, timestep, interpolation_method=waveform.get('interpolation_method', 'linear'))

        # Interpolate the simulation results to match the desired waveform time points
        simulated_values = np.interp(desired_waveform[:, 0], df['time'], df[variable])
        
        deviation_size = waveform.get('deviation_size', 0.1)
        multiplier = waveform.get('multiplier', 1.0)
        power = waveform.get('power', 2)
        score = deviational_loss(desired_waveform[:, 1], simulated_values, deviation_size, power)
        
        scores.append(score)
    
    # Return the product of all scores
    if any(score is None for score in scores):
        raise ValueError("One or more scores are None. Check your waveform evaluation.")
    return np.prod(scores) if scores else float('inf')


def plot_waveforms(result_df, waveforms, ax):
    ax.clear()
    for waveform in waveforms:
        variable = waveform['variable']
        desired_times, desired_values = zip(*waveform['time_value_pairs'])
        normalized_desired_values = (desired_values - min(desired_values)) / (max(desired_values) - min(desired_values))
        ax.plot(desired_times, normalized_desired_values, linestyle='--', label=f'Desired {variable}')

        if variable in result_df.columns:
            simulated_values = result_df[variable]
            normalized_simulated_values = (simulated_values - min(desired_values)) / (max(desired_values) - min(desired_values))
            ax.plot(result_df['time'], normalized_simulated_values, label=f'Simulated {variable}')

    ax.legend()
    
    
def simple_plot(result_df, variables):
    '''
    Plots the simulation results of one run for the specified variables.  If there are multiple variables, they will be plotted in subplots.
    If a dataframe is passed with multiple simulations, only the first one will be plotted.
    Parameters:
    result_df (pd.DataFrame): DataFrame containing the simulation results of one run.
    variables (list): List of variables to plot.
    '''
    
    #if all_results is passed, extract the spice_df from it
    if isinstance(result_df, pd.DataFrame) and 'spice_df' in result_df.columns:
        df = result_df['spice_df'].iloc[0]
    elif isinstance(result_df, pd.DataFrame):
        df = result_df
    else:
        raise TypeError("Invalid DataFrame format. Must contain 'spice_df' column.")
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError("'spice_df' is not a pandas DataFrame")
    
    if 'time' not in df.columns:
        raise KeyError("'time' column not found in spice_df")
    
    num_vars = len(variables)
    if num_vars == 0:
        raise ValueError("No variables provided to plot")
    
    fig, axs = plt.subplots(num_vars, 1, figsize=(10, 4*num_vars), sharex=True)
    axs = [axs] if num_vars == 1 else axs
    
    for i, variable in enumerate(variables):
        if variable not in df.columns:
            logging.warning(f"Variable '{variable}' not found in spice_df. Skipping.")
            continue
        
        ax = axs[i]
        ax.plot(df['time'], df[variable])
        ax.set_ylabel('Voltage (V)')
        ax.set_title(f'{variable}')
        ax.grid(True)
    
    axs[-1].set_xlabel('Time (s)')
    fig.suptitle('Simulation Results', fontsize=16)
    plt.tight_layout()
    plt.show()
    

        
def plot_sweep_result(all_results, variable, parameters_to_compare):
    '''
    Plots the simulation results of multiple runs for a specified variable.

    Parameters:
    all_results (pd.DataFrame): DataFrame containing the simulation results of multiple runs.
    variable (str): The variable to plot.
    parameters_to_compare (list): List of parameter names to include in the legend.
    '''
    if 'spice_df' not in all_results.columns:
        raise KeyError("'spice_df' not found in all_results")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for index, row in all_results.iterrows():
        df = row['spice_df']
        if not isinstance(df, pd.DataFrame):
            logging.warning(f"'spice_df' at index {index} is not a pandas DataFrame. Skipping.")
            continue
        
        if 'time' not in df.columns or variable not in df.columns:
            logging.warning(f"Required columns not found in spice_df at index {index}. Skipping.")
            continue
        
        # Create label with specified parameters
        label_parts = []
        for param in parameters_to_compare:
            if param in row.index:
                label_parts.append(f"{param}={row[param]:.2e}")
            else:
                logging.warning(f"Parameter '{param}' not found in results. Skipping in label.")
        
        label = ', '.join(label_parts)
        ax.plot(df['time'], df[variable], label=label)
    
    ax.set_xlabel('Time (s)')
    ax.set_ylabel(f'{variable}')
    ax.set_title(f'Results for {variable}')
    ax.grid(True)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()