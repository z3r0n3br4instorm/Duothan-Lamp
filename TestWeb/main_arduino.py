from flask import Flask, render_template
import pyfirmata2
import time
import threading
import os
import socket
import psutil
from datetime import datetime, timedelta
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.align import Align

# Global variables for TUI
console = Console()
start_time = datetime.now()
active_lamps = 0
trigger_status = "IDLE"
system_stats = {"cpu": 0, "memory": 0, "battery": "N/A"}

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "127.0.0.1"

def get_system_stats():
    """Get system statistics"""
    global system_stats
    try:
        system_stats["cpu"] = psutil.cpu_percent(interval=1)
        system_stats["memory"] = psutil.virtual_memory().percent
        # Try to get battery info (may not be available on all systems)
        try:
            battery = psutil.sensors_battery()
            if battery:
                system_stats["battery"] = f"{battery.percent}%"
            else:
                system_stats["battery"] = "AC Power"
        except:
            system_stats["battery"] = "N/A"
    except:
        pass

def get_uptime():
    """Get system uptime"""
    uptime_duration = datetime.now() - start_time
    hours, remainder = divmod(uptime_duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{uptime_duration.days}d {hours:02d}h {minutes:02d}m {seconds:02d}s"

def create_tui_display():
    """Create the TUI display using logo.txt template"""
    # Read the logo template
    with open('logo.txt', 'r') as f:
        logo_template = f.read()
    
    # Get current values
    ip_addr = get_local_ip()
    uptime = get_uptime()
    
    # Replace placeholders in the template
    display_text = logo_template.replace("{IP_ADDR}", ip_addr)
    display_text = display_text.replace("{0}", str(active_lamps))  # For Active Lamps
    display_text = display_text.replace("{TRIGGER_STATUS}", trigger_status)
    display_text = display_text.replace("{TIME}", uptime)
    display_text = display_text.replace("{POWER}", system_stats["battery"])
    display_text = display_text.replace("{LOAD}", f"{system_stats['cpu']:.1f}%")
    
    # Replace the second {LOAD} with memory usage
    display_text = display_text.replace("{LOAD}", f"{system_stats['memory']:.1f}%", 1)
    
    # Create colored text
    text = Text()
    for line in display_text.split('\n'):
        if "DUOTHAN 5.0" in line:
            text.append(line + "\n", style="bold cyan")
        elif "ERROR:" in line or "ERROR" in trigger_status and "Trigger Status:" in line:
            text.append(line + "\n", style="bold red")
        elif ":::" in line or "██" in line:
            text.append(line + "\n", style="bold magenta")  # Pink for logo
        else:
            text.append(line + "\n", style="cyan")  # Cyan for rest of text
    
    return Panel(text, title="[bold cyan]DUOTHAN LAMP CONTROL SYSTEM[/bold cyan]", border_style="cyan")

def update_display():
    """Update the TUI display"""
    with Live(create_tui_display(), refresh_per_second=1, console=console) as live:
        while True:
            get_system_stats()
            live.update(create_tui_display())
            time.sleep(1)

# Create a Flask instance
app = Flask(__name__, static_url_path='/templates/static')

# Start TUI in a separate thread
def start_tui():
    console.clear()
    update_display()

tui_thread = threading.Thread(target=start_tui, daemon=True)
tui_thread.start()

# Initialize Arduino
try:
    board = pyfirmata2.Arduino('/dev/ttyACM0')
    
    # Resetting the state of the all switches
    for i in range(2,13):
        board.digital[i].write(1)
        time.sleep(0.1)  # Small delay for stability
    
    trigger_status = "READY"
except Exception as e:
    trigger_status = f"ERROR: {str(e)}"
# Define a route and a view function

@app.route('/')
def main():
    return render_template('lamptest.html')

@app.route('/turnOffbutt/<int:value>/<int:status>', methods=['POST'])
def turnOffbutt(value, status):
    global active_lamps, trigger_status
    try:
        trigger_status = f"PROCESSING PIN {value}"
        board.digital[value].write(0)
        active_lamps += 1
        time.sleep(2)
        board.digital[value].write(1)
        active_lamps = max(0, active_lamps - 1)
        trigger_status = "READY"
        return '', 204
    except Exception as e:
        trigger_status = f"ERROR: {str(e)}"
        return '', 400


# Run the Flask app on the local network
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
