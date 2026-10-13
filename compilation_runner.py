from sys import exit
from config_reader import ConfigFile
from compiler import Compiler

#TODO
def _build_unity(compiler: Compiler):
    pass

#TODO
def _build_standard(compiler: Compiler):
    pass

#TODO
def _build_full(compiler: Compiler):
    pass

def build(compiler: Compiler):
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