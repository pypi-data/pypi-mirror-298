import re
import logging
import os
import shutil
import pyperclip
import numpy as np
import pandas as pd
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Mapping SPICE notation to scientific notation
SPICE_TO_SCI_NOTATION = {
    'p': 'e-12',
    'n': 'e-9',
    'u': 'e-6',
    'm': 'e-3',
    'k': 'e3',
    'meg': 'e6',
    'g': 'e9',
    't': 'e12'
}

def convert_spice_to_sci(value):
    """Convert SPICE notation to scientific notation."""
    match = re.match(r'(-?\d*\.?\d+)([pnumbkmegKtT]?)', value)
    if match:
        number, suffix = match.groups()
        if suffix in SPICE_TO_SCI_NOTATION:
            return float(f'{number}{SPICE_TO_SCI_NOTATION[suffix]}')
        return float(number)
    return float(value)

def read_parameters_from_cir(filename):
    """Read parameters from a .cir file."""
    parameters = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip().startswith('.param'):
                param_match = re.match(r'\.param\s+(\S+)\s*=\s*(\S+)', line.strip())
                if param_match:
                    param_name = param_match.group(1)
                    param_value = param_match.group(2)
                    # Handle scientific notation
                    if 'e' in param_value.lower() or 'E' in param_value:
                        param_value = float(param_value)
                    else:
                        param_value = convert_spice_to_sci(param_value)
                    parameters[param_name] = param_value  # Store the parameter value directly
    return parameters

def read_simulation_duration(cir_contents):
    """
    Read the simulation duration from the circuit contents.

    Args:
    cir_contents (str): The contents of the .cir file as a string.

    Returns:
    float: The simulation duration in seconds, or None if not found.
    """
    # Regular expression to match the tran command
    tran_pattern = r'tran\s+(\S+)\s+(\S+)'
    
    match = re.search(tran_pattern, cir_contents, re.IGNORECASE)
    if match:
        stop_time = match.group(2)
        return convert_spice_to_sci(stop_time)
    
    return None

def read_parameters_from_cir_contents(contents):
    """Read parameters from a .cir file contents."""
    parameters = {}
    
    if not contents:
        logging.info("No parameters to read")
        return parameters
    
    for line in contents.splitlines():
        if line.strip().startswith('.param'):
            param_match = re.match(r'\.param\s+(\S+)\s*=\s*(\S+)', line.strip())
            if param_match:
                param_name = param_match.group(1)
                param_value = param_match.group(2)
                
                # Handle scientific notation
                if 'e' in param_value.lower() or 'E' in param_value:
                    param_value = float(param_value)
                else:
                    param_value = convert_spice_to_sci(param_value)
                
                parameters[param_name] = param_value  # Store the parameter value directly
    
    return parameters

def format_and_copy_parameters(parameters):
    """Format parameters for copying to clipboard."""
    formatted_params = "parameters_to_sweep = {\n"
    formatted_params += ",\n".join([f"    '{name}': {values}" for name, values in parameters.items()])
    formatted_params += "\n}"
    # logging.info("Formatted parameters: \n%s", formatted_params)
    pyperclip.copy(formatted_params)
    logging.info("Parameters have been copied to the clipboard.")

def extract_and_format_parameters(filename):
    """Extract and format parameters from a .cir file."""
    parameters = read_parameters_from_cir(filename)
    format_and_copy_parameters(parameters)
    return parameters

def create_symbolic_link(subcircuit_path, link_name):
    """Create a symbolic link for subcircuit directory if it doesn't already exist correctly."""
    try:
        if os.path.islink(link_name):
            existing_target = os.readlink(link_name)
            if os.path.abspath(existing_target) == os.path.abspath(subcircuit_path):
                return
            else:
                os.remove(link_name)
        
        elif os.path.exists(link_name):
            if os.path.isdir(link_name):
                shutil.rmtree(link_name)
            else:
                os.remove(link_name)
        
        os.symlink(subcircuit_path, link_name, target_is_directory=True)
    except OSError as e:
        logging.error("Failed to create symbolic link: %s", e)

