import configparser
import subprocess
from typing import Optional
from config_reader import ConfigFile
from sys import exit


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
            return self._detect_compilers()

        if "compiler" in self._compilation_data:
            return self._compilation_data["compiler"]
        else:
            return self._detect_compilers()

    def get_standard(self) -> str | None:
        if self._compilation_data == None:
            return None

        if "standard" in self._compilation_data:
            standard = self._compilation_data["standard"]

            compiler = self.get_compiler()
            match compiler:
                case "gcc" | "g++" | "clang":
                    return f"-std={standard}"
                case "tcc":
                    print("TCC does not support configuration of the standard.")
                    exit(-1)
                case "cl":
                    return f"/std:{standard}"
                


    def get_extra_warnings(self) -> str | None:
        default_value = None

        if self._compilation_data == None:
            return default_value

        if "extra_warnings" and bool(self._compilation_data["extra_warnings"]):
            compiler = self.get_compiler()
            match compiler:
                case "gcc" | "g++" | "clang":
                    return "-Wall -Wextra"
                case "tcc":
                    return "-Wall"
                case "cl":
                    return "/W4"
        else:
            return default_value

    def get_warning_error(self) -> bool:
        default_value = False

        if self._compilation_data == None:
            return default_value

        if "warning_error" in self._compilation_data and bool(self._compilation_data["warning_error"]):
            compiler = self.get_compiler()
            match compiler:
                case "gcc" | "g++" | "clang":
                    return "-Werror"
                case "tcc":
                    print("Compiling warnings as errors is not supported by tcc.")
                    exit(-1)
                case "cl":
                    return "/WX"
        else:
            return default_value

    def get_enable_extensions(self) -> bool:
        default_value = False

        if self._compilation_data == None:
            return default_value

        if "enable_extentions" in self._compilation_data:
            return self._compilation_data["enable_extensions"]
        else:
            return default_value

    def get_build_type(self) -> str:
        default_value = "standard"

        if self._build_data == None:
            return default_value

        if "type" in self._build_data:
            return self._build_data["type"]
        else:
            return default_value

    def get_entry_point(self) -> str | None:
        if self._build_data != None and "entry_point" in self._build_data:
            return self._build_data["entry_point"]

    @staticmethod 
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
