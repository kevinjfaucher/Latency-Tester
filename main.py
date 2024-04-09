import time
import tkinter as tk
from monitoring_gui import setup_gui
from ping_utils import ping_ip


def update_metrics(start_time, end_time, ip_address, attempt_number, ping_results, latencies, log_text, start_button,
                   time_between_pings):
    global ax1, ax2, canvas

    current_time = time.time()
    if current_time < end_time:
        success, latency = ping_ip(ip_address)
        ping_results.append(success)
        latencies.append(latency if success else None)

        # Update the attempt number
        attempt_number += 1

        # Update the log
        log_message = f"{attempt_number}. {'Success' if success else 'Fail'} - Latency: {latency if success else 'N/A'} ms\n"
        log_text.config(state='normal')
        log_text.insert(tk.END, log_message)
        log_text.yview(tk.END)
        log_text.config(state='disabled')

        # Update success/fail bar chart
        ax1.clear()
        success_count = sum(ping_results)
        fail_count = len(ping_results) - success_count
        ax1.bar(['Success', 'Fail'], [success_count, fail_count], color=['green', 'red'])
        ax1.set_title("Ping Success/Fail")
        ax1.set_xlabel("Result")
        ax1.set_ylabel("Count")
        ax1.set_ylim(0, max(success_count, fail_count) + 1)  # Adjust ylim dynamically

        # Update latency scatter plot with different colors
        ax2.clear()
        latency_points = [lat for lat in latencies if lat is not None]
        successful_attempts = range(len(latency_points))

        # Define color for each latency point
        colors = ['green' if lat <= 30 else 'orange' if lat <= 60 else 'red' for lat in latency_points]

        # Create a scatter plot
        ax2.scatter(successful_attempts, latency_points, color=colors, s=10, label='Ping Latency')
        ax2.set_title("Ping Latency")
        ax2.set_xlabel("Successful Attempts")
        ax2.set_ylabel("Latency (ms)")
        ax2.grid(True)

        canvas.draw()
        # Schedule the next update based on the user-specified time between pings
        window.after(int(time_between_pings * 1000),
                     lambda: update_metrics(start_time, end_time, ip_address, attempt_number, ping_results, latencies,
                                            log_text, start_button, time_between_pings))
    else:
        start_button['state'] = tk.NORMAL


if __name__ == "__main__":
    window, setup_frame, metrics_frame, start_button, log_text, canvas, ax1, ax2 = setup_gui(update_metrics)
    window.mainloop()
