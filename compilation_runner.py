import os
import subprocess
import sys

from compiler import Compiler

"""
Returns the first part of the build command.
It contains the compiler name and all the arguments.
The responsibility to get the proper files and
finish the command falls on the other functions.
"""


def _get_build_arguments(compiler: Compiler) -> list[str]:
    build_arguments = []

    compiler_name = compiler.get_compiler()
    if compiler_name == None:
        print("No supported compiler could be found.")
        sys.exit(-1)
    build_arguments += compiler_name

    standard = compiler.get_standard()
    if standard != None:
        build_arguments += standard

    extra_warnings = compiler.get_extra_warnings()
    if extra_warnings != None:
        build_arguments += extra_warnings

    warning_error = compiler.get_warning_error()
    if warning_error != None:
        build_arguments += warning_error

    extensions_enabled = compiler.get_enable_extensions
    if extensions_enabled != None:
        build_arguments.append(extensions_enabled)

    return build_arguments


# TODO
def _build_unity(compiler: Compiler) -> None:
    arguments = _get_build_arguments(compiler)

    entry_point = compiler.get_entry_point()
    if entry_point != None:
        arguments.append(entry_point)
    else:
        print("No entry point could be found when running the program.")
        sys.exit(-1)

    subprocess.run(arguments, check=False, stderr=sys.stderr, text=True)


# TODO
def _build_standard(compiler: Compiler) -> None:
    print("Standard builds are not supported yet.")
    sys.exit(-1)


# TODO
def _build_full(compiler: Compiler) -> None:
    print("Full builds are not supported yet.")
    sys.exit(-1)


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


# TODO: Implement the option for application names on build
def run(compiler: Compiler) -> None:
    build(compiler)

    # Detect OS format
    application_name: str
    match os.name:
        case "nt":
            application_name = "./a.exe"
        case _:
            application_name = "./a.out"

    subprocess.run([application_name], check=False, text=True, stderr=sys.stderr)
