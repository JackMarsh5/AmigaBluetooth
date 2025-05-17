import subprocess
import tkinter as tk
from tkinter import messagebox

def scan_devices():
    result = subprocess.run(['bluetoothctl', 'scan', 'on'], capture_output=True, text=True, timeout=5)
    output_text.insert(tk.END, "Scanning for devices...\n")
    output_text.insert(tk.END, result.stdout + "\n")


def pair_device():
    device_address = device_entry.get().strip()
    if not device_address:
        messagebox.showerror("Error", "Please enter a device MAC address.")
        return

    output_text.insert(tk.END, f"Attempting to pair with {device_address}...\n")
    process = subprocess.run(["bluetoothctl"], input=f"pair {device_address}\nconnect {device_address}\ntrust {device_address}\nexit\n",
                             capture_output=True, text=True)
    output_text.insert(tk.END, process.stdout + "\n")


# Set up GUI
root = tk.Tk()
root.title("Amiga Bluetooth Pairing")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=20)

scan_button = tk.Button(frame, text="Scan for Devices", command=scan_devices, width=20, height=2)
scan_button.grid(row=0, column=0, padx=10)

pair_button = tk.Button(frame, text="Pair Device", command=pair_device, width=20, height=2)
pair_button.grid(row=0, column=1, padx=10)

device_entry = tk.Entry(root, width=30, font=("Arial", 14))
device_entry.pack(pady=10)
device_entry.insert(0, "Enter MAC address")

output_text = tk.Text(root, wrap=tk.WORD, font=("Courier", 10))
output_text.pack(expand=True, fill=tk.BOTH)

root.mainloop()
