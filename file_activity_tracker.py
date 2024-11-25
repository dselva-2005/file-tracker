import time
from watchdog.observers import Observer
from fileTracker.file_operations import is_folder_accessible,check_usb 
from fileTracker.folderEventFire import FolderMonitorHandler
from tkinter import Label

def monitor_folder(folder_path,folder_to_update):
    event_handler = FolderMonitorHandler(folder_path,folder_to_update,Label())
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)  # Recursive monitors subfolders
    observer.start()
    print(f"Monitoring folder: {folder_path}")
    try:
        while True:
            if check_usb() and is_folder_accessible(folder_path):
                event_handler.match()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    folder_to_monitor = r"C:\Users\dselv\Desktop\writing"
    folder_to_update = r"D:\home"
    monitor_folder(folder_to_monitor,folder_to_update)
