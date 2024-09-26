import tkinter as tk
from tkinter import ttk
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import logging
import json  # Add this import for saving progress_dict to a file
import os
class ProgressGUI:
    def __init__(self, waveforms, global_timeout, original_duration, root):
        
        self.stop_requested = False
        self.start_time = time.time()
        self.global_timeout = global_timeout  # Store the global timeout
        self.original_duration = original_duration
        
        self.waveforms = waveforms
        self.root = root
        self.root.title("Simulation Progress")

        # Main frame
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Timer frame
        self.timer_frame = tk.Frame(self.main_frame)
        self.timer_frame.pack(fill=tk.X, pady=(0, 10))

        self.label = tk.Label(self.timer_frame, text="Elapsed Time: 0s / 0s", font=("Helvetica", 16))
        self.label.pack(side=tk.LEFT)

        # Best result frame
        self.best_result_frame = tk.Frame(self.main_frame)
        self.best_result_frame.pack(fill=tk.X, pady=(0, 10))

        self.best_score_label = tk.Label(self.best_result_frame, text="Best Score: N/A", font=("Helvetica", 16))
        self.best_score_label.pack(side=tk.LEFT)

        self.best_params_label = tk.Label(self.best_result_frame, text="Best Parameters:", font=("Helvetica", 16))
        self.best_params_label.pack(side=tk.LEFT, padx=(10, 0))

        # Parameters frame
        self.params_frame = tk.Frame(self.main_frame)
        self.params_frame.pack(fill=tk.X, pady=(0, 10))

        self.params_text = tk.Text(self.params_frame, height=10, font=("Helvetica", 16), wrap=tk.WORD)
        self.params_text.pack(fill=tk.BOTH, expand=True)

        # Stop button
        self.stop_button = tk.Button(self.main_frame, text="Stop Simulations", command=self.request_stop, font=("Helvetica", 14))
        self.stop_button.pack(pady=(10, 20))

        # Plot frame
        if(self.waveforms):
            self.plot_frame = tk.Frame(self.main_frame)
            self.plot_frame.pack(fill=tk.BOTH, expand=True)
            self.fig, self.ax = plt.subplots(figsize=(8, 6))
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.update_timer()

        # Workers frame
        self.workers_frame = tk.Frame(self.main_frame)
        self.workers_frame.pack(fill=tk.X, pady=(0, 10))

        self.workers_label = tk.Label(self.workers_frame, text="Workers Progress:", font=("Helvetica", 16))
        self.workers_label.pack(anchor=tk.W)

        self.workers_tree = ttk.Treeview(self.workers_frame, columns=('Worker', 'Progress'), show='headings')
        self.workers_tree.heading('Worker', text='Worker ID')
        self.workers_tree.heading('Progress', text='Progress')
        self.workers_tree.pack(fill=tk.X, expand=True)

        self.workers_progress = {}
        
        # Text output frame 
        self.text_output_frame = tk.Frame(self.main_frame)
        self.text_output_frame.pack(fill=tk.X, pady=(0, 10))

        self.text_output_label = tk.Label(self.text_output_frame, text="Text Output:", font=("Helvetica", 16))
        self.text_output_label.pack(anchor=tk.W)

        self.text_output = tk.Text(self.text_output_frame, height=5, font=("Helvetica", 12), wrap=tk.WORD)
        self.text_output.pack(fill=tk.X, expand=True)
        self.text_output.config(state=tk.DISABLED)

    def update_timer(self):
        if not self.stop_requested:
            elapsed_time = int(time.time() - self.start_time)
            remaining_time = max(0, self.global_timeout - elapsed_time)
            self.label.config(text=f"Elapsed Time: {elapsed_time}s / {self.global_timeout}s")
            if remaining_time > 0:
                self.root.after(1000, self.update_timer)
            else:
                self.request_stop()


    

    def update_best_result(self, progress_dict):
        self.best_progress_dict = progress_dict  # Save the best progress_dict
        self.best_score_label.config(text=f"Best Score: {progress_dict['score']:.2f}")
        params_text = "\n".join([f"{key}: {value:.2e}" for key, value in progress_dict['params'].items()])
        self.params_text.delete(1.0, tk.END)
        self.params_text.insert(tk.END, params_text)
        
        # Extract and plot the best result data
        result_df = progress_dict['result_df']
        extracted_data = self.extract_waveform_data(result_df, self.waveforms)
        self.root.after(0, self.plot_combined_waveforms, extracted_data)

    def extract_waveform_data(self, result_df, waveforms):
        if 'spice_df' in result_df.columns:
            spice_df = result_df['spice_df'].iloc[0]
        else:
            logging.error("No 'spice_df' column found in the result DataFrame.")
            return None

        extracted_data = {}
        for waveform in waveforms:
            variable = waveform['variable']
            if variable in spice_df.columns:
                desired_times, desired_values = zip(*waveform['time_value_pairs'])
                min_val = min(desired_values)
                max_val = max(desired_values)
                normalized_simulated_values = (spice_df[variable].values - min_val) / (max_val - min_val)
                extracted_data[variable] = {
                    'time': spice_df['time'].values,
                    'values': normalized_simulated_values,
                    'desired_times': desired_times,
                    'desired_values': [(val - min_val) / (max_val - min_val) for val in desired_values]
                }
            else:
                logging.warning(f"Variable {variable} not found in simulation results.")
        
        return extracted_data

    def plot_combined_waveforms(self, extracted_data):
        if not self.waveforms:
            return
        
        # Clear the previous plot
        self.ax.clear()
        
        for variable, data in extracted_data.items():
            # Plot desired waveform
            self.ax.plot(data['desired_times'], data['desired_values'], label=f'{variable} (Desired)', linestyle='-')
            # Plot simulated waveform
            self.ax.plot(data['time'], data['values'], label=f'{variable} (Simulated)', linestyle='--')
        
        self.ax.set_title('Waveform Comparison')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Normalized Value')
        self.ax.legend()
        self.ax.grid(True)

        # Redraw the canvas
        self.canvas.draw()

    def request_stop(self):
        self.stop_requested = True
        self.save_best_progress()
        os._exit(0)  # Forcibly exit the entire Python process
        

        
    def save_best_progress(self):
        if self.best_progress_dict:
            if self.best_progress_dict['result_df'] is not None:
                self.best_progress_dict['result_df'].to_csv('best_result.csv')
                logging.info("Best result saved to best_result.csv")
            else:
                logging.warning("No result_df found in best_progress_dict.")
        else:
            logging.warning("No best_progress_dict found.")

    def plot_default_waveforms(self):
        if(self.waveforms is None):
            return
        fig, ax = plt.subplots()
        for waveform in self.waveforms:
            variable = waveform['variable']
            if 'function' in waveform:
                time_start = waveform['time_start']
                time_end = waveform['time_end']
                desired_times = np.linspace(time_start, time_end, 1000)
                desired_values = waveform['function'](desired_times)
            else:
                time_value_pairs = waveform['time_value_pairs']
                # Extract times and values from the desired waveform
                desired_times, desired_values = zip(*time_value_pairs)

            
            # Normalize values
            min_val = min(desired_values)
            max_val = max(desired_values)
            normalized_values = [(val - min_val) / (max_val - min_val) for val in desired_values]
            
            ax.plot(desired_times, normalized_values, label=f'{variable}')
        
        ax.set_title('Desired Waveforms')
        ax.set_xlabel('Time')
        ax.set_ylabel('Normalized Value')
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_progress(self, update_dict):
        worker_id = update_dict['worker_id']
        progress = self.get_percentage_complete(update_dict['progress'])
        if worker_id not in self.workers_progress:
            self.workers_progress[worker_id] = 0
            self.workers_tree.insert('', 'end', iid=worker_id, values=(worker_id, '0%'))

        self.workers_progress[worker_id] = progress
        self.workers_tree.item(worker_id, values=(worker_id, f"{progress:.1f}%"))
        # self.root.update_idletasks()
    
    def get_percentage_complete(self,time_in_simulation):
        return 100*time_in_simulation / self.original_duration if self.original_duration is not None else 0
    
    def update_text_output(self, text_output):
        self.text_output.config(state=tk.NORMAL)
        self.text_output.insert(tk.END, text_output + "\n")
        self.text_output.see(tk.END)
        self.text_output.config(state=tk.DISABLED)
        self.root.update_idletasks()