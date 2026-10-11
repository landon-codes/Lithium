import sys
import config_reader
import errors
from pathlib import Path

if len(sys.argv) <= 1:
    # TODO: Define a better help system.
    errors.throw_fatal_error("No arguments were provided.")

config_file_path = Path("lithium.ini")
if not config_file_path.exists():
    errors.throw_fatal_error(
        "No config file could be found.\nMake sure you have a config file named `lithium.ini`!"
    )
config = config_reader.ConfigFile(config_file_path)


# TODO
def build_program(config: config_reader.ConfigFile) -> None:
    print("Program built!")


# TODO
def run_program(config: config_reader.ConfigFile) -> None:
    print("Program run!")


match sys.argv[1]:
    case "build":
        build_program(config)
    case "run":
        run_program(config)
