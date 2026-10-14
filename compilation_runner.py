from sys import exit
from config_reader import ConfigFile
from compiler import Compiler
import subprocess

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
        exit(-1)
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
        build_arguments += extensions_enabled

    return build_arguments

#TODO
def _build_unity(compiler: Compiler) -> None:
    arguments = _get_build_arguments(compiler)

    entry_point = compiler.get_entry_point()
    arguments.append(entry_point)

    subprocess.run(arguments)

#TODO
def _build_standard(compiler: Compiler) -> None:
    pass

#TODO
def _build_full(compiler: Compiler) -> None:
    pass

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
            print(f"The build type, \"{build_type}\" does not appear to be supported.")
            print("The currently supported build types are:1. Standard\n2. Unity\n3. Full build")
            exit(-1)