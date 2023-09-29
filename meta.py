import tomllib
from typing import Any


class ProjectMeta:
    """Meta information about the project"""

    _default_version: str = "x.x.x"
    _default_title = _default_description = "Pocket Assistant"

    def __init__(self, file_path: str = "pyproject.toml") -> None:
        self._data: dict[str, Any] = self._fetch_data(file_path)

    @staticmethod
    def _fetch_data(file_path: str) -> dict[str, Any]:
        """Method that parses 'pyproject.toml' file and returns dictionary with data from it"""
        try:
            with open(file_path, "rb") as file:
                poetry_data: dict[str, Any] = tomllib.load(file).get("tool", {}).get("poetry", {})
        except (FileNotFoundError, tomllib.TOMLDecodeError):
            poetry_data: dict[str, Any] = {}
        return poetry_data

    @property
    def title(self) -> str:
        """Title of the project"""
        return self._data.get("name", self._default_title)

    @property
    def version(self) -> str:
        """Version of the project"""
        return self._data.get("version", self._default_version)

    @property
    def description(self) -> str:
        """Description of the project"""
        return self._data.get("description", self._default_description)
