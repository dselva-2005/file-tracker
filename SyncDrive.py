import tkinter as tk
from tkinter import ttk
from watchdog.observers import Observer
from fileTracker.file_operations import is_folder_accessible, check_usb
from fileTracker.folderEventFire import FolderMonitorHandler
from functools import partial
from pathlib import Path

# Initialize global variables
observer = None
event_handler = None
running = False

def monitor(folder_path):
    # Monitor function to be run every second
    if running:
        if check_usb() and is_folder_accessible(folder_path):
            event_handler.match()  # Trigger matching action if conditions are met
        root.after(1000, partial(monitor, folder_path))  # Keep monitoring every 1000 ms

def start():
    global observer, event_handler, running
    folder_to_monitor = source.get()
    folder_to_update = destination.get()
    if Path(folder_to_monitor).exists():
        running = True
        source.config(state="disabled")  # Disable editing
        destination.config(state="disabled")  # Disable editing
        # Setup the event handler and observer
        event_handler = FolderMonitorHandler(folder_to_monitor, folder_to_update,stats)
        observer = Observer()
        observer.schedule(event_handler, folder_to_monitor, recursive=True)  # Monitor recursively
        observer.start()

        # Update the label with the user input and start monitoring
        title_label.config(text=f'Monitoring', bg="lightgreen", fg="darkgreen")
        monitor(folder_to_monitor)  # Start folder monitoring
    else:
        title_label.config(text=f'Invalid Source',bg="#FF6666", fg="#8B0000")

def stop():
    global running
    running = False
    if observer:
        observer.stop()
        observer.join()  # Wait for the observer thread to stop
    title_label.config(text=f' Stopped Monitoring',bg="#FF6666", fg="#8B0000")
    source.config(state="normal")  # Disable editing
    destination.config(state="normal")  # Disable editing


# Create the Tkinter window
root = tk.Tk()
root.title("Folder Mirroring App")
root.geometry("430x380")
root.configure(bg="#f9f9f9")  # Light background for minimalism

# Title Label
title_label = tk.Label(
    root, text="Folder Mirroring App", font=("Arial", 18, "bold"), fg="#333333", bg="#f9f9f9"
)
title_label.pack(pady=(10, 20))

# Source Folder Label and Entry
from_label = tk.Label(root, text="Source Folder", font=("Arial", 12), fg="#383737", bg="#f9f9f9")
from_label.pack()

source = ttk.Entry(root, width=40, font=("Arial", 11))
source.insert(0, r"C:\Users\dselv\Desktop\writing")
source.pack(padx=20, pady=(0, 15))

# Destination Folder Label and Entry
to_label = tk.Label(root, text="Destination Folder", font=("Arial", 12), fg="#383737", bg="#f9f9f9")
to_label.pack()

destination = ttk.Entry(root, width=40, font=("Arial", 11))
destination.insert(0, r"D:\home")
destination.pack(padx=20, pady=(0, 15))

# Style the Entry fields to blend completely with the background
style = ttk.Style()
style.configure(
    "Custom.TEntry",
    fieldbackground="#f9f9f9",  # Matches the background color completely
    borderwidth=0,  # No border
    highlightthickness=0,  # No focus border
    padding=5,
    foreground="#333333",  # Dark text for readability
)

# Apply the custom style to both entries
source.configure(style="Custom.TEntry")
destination.configure(style="Custom.TEntry")

# Buttons
button_frame = tk.Frame(root, bg="#f9f9f9")
button_frame.pack(pady=10)

button_start = tk.Button(
    button_frame,
    text="Start",
    font=("Arial", 12),
    bg="#4CAF50",
    fg="white",
    activebackground="#45a049",
    activeforeground="white",
    relief="flat",
    width=10,
    command=start,
)
button_start.grid(row=0, column=0, padx=10)

button_stop = tk.Button(
    button_frame,
    text="Stop",
    font=("Arial", 12),
    bg="#f44336",
    fg="white",
    activebackground="#e53935",
    activeforeground="white",
    relief="flat",
    width=10,
    command=stop,
)
button_stop.grid(row=0, column=1, padx=10)

# Status Label
stats = tk.Label(root, text="", font=("Arial", 10), fg="#666666", bg="#f9f9f9")
stats.pack(pady=(10, 0))

# Run the Tkinter event loop
root.mainloop()