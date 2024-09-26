import os
import shutil
import glob
import subprocess

class TerminalCommands:
    def __init__(self, file_manager, gui):
        self.file_manager = file_manager
        self.gui = gui
        self.current_path = os.getcwd()

    def help(self, args):
        commands = {
            'cd': 'Change the current directory',
            'pwd': 'Print the current working directory',
            'ls': 'List directory contents',
            'mkdir': 'Create a new directory',
            'rm': 'Remove files or directories',
            'mv': 'Move or rename files or directories',
            'cp': 'Copy files or directories',
            'cat': 'Display the contents of a file',
            'grep': 'Search for a pattern in a file',
            'chmod': 'Change file permissions',
            'history': 'Show command history',
            'clear': 'Clear the console screen',
            'echo': 'Display a line of text',
            'touch': 'Create an empty file',
            'help': 'Display information about available commands'
        }

        max_cmd_length = max(len(cmd) for cmd in commands)
        
        help_text = "Available commands:\n\n"
        for cmd, description in commands.items():
            help_text += f"{cmd.ljust(max_cmd_length + 2)} {description}\n"
        
        help_text += "\nFor more information on a specific command, type 'help <command>'."
        return help_text

    def help_command(self, command):
        command_help = {
            'cd': 'cd [DIRECTORY]\n\nChange the current directory to DIRECTORY. If no DIRECTORY is specified, changes to the home directory.',
            'pwd': 'pwd\n\nPrint the current working directory.',
            'ls': 'ls [DIRECTORY]\n\nList directory contents. If no DIRECTORY is specified, lists the current directory.',
            'mkdir': 'mkdir DIRECTORY\n\nCreate a new directory named DIRECTORY.',
            'rm': 'rm [-r] [-f] FILE...\n\nRemove files or directories.\n  -r  remove directories and their contents recursively\n  -f  ignore nonexistent files and arguments, never prompt',
            'mv': 'mv SOURCE DESTINATION\n\nMove or rename SOURCE to DESTINATION.',
            'cp': 'cp [-r] SOURCE DESTINATION\n\nCopy SOURCE to DESTINATION.\n  -r  copy directories recursively',
            'cat': 'cat FILE\n\nDisplay the contents of FILE.',
            'grep': 'grep PATTERN FILE\n\nSearch for PATTERN in FILE.',
            'chmod': 'chmod PERMISSIONS FILE\n\nChange the file mode (permissions) of FILE to PERMISSIONS.',
            'history': 'history\n\nDisplay the command history.',
            'clear': 'clear\n\nClear the console screen.',
            'echo': 'echo [STRING...]\n\nDisplay a line of text.',
            'touch': 'touch FILE\n\nCreate an empty file or update the access and modification times of an existing file.',
            'help': 'help [COMMAND]\n\nDisplay information about available commands. If COMMAND is specified, show detailed help for that command.'
        }
        
        return command_help.get(command, f"No detailed help available for '{command}'.")

    def execute(self, command):
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == 'help' and len(args) == 1:
            return self.help_command(args[0])
        elif hasattr(self, cmd):
            return getattr(self, cmd)(args)
        else:
            return f"Unknown command: {cmd}. Type 'help' for a list of available commands."

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
            return "Usage: rm [-rf] <item_name>"
        
        recursive = False
        force = False
        items_to_remove = []

        # Parse arguments
        for arg in args:
            if arg.startswith('-'):
                if 'r' in arg:
                    recursive = True
                if 'f' in arg:
                    force = True
            else:
                items_to_remove.append(arg)

        if not items_to_remove:
            return "Usage: rm [-rf] <item_name>"

        results = []
        for item in items_to_remove:
            item_path = os.path.join(self.current_path, item)
            try:
                if os.path.isdir(item_path):
                    if recursive:
                        shutil.rmtree(item_path)
                        results.append(f"Removed directory: {item}")
                    else:
                        return f"Cannot remove '{item}': Is a directory. Use -r to remove directories."
                elif os.path.isfile(item_path):
                    os.remove(item_path)
                    results.append(f"Removed file: {item}")
                else:
                    if not force:
                        return f"Cannot remove '{item}': No such file or directory"
            except Exception as e:
                if not force:
                    return f"Error removing '{item}': {str(e)}"

        return "\n".join(results) if results else "No items were removed."

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