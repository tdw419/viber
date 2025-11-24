
import argparse
from . import project_service

def main():
    """
    The main entry point for the project CLI.
    """
    parser = argparse.ArgumentParser(description="A CLI for managing projects.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # New command
    new_parser = subparsers.add_parser("new", help="Create a new project.")
    new_parser.add_argument("name", help="The name of the project to create.")

    args = parser.parse_args()

    if args.command == "new":
        project_service.create_project(args.name)

if __name__ == "__main__":
    main()
