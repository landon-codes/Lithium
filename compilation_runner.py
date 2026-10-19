import pathlib
import subprocess
import sys

from compiler import Compiler


def get_build_arguments(compiler: Compiler) -> list[str]:
    build_arguments = []

    compiler_name = compiler.get_compiler()
    if compiler_name == None:
        print("No supported compiler could be found.")
        sys.exit(-1)
    build_arguments.append(compiler_name)

    output_file = compiler.get_output_file()
    build_arguments.extend(output_file)

    standard = compiler.get_standard()
    if standard != None:
        build_arguments.append(standard)

    extra_warnings = compiler.get_extra_warnings()
    if extra_warnings != None:
        build_arguments.extend(extra_warnings)

    warning_error = compiler.get_warning_error()
    if warning_error != None:
        build_arguments.append(warning_error)

    extensions_enabled = compiler.get_enable_extensions()
    if extensions_enabled != None:
        build_arguments.append(extensions_enabled)

    return build_arguments


def _build_unity(compiler: Compiler) -> None:
    arguments = get_build_arguments(compiler)

    entry_point = compiler.get_entry_point()
    if entry_point != None:
        arguments.append(entry_point)
    else:
        print("No entry point could be found when running the program.")
        sys.exit(-1)

    _run_compilation(compiler, arguments)


def _build_standard(compiler: Compiler) -> None:
    new_files = compiler.get_new_files()
    output_directory = pathlib.Path(compiler.get_output_file_name).parent
    compilation_arguments = get_build_arguments(compiler)

    compilation_command = [
        "cd",
        output_directory,
        "&&"
    ]
    compilation_command.extend(compilation_arguments)

    # TODO: Get the argument to add to the compilation command to output
    # object files instead of an executable.

    #TODO: Add `../` to the beginning of each file
    # and append that file to the end of the 
    # compilation command so that it can be compiled.
    for file in new_files:
        pass

def _build_full(compiler: Compiler) -> None:
    build_arguments = get_build_arguments(compiler)

    files = compiler.get_all_files()
    build_arguments.extend(files)

    _run_compilation(compiler, build_arguments)

def _run_compilation(compiler: Compiler, arguments: list[str]):
    subprocess.run(arguments, check=False, stderr=sys.stderr, text=True)

def _run_output(application_name: str):
    subprocess.run([application_name], check=False, text=True, stderr=sys.stderr)
    
def build(compiler: Compiler) -> None:
    build_type = compiler.get_build_type()
    
    match build_type:
        case "unity":
            _build_unity(compiler)
        case "standard":
            _build_standard(compiler)
        case "full build":
            _build_full(compiler)
        case _:
            print(f'The build type, "{build_type}" does not appear to be supported.')
            print(
                "The currently supported build types are:1. Standard\n2. Unity\n3. Full build"
            )
            sys.exit(-1)

def run(compiler: Compiler) -> None:
    try:
        build(compiler)
    except: return

    application_name = compiler.get_output_file_name()

    _run_output(application_name)
