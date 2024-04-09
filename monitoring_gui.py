import tkinter as tk
from tkinter import messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
import time

def start_monitoring(ip_entry, duration_entry, time_between_pings_entry, start_button, log_text, setup_frame, metrics_frame, update_metrics):
    # Retrieve values from GUI
    ip_address = ip_entry.get()
    duration_in_minutes = float(duration_entry.get())
    time_between_pings = float(time_between_pings_entry.get())

    # Check for valid IP address, duration, and time between pings
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip_address) or duration_in_minutes <= 0 or time_between_pings <= 0:
        messagebox.showerror("Error", "Please enter a valid IP address, duration, and time between pings.")
        return

    # Prepare for a new monitoring session
    ping_results = []
    latencies = []
    attempt_number = 0
    start_time = time.time()
    end_time = start_time + duration_in_minutes * 60
    start_button['state'] = tk.DISABLED  # Disable the start button during monitoring

    # Clear the previous log
    log_text.delete('1.0', tk.END)

    # Switch to the metrics screen
    setup_frame.pack_forget()
    metrics_frame.pack(fill='both', expand=True)

    # Start updating metrics with the additional time_between_pings argument
    update_metrics(start_time, end_time, ip_address, attempt_number, ping_results, latencies, log_text, start_button, time_between_pings)

def setup_gui(update_metrics_callback):
    window = tk.Tk()
    window.title("Ping Monitor")

    # Setup Frame
    setup_frame = tk.Frame(window)
    setup_frame.pack(fill='both', expand=True)

    # IP Address Entry
    tk.Label(setup_frame, text="IP Address:").pack(side='top', fill='x', padx=50, pady=5)
    ip_entry = tk.Entry(setup_frame)
    ip_entry.pack(side='top', fill='x', padx=50, pady=5)

    # Time Between Pings Entry
    tk.Label(setup_frame, text="Time Between Pings (seconds):").pack(side='top', fill='x', padx=50, pady=5)
    time_between_pings_entry = tk.Entry(setup_frame)
    time_between_pings_entry.pack(side='top', fill='x', padx=50, pady=5)

    # Duration Entry
    tk.Label(setup_frame, text="Duration (minutes):").pack(side='top', fill='x', padx=50, pady=5)
    duration_entry = tk.Entry(setup_frame)
    duration_entry.pack(side='top', fill='x', padx=50, pady=5)

    # Start Button
    start_button = tk.Button(setup_frame, text="Start Monitoring", command=lambda: start_monitoring(
        ip_entry, duration_entry, time_between_pings_entry, start_button, log_text, setup_frame, metrics_frame, update_metrics_callback))
    start_button.pack(side='top', pady=20)

    # Metrics Frame
    metrics_frame = tk.Frame(window)

    # Graph Area
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    canvas = FigureCanvasTkAgg(fig, master=metrics_frame)
    canvas.get_tk_widget().pack(side='top', fill='both', expand=True)

    # Log Text Area
    log_text = scrolledtext.ScrolledText(metrics_frame, height=15)
    log_text.pack(side='bottom', fill='x', expand=True)
    log_text.config(state='disabled')

    return window, setup_frame, metrics_frame, start_button, log_text, canvas, ax1, ax2