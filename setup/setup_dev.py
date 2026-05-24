import argparse
import config
import utils
import sys
import os

vi_command_keys = list(config.VERIFY_INSTALLATION_COMMANDS.keys())
parser = argparse.ArgumentParser(description="DEVELOPMENT ENVIRONMENT CLI COMMANDS")
parser.add_argument("-d","--dir", type=str, default=".")
parser.add_argument("--env", type=str, required=True, choices=vi_command_keys, help="Environment to setup")
parser.add_argument("-v", "--verbose", action="store_true", help="Output log processes to terminal")
args = parser.parse_args()


OPERATING_SYSTEM = utils.get_os().lower()
if OPERATING_SYSTEM not in config.SUPPORTED_OS:
    print(F"OS:({OPERATING_SYSTEM}) IS NOT SUPPORTED YET")
    sys.exit(1)

cmd_key = args.env.strip()
commands = config.VERIFY_INSTALLATION_COMMANDS.get(cmd_key)
    
if not commands:
    print(f"INVALID ARGUMENT PASSED TO --env => {cmd_key}.\nUse --env (-h --help) for help")
    sys.exit(1)

try:
    use_path = os.path.abspath(args.dir)
    os.makedirs(use_path, exist_ok=True)
except FileNotFoundError:
    print("Provide a valid path")
    sys.exit(1)
    
is_installed =  utils.verify_installation(commands, use_path)
if not is_installed:
    print(f"{cmd_key} is not installed. Installation procedure is not yet implemented...")
    sys.exit(1)

print(f"{cmd_key} is installed. Setup process is not yet implemented")






