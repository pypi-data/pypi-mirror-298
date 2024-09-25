import argparse
import sys

def setup(project: str, boot: bool, install: bool, token: str):
    print(f"Setting up project: {project}")
    if boot:
        print("Booting up the project...")
    if install:
        print("Installing dependencies...")
    print(f"Using token: {token}")

def main():
    parser = argparse.ArgumentParser(description="SpeedyBot CLI")
    
    subparsers = parser.add_subparsers(dest="command")

    # Create the setup command
    setup_parser = subparsers.add_parser('setup', help='Setup a new project')
    setup_parser.add_argument('--project', required=True, help='Name of the project')
    setup_parser.add_argument('--boot', action='store_true', help='Boot up the project')
    setup_parser.add_argument('--install', action='store_true', help='Install dependencies')
    setup_parser.add_argument('--token', required=True, help='API token')

    args = parser.parse_args()

    if args.command == 'setup':
        setup(args.project, args.boot, args.install, args.token)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
