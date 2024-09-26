import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QListWidget, QPushButton, QInputDialog, QMessageBox, QFileDialog,
                             QListWidgetItem, QLabel, QLineEdit, QTextEdit, QGridLayout)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QTextCursor
from PyQt5.QtCore import Qt, QSize
from .core import AdvancedPyFileManager
from .terminal_commands import TerminalCommands

from PyQt5.QtWidgets import QTextEdit, QCompleter
from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QTextCursor
import os

class InteractiveTerminal(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setReadOnly(False)
        self.command_history = []
        self.history_index = 0
        self.current_command = ""
        
        # Set up auto-completion
        self.completer = QCompleter(self)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.activated.connect(self.insert_completion)
        
        # Initialize suggestion list
        # self.update_suggestion_list()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            self.handle_tab()
        elif event.key() == Qt.Key_Return:
            self.handle_return()
        elif event.key() == Qt.Key_Backspace:
            cursor = self.textCursor()
            if cursor.positionInBlock() > len(self.parent.current_path) + 3:
                super().keyPressEvent(event)
                self.update_completer()
        elif event.key() == Qt.Key_Up:
            self.handle_up()
        elif event.key() == Qt.Key_Down:
            self.handle_down()
        elif event.key() == Qt.Key_Left:
            cursor = self.textCursor()
            if cursor.positionInBlock() > len(self.parent.current_path) + 3:
                super().keyPressEvent(event)
        elif event.key() == Qt.Key_Home:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, len(self.parent.current_path) + 3)
            self.setTextCursor(cursor)
        else:
            super().keyPressEvent(event)
            self.update_completer()

    def handle_tab(self):
        if not self.completer.popup().isVisible():
            self.update_completer()
        else:
            self.completer.setCurrentRow(self.completer.currentRow() + 1)

    def get_current_command(self):
        return self.toPlainText().split('\n')[-1][len(self.parent.current_path) + 3:]

    # def update_suggestion_list(self):
    #     # Basic commands
    #     commands = ['cd', 'ls', 'mkdir', 'rm', 'mv', 'cp', 'pwd', 'cat', 'grep', 'chmod', 'touch', 'echo']
        
    #     # Add file and directory names from the current directory
    #     try:
    #         files_and_dirs = os.listdir(self.parent.current_path)
    #     except OSError:
    #         files_and_dirs = []
        
        # Add full command history
        full_commands = self.command_history.copy()
        
        # Combine all suggestions
        self.all_suggestions = commands + files_and_dirs + full_commands
        self.all_suggestions = list(set(self.all_suggestions))  # Remove duplicates

    def update_completer(self):
        current_text = self.get_current_command()
        suggestions = [s for s in self.all_suggestions if s.lower().startswith(current_text.lower())]
        
        model = QStringListModel(suggestions)
        self.completer.setModel(model)
        self.completer.setCompletionPrefix(current_text)
        
        if suggestions:
            rect = self.cursorRect()
            rect.setWidth(self.completer.popup().sizeHintForColumn(0) 
                          + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(rect)
        else:
            self.completer.popup().hide()

    def insert_completion(self, completion):
        cursor = self.textCursor()
        chars_to_delete = len(self.get_current_command())
        cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, chars_to_delete)
        cursor.removeSelectedText()
        cursor.insertText(completion)
        self.setTextCursor(cursor)

    def handle_return(self):
        command = self.get_current_command()
        if command not in self.command_history:
            self.command_history.append(command)
        self.history_index = len(self.command_history)
        self.append('\n')
        self.parent.execute_command(command)
        self.update_suggestion_list()

    def handle_up(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.show_command(self.command_history[self.history_index])

    def handle_down(self):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.show_command(self.command_history[self.history_index])
        elif self.history_index == len(self.command_history) - 1:
            self.history_index += 1
            self.show_command('')

    def show_command(self, command):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(f"{self.parent.current_path} $ {command}")

    def handle_return(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
        command = self.toPlainText().split('\n')[-1][len(self.parent.current_path) + 3:]
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        self.parent.execute_command(command)

    def handle_up(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.show_command(self.command_history[self.history_index])

    def handle_down(self):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.show_command(self.command_history[self.history_index])
        elif self.history_index == len(self.command_history) - 1:
            self.history_index += 1
            self.show_command('')

    def show_command(self, command):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(f"{self.parent.current_path} $ {command}")

class HackerStyle(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_manager = AdvancedPyFileManager()
        self.current_path = os.getcwd()
        self.terminal_commands = TerminalCommands(self.file_manager, self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('NexusFM - Advanced File Manager')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #0C0C0C;
                color: #00FF00;
                font-family: 'Courier';
            }
            QListWidget, QTextEdit {
                background-color: #1C1C1C;
                border: 1px solid #00FF00;
            }
            QPushButton {
                background-color: #0C0C0C;
                color: #00FF00;
                border: 1px solid #00FF00;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #00FF00;
                color: #0C0C0C;
            }
            QLabel, QLineEdit {
                color: #00FF00;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Path display and navigation
        nav_layout = QHBoxLayout()
        self.path_input = QLineEdit(self.current_path)
        self.path_input.returnPressed.connect(self.navigate_to_path)
        nav_layout.addWidget(self.path_input)
        nav_button = QPushButton("Go")
        nav_button.clicked.connect(self.navigate_to_path)
        nav_layout.addWidget(nav_button)
        layout.addLayout(nav_layout)

        # File list
        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(self.item_double_clicked)
        layout.addWidget(self.file_list)

        # Buttons
        button_layout = QGridLayout()
        buttons = [
            ('⟳', self.refresh, 'Refresh'),
            ('✚', self.create_folder, 'Create Folder'),
            ('✖', self.delete_item, 'Delete'),
            ('↷', self.move_item, 'Move'),
            ('⎘', self.copy_item, 'Copy'),
            ('#', self.calculate_hash, 'Calculate Hash'),
            ('🔒', self.change_permissions, 'Change Permissions'),
            ('🔍', self.search_content, 'Search Content'),
            ('⏲', self.show_history, 'Show History')
        ]

        for i, (icon, func, text) in enumerate(buttons):
            button = QPushButton(f"{icon} {text}")
            button.setToolTip(text)
            button.clicked.connect(func)
            button.setFixedSize(150, 60)
            button.setIconSize(QSize(24, 24))
            row, col = divmod(i, 3)
            button_layout.addWidget(button, row, col)

        layout.addLayout(button_layout)

        # Interactive Terminal
        self.console_output = InteractiveTerminal(self)
        layout.addWidget(self.console_output)

        central_widget.setLayout(layout)

        self.refresh()

        # Initialize console
        self.console_output.append("Personalized File Manager v0.2.0")
        self.console_output.append("Type 'help' for a list of commands.")
        self.show_prompt()

    def show_prompt(self):
        self.console_output.append(f"\n{self.current_path} $ ")
        cursor = self.console_output.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.console_output.setTextCursor(cursor)

    def append_to_console(self, text):
        self.console_output.moveCursor(QTextCursor.End)
        self.console_output.insertPlainText(text)
        self.console_output.moveCursor(QTextCursor.End)

    def execute_command(self, command):
        result = self.terminal_commands.execute(command)
        if result:  # Only append if there's a result
            self.append_to_console(f"\n{result}")
        self.current_path = self.terminal_commands.current_path
        self.path_input.setText(self.current_path)
        self.refresh()
        if command.strip().lower() != "clear":  # Don't show prompt if the command was 'clear'
            self.show_prompt()

    def change_directory(self, args):
        if not args:
            new_path = os.path.expanduser('~')
        else:
            new_path = os.path.abspath(os.path.join(self.current_path, args[0]))
        
        if os.path.isdir(new_path):
            self.current_path = new_path
            self.path_input.setText(self.current_path)
            self.refresh()
        else:
            self.append_to_console(f"\nDirectory not found: {new_path}")

    def list_directory(self, args):
        path = args[0] if args else self.current_path
        contents = self.file_manager.list_contents(path)
        self.append_to_console("\n" + "\n".join(contents))

    def create_folder_cmd(self, args):
        if not args:
            self.append_to_console("\nUsage: mkdir <folder_name>")
            return
        folder_name = args[0]
        try:
            result = self.file_manager.create_folder(os.path.join(self.current_path, folder_name))
            self.append_to_console(f"\n{result}")
            self.refresh()
        except Exception as e:
            self.append_to_console(f"\nError: {str(e)}")

    def delete_item_cmd(self, args):
        if not args:
            self.append_to_console("\nUsage: rm <item_name>")
            return
        item_name = args[0]
        try:
            result = self.file_manager.delete_item(os.path.join(self.current_path, item_name))
            self.append_to_console(f"\n{result}")
            self.refresh()
        except Exception as e:
            self.append_to_console(f"\nError: {str(e)}")

    def move_item_cmd(self, args):
        if len(args) != 2:
            self.append_to_console("\nUsage: mv <source> <destination>")
            return
        source, destination = args
        try:
            result = self.file_manager.move_item(
                os.path.join(self.current_path, source),
                os.path.join(self.current_path, destination)
            )
            self.append_to_console(f"\n{result}")
            self.refresh()
        except Exception as e:
            self.append_to_console(f"\nError: {str(e)}")

    def copy_item_cmd(self, args):
        if len(args) != 2:
            self.append_to_console("\nUsage: cp <source> <destination>")
            return
        source, destination = args
        try:
            result = self.file_manager.copy_item(
                os.path.join(self.current_path, source),
                os.path.join(self.current_path, destination)
            )
            self.append_to_console(f"\n{result}")
            self.refresh()
        except Exception as e:
            self.append_to_console(f"\nError: {str(e)}")

    def calculate_hash_cmd(self, args):
        if len(args) < 1 or len(args) > 2:
            self.append_to_console("\nUsage: hash <file_name> [algorithm]")
            return
        file_name = args[0]
        algorithm = args[1] if len(args) == 2 else 'sha256'
        try:
            hash_value = self.file_manager.calculate_hash(os.path.join(self.current_path, file_name), algorithm)
            self.append_to_console(f"\n{hash_value}  {file_name}")
        except Exception as e:
            self.append_to_console(f"\nError: {str(e)}")

    def change_permissions_cmd(self, args):
        if len(args) != 2:
            self.append_to_console("\nUsage: chmod <permissions> <item_name>")
            return
        permissions, item_name = args
        try:
            result = self.file_manager.change_permissions(
                os.path.join(self.current_path, item_name),
                permissions
            )
            self.append_to_console(f"\n{result}")
            self.refresh()
        except Exception as e:
            self.append_to_console(f"\nError: {str(e)}")

    def search_content_cmd(self, args):
        if len(args) < 1:
            self.append_to_console("\nUsage: grep <pattern> [path]")
            return
        pattern = args[0]
        path = args[1] if len(args) > 1 else self.current_path
        try:
            result = self.file_manager.search_content(path, pattern)
            self.append_to_console(f"\n{result}")
        except Exception as e:
            self.append_to_console(f"\nError: {str(e)}")

    def show_history_cmd(self):
        history = self.file_manager.show_history()
        self.append_to_console("\n" + "\n".join(history))

    def show_help(self):
        help_text = """
Available commands:
  cd <path>               - Change directory
  ls [path]               - List directory contents
  mkdir <folder_name>     - Create a new folder
  rm <item_name>          - Delete a file or folder
  mv <source> <dest>      - Move a file or folder
  cp <source> <dest>      - Copy a file or folder
  hash <file> [algorithm] - Calculate file hash
  chmod <perms> <item>    - Change item permissions
  grep <pattern> [path]   - Search content
  history                 - Show command history
  help                    - Show this help message
"""
        self.append_to_console(help_text)

    def navigate_to_path(self):
        new_path = self.path_input.text()
        if os.path.isdir(new_path):
            self.current_path = new_path
            self.refresh()
        else:
            QMessageBox.warning(self, "Invalid Path", f"The path '{new_path}' is not a valid directory.")

    def refresh(self):
        self.file_list.clear()
        self.file_list.addItem('..')
        contents = self.file_manager.list_contents(self.current_path)
        for item in contents:
            list_item = QListWidgetItem(item)
            if item.startswith('[DIR]'):
                list_item.setForeground(QColor('#00FFFF'))
            self.file_list.addItem(list_item)
        self.path_input.setText(self.current_path)

    def item_double_clicked(self, item):
        if item.text() == '..':
            self.current_path = os.path.dirname(self.current_path)
        else:
            new_path = os.path.join(self.current_path, item.text().split()[-1])
            if os.path.isdir(new_path):
                self.current_path = new_path
            else:
                QMessageBox.information(self, "File Selected", f"You selected file: {item.text().split()[-1]}")
        self.refresh()

    def create_folder(self):
        folder_name, ok = QInputDialog.getText(self, "Create Folder", "Enter folder name:")
        if ok and folder_name:
            try:
                result = self.file_manager.create_folder(os.path.join(self.current_path, folder_name))
                self.append_to_console(f"\n$ mkdir {folder_name}")
                self.append_to_console(f"\n{result}")
                self.refresh()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def delete_item(self):
        current_item = self.file_list.currentItem()
        if current_item and current_item.text() != '..':
            item_name = current_item.text().split()[-1]
            reply = QMessageBox.question(self, "Confirm Deletion", 
                                         f"Are you sure you want to delete {item_name}?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    result = self.file_manager.delete_item(os.path.join(self.current_path, item_name))
                    self.append_to_console(f"\n$ rm -rf {item_name}")
                    self.append_to_console(f"\n{result}")
                    self.refresh()
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))

    def move_item(self):
        current_item = self.file_list.currentItem()
        if current_item and current_item.text() != '..':
            item_name = current_item.text().split()[-1]
            destination = QFileDialog.getExistingDirectory(self, "Select Destination")
            if destination:
                try:
                    result = self.file_manager.move_item(
                        os.path.join(self.current_path, item_name),
                        os.path.join(destination, item_name)
                    )
                    self.append_to_console(f"\n$ mv {item_name} {destination}")
                    self.append_to_console(f"\n{result}")
                    self.refresh()
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))

    def copy_item(self):
        current_item = self.file_list.currentItem()
        if current_item and current_item.text() != '..':
            item_name = current_item.text().split()[-1]
            destination = QFileDialog.getExistingDirectory(self, "Select Destination")
            if destination:
                try:
                    result = self.file_manager.copy_item(
                        os.path.join(self.current_path, item_name),
                        os.path.join(destination, item_name)
                    )
                    self.append_to_console(f"\n$ cp -r {item_name} {destination}")
                    self.append_to_console(f"\n{result}")
                    self.refresh()
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))

    def calculate_hash(self):
        current_item = self.file_list.currentItem()
        if current_item and current_item.text() != '..' and not current_item.text().startswith('[DIR]'):
            file_name = current_item.text().split()[-1]
            file_path = os.path.join(self.current_path, file_name)
            algorithm, ok = QInputDialog.getItem(self, "Select Hash Algorithm", 
                                                 "Choose algorithm:", 
                                                 ["md5", "sha1", "sha256", "sha512"], 
                                                 current=2, 
                                                 editable=False)
            if ok:
                try:
                    hash_value = self.file_manager.calculate_hash(file_path, algorithm)
                    self.append_to_console(f"\n$ {algorithm}sum {file_name}")
                    self.append_to_console(f"\n{hash_value}  {file_name}")
                    self.show_prompt()
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))

    def change_permissions(self):
        current_item = self.file_list.currentItem()
        if current_item and current_item.text() != '..':
            item_name = current_item.text().split()[-1]
            permissions, ok = QInputDialog.getText(self, "Change Permissions", 
                                                   "Enter new permissions (octal):")
            if ok:
                try:
                    result = self.file_manager.change_permissions(
                        os.path.join(self.current_path, item_name),
                        permissions
                    )
                    self.append_to_console(f"\n$ chmod {permissions} {item_name}")
                    self.append_to_console(f"\n{result}")
                    self.refresh()
                except Exception as e:
                    QMessageBox.warning(self, "Error", str(e))

    def search_content(self):
        pattern, ok = QInputDialog.getText(self, "Search Content", "Enter search pattern:")
        if ok:
            try:
                result = self.file_manager.search_content(self.current_path, pattern)
                self.append_to_console(f"\n$ grep -r '{pattern}' .")
                self.append_to_console(f"\n{result}")
                self.show_prompt()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def show_history(self):
        history = self.file_manager.show_history()
        self.append_to_console("\n$ history")
        self.append_to_console("\n" + "\n".join(history))
        self.show_prompt()

    def clear_console(self):
        self.console_output.clear()
        self.show_prompt()

def main():
    app = QApplication(sys.argv)
    ex = HackerStyle()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()