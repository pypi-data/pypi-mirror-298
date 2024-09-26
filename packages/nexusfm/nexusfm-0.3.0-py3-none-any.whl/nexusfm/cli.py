import argparse
import sys
from .core import AdvancedPyFileManager

def main():
    manager = AdvancedPyFileManager()
    parser = argparse.ArgumentParser(description="Personalized File Manager")
    parser.add_argument('action', choices=['list', 'create', 'delete', 'move', 'copy', 'hash', 'chmod', 'search', 'history'], help='Action to perform')
    parser.add_argument('args', nargs='*', help='Additional arguments for the action')

    args = parser.parse_args()

    try:
        if args.action == 'list':
            path = args.args[0] if args.args else '.'
            contents = manager.list_contents(path)
            print("\n".join(contents))
        elif args.action == 'create':
            if len(args.args) != 1:
                print("Usage: create <folder_name>")
            else:
                print(manager.create_folder(args.args[0]))
        elif args.action == 'delete':
            if len(args.args) != 1:
                print("Usage: delete <item_name>")
            else:
                print(manager.delete_item(args.args[0]))
        elif args.action == 'move':
            if len(args.args) != 2:
                print("Usage: move <source> <destination>")
            else:
                print(manager.move_item(args.args[0], args.args[1]))
        elif args.action == 'copy':
            if len(args.args) != 2:
                print("Usage: copy <source> <destination>")
            else:
                print(manager.copy_item(args.args[0], args.args[1]))
        elif args.action == 'hash':
            if len(args.args) not in [1, 2]:
                print("Usage: hash <file_path> [algorithm]")
            else:
                file_path = args.args[0]
                algorithm = args.args[1] if len(args.args) == 2 else 'sha256'
                print(manager.calculate_hash(file_path, algorithm))
        elif args.action == 'chmod':
            if len(args.args) != 2:
                print("Usage: chmod <permissions> <item_path>")
            else:
                print(manager.change_permissions(args.args[1], args.args[0]))
        elif args.action == 'search':
            if len(args.args) != 2:
                print("Usage: search <path> <pattern>")
            else:
                print(manager.search_content(args.args[0], args.args[1]))
        elif args.action == 'history':
            history = manager.show_history()
            print("\n".join(history))
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()