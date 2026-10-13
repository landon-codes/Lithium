import configparser
import subprocess
from typing import Optional
from config_reader import ConfigFile


class Compiler:
    def __init__(self, config_data: ConfigFile):
        self._config = config_data

        # Reads the compilation data from the config file.
        # The compilation data is set to null if none is written.
        self._compilation_data: configparser.SectionProxy | None
        if self._config.contains_section("compilation"):
            self._compilation_data = self._config.get_section("compilation")
        else:
            self._compilation_data = None

        # Reads the build type from the config file.
        # The build type is set to null if none is written.
        self._build_data: configparser.SectionProxy | None
        if self._config.contains_section("build type"):
            self._build_data = self._config.get_section("build type")
        else:
            self._build_data = None

    def get_compiler(self) -> str | None:
        if self._compilation_data == None:
            return None

        if "compiler" in self._compilation_data:
            return self._compilation_data["compiler"]
        else:
            Compiler._detect_compilers()

    @staticmethod  # TODO: Implement automatic compiler detection
    def _detect_compilers() -> str | None:         
        compiler_calls = {
            "clang": ["clang", "--version"],
            "g++": ["g++", "--version"],
            "gcc": ["gcc", "--version"],
            "msvc": ["cl", "--version"],
            "tcc": ["tcc", "--version"]
        }

        for compiler, value in compiler_calls.items():
            try:
                subprocess.run(value, capture_output=True, check=True, text=True)
                return compiler
            finally: pass
