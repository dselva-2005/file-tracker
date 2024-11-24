from watchdog.events import FileSystemEventHandler
from .file_operations import create_file_set,delete_file_set,copy_set_file,rename_set_file
from datetime import datetime


class FolderMonitorHandler(FileSystemEventHandler):
    def __init__(self,folder_path,folder_to_update,label):
        self.folder_path = folder_path
        self.folder_to_update = folder_to_update
        self.operations = list()
        self.created = int()
        self.deleted = int()
        self.moved = int()
        self.modified = int()
        self.label = label

    def on_created(self, event):
        if '.TMP' not in event.src_path:
            if '.tmp' not in event.src_path:
                if '~$' not in event.src_path:
                    self.operations.append({'create':event.src_path})
                    self.created += 1
            

    def on_deleted(self, event):
        if '.TMP' not in event.src_path:
            if '.tmp' not in event.src_path:
                if '~$' not in event.src_path :
                    self.operations.append({'deleted':event.src_path})
                    self.deleted += 1
                

    def on_modified(self, event):
        if '.TMP' not in event.src_path:
            if '.tmp' not in event.src_path:
                if '~$' not in event.src_path:
                    if not event.is_directory:
                        action = dict({'modified':event.src_path})
                        if action not in self.operations:
                            self.operations.append(action)
                            self.modified +=1

    def on_moved(self, event):
        if '.TMP' not in event.src_path and '.TMP' not in event.dest_path:
            if '.tmp' not in event.src_path and '.tmp' not in event.dest_path:
                if '~$' not in event.src_path and '~$' not in event.dest_path:
                    self.operations.append({"moved":(event.src_path,event.dest_path)})
                    self.moved += 1
                

    def match(self):

        if self.operations:
            for task in self.operations:
                for kind,operation in task.items():
                    match kind:
                        case 'create':
                            # Code to execute if subject matches pattern1
                            create_file_set(operation,self.folder_path,self.folder_to_update)
                        case 'deleted':
                            # Code to execute if subject matches pattern2
                            delete_file_set(operation,self.folder_path,self.folder_to_update)
                        case 'modified':
                            # Code to execute if subject matches pattern2
                            copy_set_file(operation,self.folder_path,self.folder_to_update)
                        case 'moved':
                            # Code to execute if subject matches pattern2
                            rename_set_file(operation,self.folder_path,self.folder_to_update)
                        case _:
                            # Default case (matches anything)
                            pass
            now = datetime.now()
            formatted_datetime = now.strftime("%d/%m/%Y %H:%M:%S")
            self.label.config(text=f'last updated at \n{formatted_datetime} \ncreated:{self.created},deleted:{self.deleted},moved:{self.moved},modified:{self.modified}',font=("Arial", 11))
            self.operations.clear()
            self.created = 0
            self.deleted = 0
            self.moved = 0
            self.modified = 0