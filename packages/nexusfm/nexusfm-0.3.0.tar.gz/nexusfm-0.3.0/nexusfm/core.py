import os
import shutil
import datetime
import hashlib
import stat
import subprocess

class AdvancedPyFileManager:
    def __init__(self):
        self.history = []

    def list_contents(self, path='.'):
        contents = []
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            item_stat = os.stat(full_path)
            item_type = 'DIR' if os.path.isdir(full_path) else 'FILE'
            item_size = item_stat.st_size
            item_perms = stat.filemode(item_stat.st_mode)
            item_modified = datetime.datetime.fromtimestamp(item_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            contents.append(f"[{item_type}] {item.ljust(20)} {item_perms} {str(item_size).rjust(10)} bytes {item_modified}")
        self._add_to_history(f"Listed contents of {path}")
        return contents

    def create_folder(self, folder_name):
        os.makedirs(folder_name, exist_ok=True)
        self._add_to_history(f"Created folder: {folder_name}")
        return f"Folder '{folder_name}' created."

    def delete_item(self, item_name):
        if os.path.isdir(item_name):
            shutil.rmtree(item_name)
            self._add_to_history(f"Deleted folder: {item_name}")
            return f"Folder '{item_name}' and its contents deleted."
        elif os.path.isfile(item_name):
            os.remove(item_name)
            self._add_to_history(f"Deleted file: {item_name}")
            return f"File '{item_name}' deleted."
        else:
            return f"'{item_name}' not found."

    def move_item(self, source, destination):
        shutil.move(source, destination)
        self._add_to_history(f"Moved: {source} -> {destination}")
        return f"Moved '{source}' to '{destination}'."

    def copy_item(self, source, destination):
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
        self._add_to_history(f"Copied: {source} -> {destination}")
        return f"Copied '{source}' to '{destination}'."

    def calculate_hash(self, file_path, algorithm='sha256'):
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()

    def change_permissions(self, item_path, permissions):
        os.chmod(item_path, int(permissions, 8))
        self._add_to_history(f"Changed permissions of {item_path} to {permissions}")
        return f"Changed permissions of '{item_path}' to {permissions}."

    def search_content(self, path, pattern):
        result = subprocess.run(['grep', '-r', pattern, path], capture_output=True, text=True)
        self._add_to_history(f"Searched for '{pattern}' in {path}")
        return result.stdout

    def show_history(self):
        return self.history

    def _add_to_history(self, action):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"{timestamp}: {action}")