def remove_symbolic_link(link_name):
    """Remove a symbolic link."""
    try:
        if os.path.islink(link_name):
            os.remove(link_name)
    except OSError as e:
        logging.error("Failed to remove symbolic link: %s", e)

def modify_cir_file_with_parameters(contents, param_names, values):
    """Modify .cir file contents with given parameters."""
    if param_names is None:
        param_names = []
    if values is None:
        values = []
    param_dict = dict(zip(param_names, values))
    new_contents = []
    for line in contents:
        if line.strip().startswith('.param'):
            param_match = re.match(r'\.param\s+(\S+)\s*=\s*(\S+)', line.strip())
            if param_match:
                param_name = param_match.group(1)
                default_value = param_match.group(2)
                if param_name in param_dict:
                    new_value = param_dict[param_name]
                    if np.isnan(new_value):
                        logging.error(f"NaN value detected for parameter {param_name}. Using default value: {default_value}")
                    else:
                        line = f'.param {param_name} = {new_value:.6e}\n'
        elif line.strip().startswith('.inc'):
            line = re.sub(r'(\.inc\s+)(\S+)', r'\1subcircuits/\2', line)
        new_contents.append(line)
    return new_contents



def modify_cir_with_param_dict(contents, param_dict):
    """Modify .cir file contents with given parameters."""
    if param_dict is None:
        # logging.info("No parameters to modify")
        return contents

    new_contents = []
    for line in contents.splitlines():  # Split the string into lines
        if line.strip().startswith('.param'):
            param_match = re.match(r'\.param\s+(\S+)\s*=\s*(\S+)', line.strip())
            if param_match:
                param_name = param_match.group(1)
                default_value = param_match.group(2)
                if param_name in param_dict:
                    new_value = param_dict[param_name]
                    if new_value is None or (isinstance(new_value, float) and np.isnan(new_value)):
                        logging.error(f"Invalid value {new_value} detected for parameter {param_name}. Using default value: {default_value}")
                    else:
                        line = f'.param {param_name} = {new_value:.6e}'
        elif line.strip().startswith('.inc'):
            line = re.sub(r'(\.inc\s+)(\S+)', r'\1subcircuits/\2', line)
        new_contents.append(line)
    return '\n'.join(new_contents)  # Join the list into a single string




def modify_output_filename(contents, output_filename):
    """Modify the .cir file contents to write to a specified output file."""
    new_contents = []
    for line in contents.split('\n'):
        if line.strip().startswith('write'):
            line = re.sub(r'(write\s+\S+/)(\S+)', rf'\1{output_filename}', line)
        new_contents.append(line)
    # logging.info(f"Modified output filename to {output_filename}")
    return '\n'.join(new_contents)

