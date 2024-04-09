# ping_utils.py
import os
import re

# Function to ping an IP address and return the success status and latency
def ping_ip(ip_address):
    response = os.popen(f"ping -n 1 {ip_address}").read()
    success = "Received = 1" in response
    latency = -1
    if success:
        match = re.search(r"Average = (\d+)ms", response)
        if match:
            latency = int(match.group(1))
    return success, latency
