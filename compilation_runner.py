import pathlib
import subprocess
import sys

from compiler import Compiler


def get_build_arguments(compiler: Compiler, include_output_dir: bool = True) -> list[str]:
    build_arguments = []

    compiler_name = compiler.get_compiler()
    if compiler_name == None:
        print("No supported compiler could be found.")
        sys.exit(-1)
    build_arguments.append(compiler_name)

    if include_output_dir:
        output_file = compiler.get_output_file()
        if output_file is None:
            print("There was an error getting the output file.")
            sys.exit(-1)
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


def _build_unity(compiler: Compiler) -> bool:
    arguments = get_build_arguments(compiler)

    entry_point = compiler.get_entry_point()
    if entry_point != None:
        arguments.append(entry_point)
    else:
        print("No entry point could be found when running the program.")
        sys.exit(-1)

    return _run_compilation(arguments)


# TODO:
# If this functions fails while compiling an object file,
# the function will continue to try and compile the full
# executable. This will cause errors if the program
# tries to run the executable after.
def _build_standard(compiler: Compiler) -> bool:
    new_files = compiler.get_new_files()
    output_directory = pathlib.Path(compiler.get_output_file_name()).parent
    compilation_arguments = get_build_arguments(compiler, include_output_dir=False)

    object_extension: str
    match compiler.get_compiler():
        case "gcc" | "g++" | "clang" | "clang++" | "tcc":
            compilation_arguments.append("-c")
            object_extension = ".o"
        case "cl":
            compilation_arguments.append("/c")
            object_extension = ".obj"

    for file in new_files:
        original_file = pathlib.Path(file)
        file_object = str(output_directory / original_file.stem) + object_extension

        compilation_command = compilation_arguments.copy()
        compilation_command.extend([file, "-o", file_object])
        _run_compilation(compilation_command)

    object_files = [str(f) for f in output_directory.rglob(f"*{object_extension}") if f.is_file()]
    final_compilation_command = get_build_arguments(compiler, include_output_dir=True)
    final_compilation_command.extend(object_files)
    return _run_compilation(final_compilation_command)

def _build_full(compiler: Compiler) -> bool:
    build_arguments = get_build_arguments(compiler)

    files = compiler.get_all_files()
    build_arguments.extend(files)

    return _run_compilation(build_arguments)

# Returns true if the compilation was successfull.
def _run_compilation(arguments: list[str]) -> bool:
    compilation = subprocess.run(arguments, check=False, text=True, capture_output=True)

    errors = compilation.stderr

    if errors is not None and errors != "":
        print(errors)
        return False
    
    return True

def _run_output(application_name: str):
    subprocess.run([application_name], check=False, text=True, stderr=sys.stderr, stdout=sys.stdout)
    
def build(compiler: Compiler) -> bool:
    build_type = compiler.get_build_type()
    
    match build_type:
        case "unity":
            return _build_unity(compiler)
        case "standard":
            return _build_standard(compiler)
        case "full build":
            return _build_full(compiler)
        case _:
            print(f'The build type, "{build_type}" does not appear to be supported.')
            print(
                "The currently supported build types are:1. Standard\n2. Unity\n3. Full build"
            )
            sys.exit(-1)

def run(compiler: Compiler) -> None:
    build_succeeded = build(compiler)
    application_name = compiler.get_output_file_name()

    if build_succeeded: _run_output(application_name)
