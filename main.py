import sys
import config_reader
import errors
import subprocess
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


# TODO make this support custom export names
def build_program(config: config_reader.ConfigFile) -> None:
    build_command = []

    compilation_data = config.get_section("compilation")

    #TODO: Add automatic compiler detection
    if "compiler" in compilation_data:
        build_command.append(compilation_data["compiler"])
    else:
        errors.throw_fatal_error("The compiler was not found in the config file.\nPlease specify it under `[compilation]` using `compiler = [YOUR_COMPILER]`")
    
    if "standard" in compilation_data:
        build_command.append(f"-std={compilation_data["standard"]}")
    
    if "extra_warnings" in compilation_data and bool(compilation_data["extra_warnings"]):
        build_command.append("-Wall")
        build_command.append("-Wextra")

    if "warning_error" in compilation_data and bool(compilation_data["warning_error"]):
        build_command.append("-Werror")

    if "enable_extensions" in compilation_data and bool(compilation_data["enable_extensions"]):
        build_command.append("-Wpedantic")


    build_type = config.get_section("build type")

    #TODO: Add support for standard building with multiple files listed.
    # Also consider adding support for file detection so the user doesn't have to list all of their files.
    if "type" in build_type and build_type["type"] == "unity":
        entry_point: str

        if "entry_point" in build_type:
            entry_point = build_type["entry_point"]
        else:
            errors.throw_fatal_error("The build type was set to `unity` but no entry point was given.")

        build_command.append(entry_point)

    subprocess.run(build_command, check=False, stderr=sys.stderr, text=True)

# TODO make this support custom export names
def run_program(config: config_reader.ConfigFile) -> None:
    build_program(config)
    subprocess.run("./a.out")


match sys.argv[1]:
    case "build":
        build_program(config)
    case "run":
        run_program(config)
