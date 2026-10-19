import os
import sys
from pathlib import Path

import compilation_runner
import config_reader
from compiler import Compiler

if len(sys.argv) <= 1:
    # TODO: Define a better help system.
    print("No arguments were provided.")
    sys.exit(-1)

config_file_path = Path("./lithium.ini")
if not config_file_path.exists():
    print(
        "No config file could be found.\nMake sure you have a config file named `lithium.ini`!"
    )
    sys.exit(-1)
config = config_reader.ConfigFile(config_file_path)

compiler = Compiler(config)

output_dir = Path(compiler.get_output_file_name()).parent
os.makedirs(output_dir, exist_ok=True)

match sys.argv[1]:
    case "build":
        compilation_runner.build(compiler)
    case "run":
        compilation_runner.run(compiler)
    case "getargs":
        print(compilation_runner.get_build_arguments(compiler))
