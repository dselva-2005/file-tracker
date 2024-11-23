import tkinter as tk
from watchdog.observers import Observer
from fileTracker.file_operations import is_folder_accessible, check_usb
from fileTracker.folderEventFire import FolderMonitorHandler
from functools import partial

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
    folder_to_monitor = r"C:\Users\dselv\Desktop\writing"
    folder_to_update = r"D:\home"
    user_input = entry.get()
    running = True

    # Setup the event handler and observer
    event_handler = FolderMonitorHandler(folder_to_monitor, folder_to_update)
    observer = Observer()
    observer.schedule(event_handler, folder_to_monitor, recursive=True)  # Monitor recursively
    observer.start()

    # Update the label with the user input and start monitoring
    label.config(text=f'You entered {user_input}', bg="lightgreen", fg="darkgreen")
    monitor(folder_to_monitor)  # Start folder monitoring

def stop():
    global running
    running = False
    if observer:
        observer.stop()
        observer.join()  # Wait for the observer thread to stop
    label.config(bg="#FF6666", fg="#8B0000")

# Create the Tkinter window
root = tk.Tk()
root.title('Folder Mirroring app')
root.geometry('430x300')

# Label and Entry widget for user input
label = tk.Label(root, text='hello world', font=('Arial', 16))
label.pack()

entry = tk.Entry(root, width=30)
entry.pack()

# Buttons to start and stop monitoring
button_start = tk.Button(root, text='Start', command=start)
button_start.pack()

button_stop = tk.Button(root, text='Stop', command=stop)
button_stop.pack()

# Run the Tkinter event loop
root.mainloop()