def cleanup_temp_files(temp_dir):
    """Delete all temporary outtran and circuit files in the given directory and remove symbolic link."""
    print('cleanup')
    for filename in os.listdir(temp_dir):
        if (filename.startswith("temp_") and filename.endswith(".cir")) or \
           (filename.endswith(".raw")):
            file_path = os.path.join(temp_dir, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                logging.error(f"Error deleting file {file_path}: {str(e)}")
    
    # Remove symbolic link
    subcircuit_link = os.path.join(temp_dir, 'subcircuits')
    remove_symbolic_link(subcircuit_link)
    remove_symbolic_link(subcircuit_link)
    
def parse_variable_names(lines):
    variable_names = []
    parsing_variables = False
    data_start_index = 0

    for i, line in enumerate(lines):
        if line.startswith("Variables:"):
            parsing_variables = True
            continue
        if parsing_variables:
            if line.strip() == "Values:":
                data_start_index = i + 1
                break
            parts = line.split()
            if len(parts) > 2:
                variable_names.append(parts[1])  # Take the variable name and ignore the rest
    
    return variable_names, data_start_index

# Function to parse the outtran.raw file
def parse_outtran(file_path, temp_folder = 'temp_sim_files/'):
    with open(temp_folder + file_path, 'r') as file:
        lines = file.readlines()
    
    variable_names, data_start_index = parse_variable_names(lines)

    # Prepare containers for storing parsed data
    timestep_data = []
    current_timestep = []

    # Read the data lines
    for line in lines[data_start_index:]:
        if line.strip() == "":
            continue
        values = line.split()
        if len(values) == 2:  # Indicates the start of a new timestep
            if current_timestep:
                timestep_data.append(current_timestep)
            current_timestep = [float(values[1])]  # Start with the time value
        else:
            current_timestep.append(float(values[0]))

    # Add the last timestep data
    if current_timestep:
        timestep_data.append(current_timestep)

    # Convert to DataFrame
    columns = ['time'] + variable_names[1:]  # Adjust columns to match data structure
    df = pd.DataFrame(timestep_data, columns=columns)
    
    return df

class SpiceSource:
    def __init__(self, name, node, parameter_name):
        self.name = name
        self.node = node
        self.parameter_name = parameter_name

def identify_voltage_sources(contents):
    """Identify voltage sources in the .cir file contents."""
    voltage_sources = []
    for line in contents.splitlines():
        if re.match(r'^[vV]', line):
            parts = line.split()
            if len(parts) > 2 and 'DC' in parts:
                name = parts[0]
                node = parts[1]
                parameter_name = parts[-1].strip("'")
                voltage_sources.append(SpiceSource(name, node, parameter_name))
    return voltage_sources



def prepare_cir_for_ngspice_input(contents,parameters):
    """Prepare the .cir file contents for server input.  Modify the parameters, add the server line headers, and return the modified contents."""
    contents = modify_cir_with_param_dict(contents, parameters)
    new_contents = strip_spice_comments(contents)
    # new_contents = add_circbyline_prefix(new_contents)    
    return new_contents


def add_circbyline_prefix(contents):
    """Add 'circbyline ' to the beginning of every line in a string."""
    lines = contents.split('\n')
    prefixed_lines = ['circbyline ' + line for line in lines]
    return '\n'.join(prefixed_lines)

def strip_spice_comments(contents):
    """Strip all comments from the .cir file contents."""
    lines = contents.split('\n')
    stripped_lines = [line.split('*')[0] for line in lines]
    return '\n'.join(stripped_lines)

def modify_transient_simulation(cir_contents, step_size=None, stop_time=None, start_time=None, max_step=None):
    """
    Modify the transient simulation parameters in a .cir file.

    Args:
    cir_contents (str): The contents of the .cir file as a string.
    step_size (str): The new step size for the transient simulation (e.g., '1p').
    stop_time (str): The new stop time for the transient simulation (e.g., '50n').
    start_time (str): The new start time for the transient simulation (e.g., '0').
    max_step (str): The new maximum step size for the transient simulation (e.g., '1p').

    Returns:
    str: The modified contents of the .cir file.
    """
    # Regular expression to match the tran command
    tran_pattern = r'(tran\s+)(\S+)(\s+)(\S+)(\s+)(\S+)?(\s+)?(\S+)?'

    def replace_tran(match):
        new_step = step_size if step_size is not None else match.group(2)
        new_stop = stop_time if stop_time is not None else match.group(4)
        new_start = start_time if start_time is not None else match.group(6) or '0'
        new_max = max_step if max_step is not None else match.group(8) or new_step

        return f"tran {new_step} {new_stop} {new_start} {new_max}"

    # Replace the tran command parameters
    modified_contents = re.sub(tran_pattern, replace_tran, cir_contents, flags=re.IGNORECASE)

    return modified_contents

def get_value_at_time(spice_df, variable, time):
    """Get the value of a variable at a specific time from a dataframe."""
    value = spice_df.loc[(spice_df['time'] - time).abs().idxmin(), variable]
    return value

def get_values_in_time_range(spice_df, variable, time_range):
    """Get the values of a variable within a specific time range from a dataframe."""
    values = spice_df.loc[(spice_df['time'] >= time_range[0]) & (spice_df['time'] <= time_range[1]), variable]
    return values