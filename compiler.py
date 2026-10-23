import configparser
import os
import pathlib
import subprocess
from datetime import datetime
from sys import exit

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
                case "gcc" | "g++" | "clang" | "clang++":
                    return f"-std={standard}"
                case "tcc":
                    print("TCC does not support configuration of the standard.")
                    exit(-1)
                case "cl":
                    return f"/std:{standard}"

    def get_extra_warnings(self) -> list[str] | None:
        default_value = None

        if self._compilation_data == None:
            return default_value

        if (
            "extra_warnings" in self._compilation_data
            and self._compilation_data.getboolean("extra_warnings")
        ):
            compiler = self.get_compiler()
            match compiler:
                case "gcc" | "g++" | "clang" | "clang++":
                    return ["-Wall", "-Wextra"]
                case "tcc":
                    return ["-Wall"]
                case "cl":
                    return ["/W4"]
        else:
            return default_value

    def get_warning_error(self) -> str | None:
        default_value = None

        if self._compilation_data == None:
            return default_value

        if (
            "warning_error" in self._compilation_data
            and self._compilation_data.getboolean("warning_error")
        ):
            compiler = self.get_compiler()
            match compiler:
                case "gcc" | "g++" | "clang" | "clang++":
                    return "-Werror"
                case "tcc":
                    print("Compiling warnings as errors is not supported by tcc.")
                    exit(-1)
                case "cl":
                    return "/WX"
        else:
            return default_value

    def get_enable_extensions(self) -> str | None:
        default_value = None

        if self._compilation_data == None:
            return default_value

        if (
            "enable_extentions" in self._compilation_data
            and not self._compilation_data.getboolean("enable_extensions")
        ):
            compiler = self.get_compiler()
            match compiler:
                case "gcc" | "g++" | "clang" | "clang++":
                    return "-pedantic-errors"
                case "tcc":
                    print("Disabling GNU extensions is not supported by tcc.")
                    exit(-1)
                case "cl":
                    language = self._detect_language()

                    if language == "c":
                        return "/W4"
                    elif language == "c++":
                        return "/permissive-"

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

    def get_all_files(self) -> list[str]:
        if self._build_data != None and "files" in self._build_data:
            # .ini files do not natively support lists, so instead we use a
            # string where files are seperated by commas.
            files_str = self._build_data["files"]
            files = [f.strip() for f in files_str.split(",") if f.strip()]

            # Remove extra quotes from the file names
            files[0] = files[0][1:]
            file_len = len(files[1])
            files[1] = files[1][0 : file_len - 1]

            return files
        else:
            return self._detect_files()

    def get_new_files(self) -> list[str]:
        output_directory = pathlib.Path(self.get_output_file_name()).parent
        files_found: list[str] = []

        all_files = self.get_all_files()

        object_extension: str
        match os.name:
            case "nt":
                object_extension = ".obj"
            case _:
                object_extension = ".o"

        for file in all_files:
            original_path = pathlib.Path(file)
            object_file = output_directory / (original_path.stem + object_extension)

            if not object_file.exists():
                files_found.append(str(original_path))
                continue

            original_path_modification_date = datetime.fromtimestamp( # noqa DTZ006
                original_path.stat().st_mtime
            )  
            object_file_modification_date = datetime.fromtimestamp( # noqa DTZ006
                object_file.stat().st_mtime
            )

            if original_path_modification_date > object_file_modification_date:
                files_found.append(str(original_path))

        return files_found

    def get_output_file_name(self) -> str:
        default_value = "bin/main"
        output_name: str

        if self._build_data is not None:
            output_name = default_value

        if self._build_data is not None and "output_name" in self._build_data:
            output_name = self._build_data["output_name"]
        else:
            output_name = default_value

        os_extension: str
        match os.name:
            case "nt":
                os_extension = ".exe"
            case _:
                os_extension = ""

        return output_name + os_extension

    def get_output_file(self) -> list[str] | None:
        output_name = self.get_output_file_name()

        match self.get_compiler():
            case "gcc" | "g++" | "clang" | "clang++" | "tcc":
                return ["-o", f"{output_name}"]
            case "cl":
                return [f'/Fe"{output_name}"']

    # It appears that msvc (cl) does not support forcing colored output.
    # TCC doesn't support colored output at all.
    def get_argument_for_colored_output(self) -> str | None:
        compiler = self.get_compiler()

        match compiler:
            case "clang" | "clang++":
                return "-fcolor-diagnostics"
            case "gcc" | "g++":
                return "-fdiagnostics-color=always"

    @staticmethod
    def _detect_compilers() -> str | None:
        compiler_calls = {
            "clang": ["clang", "--version"],
            "g++": ["g++", "--version"],
            "gcc": ["gcc", "--version"],
            "msvc": ["cl", "--version"],
            "tcc": ["tcc", "--version"],
        }

        for compiler, value in compiler_calls.items():
            try:
                subprocess.run(value, capture_output=True, check=True, text=True)
                return compiler
            finally:
                pass

    def _detect_language(self) -> str | None:
        # Try to get the language from the entry point
        entry_point = self.get_entry_point()
        if entry_point != None:
            suffix = pathlib.Path(entry_point).suffix
            match suffix:
                case ".c":
                    return "c"
                case ".cpp" | ".c++":
                    return "c++"

        # If the entry point fails, try detecting it manually
        project_root = self._config.get_file_path().parent
        project_files = [f for f in project_root.rglob("*") if f.is_file()]

        for file in project_files:
            if file.suffix == ".c":
                return "c"
            elif file.suffix == ".cpp" or file.suffix == ".c++":
                return "c++"

    def _detect_files(self) -> list[str]:
        language = self._detect_language()
        project_root = self._config.get_file_path().parent

        if language == None:
            print(
                "The project language could not be detected when trying to detect the project files."
            )
            exit(-1)

        files: list[str]

        if language == "c":
            files = [str(f) for f in project_root.rglob("*.c") if f.is_file()]
        elif language == "c++":
            files = [str(f) for f in project_root.rglob("*.cpp") if f.is_file()]

            # Tries searching for .c++ files if no .cpp files are found.
            if len(files) < 1:
                files = [str(f) for f in project_root.rglob("*.c++") if f.is_file()]

        if len(files) < 1:
            print("No files could be detected in the project.")
            exit(-1)

        return files
