import configparser
from pathlib import Path


class ConfigFile:
    def __init__(self, file_path: Path):
        self._file_path = file_path

        self._config = configparser.ConfigParser()
        self._config.read(self._file_path)

    def get_file_path(self) -> Path:
        return self._file_path

    def get_section(self, section_name: str) -> configparser.SectionProxy:
        return self._config[section_name]

    def contains_section(self, section_name: str) -> bool:
        return section_name in self._config
