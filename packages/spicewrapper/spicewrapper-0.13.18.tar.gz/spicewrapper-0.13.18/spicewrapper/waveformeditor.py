import matplotlib
matplotlib.use('TkAgg')  # Set the backend to TkAgg

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import simpledialog, messagebox
import pyperclip

class WaveformEditor:
    def __init__(self):
        self.points = []
        self.root = tk.Tk()
        self.root.title("Waveform Editor")
        self.create_gui()
        self.create_plot()

    def create_gui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(control_frame, text="Variable:").grid(row=0, column=0)
        self.variable_entry = tk.Entry(control_frame)
        self.variable_entry.grid(row=0, column=1)

        tk.Label(control_frame, text="Start Time:").grid(row=1, column=0)
        self.start_time_entry = tk.Entry(control_frame)
        self.start_time_entry.grid(row=1, column=1)

        tk.Label(control_frame, text="End Time:").grid(row=2, column=0)
        self.end_time_entry = tk.Entry(control_frame)
        self.end_time_entry.grid(row=2, column=1)

        tk.Label(control_frame, text="Lower Y:").grid(row=3, column=0)
        self.lower_y_entry = tk.Entry(control_frame)
        self.lower_y_entry.grid(row=3, column=1)

        tk.Label(control_frame, text="Upper Y:").grid(row=4, column=0)
        self.upper_y_entry = tk.Entry(control_frame)
        self.upper_y_entry.grid(row=4, column=1)

        tk.Label(control_frame, text="Deviation Size:").grid(row=5, column=0)
        self.deviation_size_entry = tk.Entry(control_frame)
        self.deviation_size_entry.grid(row=5, column=1)

        tk.Label(control_frame, text="Power:").grid(row=6, column=0)
        self.power_entry = tk.Entry(control_frame)
        self.power_entry.grid(row=6, column=1)

        tk.Button(control_frame, text="Set Axes", command=self.set_axes).grid(row=7, column=0, columnspan=2)
        tk.Button(control_frame, text="Enter", command=self.enter).grid(row=8, column=0, columnspan=2)

    def create_plot(self):
        plot_frame = tk.Frame(self.root)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots()
        self.ax.grid(True)  # Add grid to the plot
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def set_axes(self):
        try:
            start_time = float(self.start_time_entry.get())
            end_time = float(self.end_time_entry.get())
            lower_y = float(self.lower_y_entry.get())
            upper_y = float(self.upper_y_entry.get())
            self.ax.set_xlim(start_time, end_time)
            self.ax.set_ylim(lower_y, upper_y)
            self.ax.figure.canvas.draw()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid numerical values for the axes limits.")

    def onclick(self, event):
        if event.inaxes is not None:
            point = (event.xdata, event.ydata)
            if point in self.points:
                self.points.remove(point)
                self.ax.plot(event.xdata, event.ydata, 'ro')
            else:
                self.points.append(point)
                self.ax.plot(event.xdata, event.ydata, 'bo')
            self.ax.figure.canvas.draw()
objective_waveform = {
    'variable': 'fdsafdsa',
    'time_value_pairs': [(0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)],
    'deviation_size': 2e-06,
    'power': 2
}

def enter(self):
    self.points.sort()
    time_value_pairs = [(round(float(x), 18), round(float(y), 18)) for x, y in self.points]
    variable = self.variable_entry.get()
    deviation_size = self.deviation_size_entry.get()
    power = self.power_entry.get()
    waveform = {
        'variable': variable if variable else 'var_name',
        'time_value_pairs': time_value_pairs,
        'deviation_size': float(deviation_size) if deviation_size else 1e-6,
        'power': int(power) if power else 1
    }
    formatted_waveform = (
        "objective_waveform = {\n"
        f"    'variable': '{waveform['variable']}',\n"
        f"    'time_value_pairs': {[(round(x, 3), round(y, 3)) for x, y in waveform['time_value_pairs']]},\n"
        f"    'deviation_size': {waveform['deviation_size']},\n"
        f"    'power': {waveform['power']}\n"
        "}"
    )
    pyperclip.copy(formatted_waveform)
    messagebox.showinfo("Waveform Copied", "The waveform has been copied to the clipboard.")
    self.root.destroy()

if __name__ == "__main__":
    WaveformEditor()
    tk.mainloop()