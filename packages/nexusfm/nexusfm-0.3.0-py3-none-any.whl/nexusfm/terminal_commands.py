import os
import shutil
import glob
import subprocess

class TerminalCommands:
    def __init__(self, file_manager, gui):
        self.file_manager = file_manager
        self.gui = gui
        self.current_path = os.getcwd()

    def execute(self, command):
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if hasattr(self, cmd):
            return getattr(self, cmd)(args)
        else:
            return f"Unknown command: {cmd}"

    def cd(self, args):
        if not args:
            new_path = os.path.expanduser('~')
        else:
            new_path = os.path.abspath(os.path.join(self.current_path, args[0]))
        
        if os.path.isdir(new_path):
            self.current_path = new_path
            return f"Changed directory to {self.current_path}"
        else:
            return f"Directory not found: {new_path}"

    def pwd(self, args):
        return self.current_path

    def ls(self, args):
        path = args[0] if args else self.current_path
        return "\n".join(self.file_manager.list_contents(path))

    def mkdir(self, args):
        if not args:
            return "Usage: mkdir <folder_name>"
        folder_name = args[0]
        return self.file_manager.create_folder(os.path.join(self.current_path, folder_name))

    def rm(self, args):
        if not args:
            return "Usage: rm [-r] <item_name>"
        if args[0] == "-r":
            if len(args) < 2:
                return "Usage: rm -r <item_name>"
            item_name = args[1]
        else:
            item_name = args[0]
        return self.file_manager.delete_item(os.path.join(self.current_path, item_name))

    def mv(self, args):
        if len(args) != 2:
            return "Usage: mv <source> <destination>"
        source, destination = args
        return self.file_manager.move_item(
            os.path.join(self.current_path, source),
            os.path.join(self.current_path, destination)
        )

    def cp(self, args):
        if len(args) != 2:
            return "Usage: cp [-r] <source> <destination>"
        if args[0] == "-r":
            if len(args) != 3:
                return "Usage: cp -r <source> <destination>"
            source, destination = args[1], args[2]
        else:
            source, destination = args
        return self.file_manager.copy_item(
            os.path.join(self.current_path, source),
            os.path.join(self.current_path, destination)
        )

    def cat(self, args):
        if not args:
            return "Usage: cat <file_name>"
        file_path = os.path.join(self.current_path, args[0])
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def grep(self, args):
        if len(args) < 2:
            return "Usage: grep <pattern> <file_name>"
        pattern, file_name = args[0], args[1]
        return self.file_manager.search_content(os.path.join(self.current_path, file_name), pattern)

    def chmod(self, args):
        if len(args) != 2:
            return "Usage: chmod <permissions> <item_name>"
        permissions, item_name = args
        return self.file_manager.change_permissions(
            os.path.join(self.current_path, item_name),
            permissions
        )

    def history(self, args):
        return "\n".join(self.file_manager.show_history())

    def clear(self, args):
        self.gui.clear_console()
        return ""

    def echo(self, args):
        return " ".join(args)

    def touch(self, args):
        if not args:
            return "Usage: touch <file_name>"
        file_path = os.path.join(self.current_path, args[0])
        open(file_path, 'a').close()
        return f"Created file: {args[0]}"

    def help(self, args):
        commands = [method for method in dir(self) if not method.startswith('_') and callable(getattr(self, method))]
        return "Available commands:\n" + "\n".join(commands)