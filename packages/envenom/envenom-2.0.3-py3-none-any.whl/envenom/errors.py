# `envenom` - an elegant application configurator for the more civilized age
# Copyright (C) 2024 Artur Ciesielski <artur.ciesielski@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from dataclasses import dataclass


class GenericError(Exception):
    """
    Base exception class for any errors raised by `envenom`.
    """

    def __str__(self) -> str:
        return "error"

    def __format__(self, __format_spec: str) -> str:
        match __format_spec:
            case "class":
                return self.__class__.__name__
            case _:
                return str(self)


@dataclass
class ConfigurationError(GenericError):
    """
    Base exception class for any errors raised by `envenom`
    relating to a specific configuration field.
    """

    name: str

    def __str__(self) -> str:
        return f"error for configuration '{self.name}'"

    def __format__(self, __format_spec: str) -> str:
        if __format_spec == "var":
            return self.name
        return super().__format__(__format_spec)


class MissingConfiguration(ConfigurationError):
    """
    Raised when a required configuration entry is missing in the environment.
    """

    def __str__(self) -> str:
        return f"missing value for configuration '{self.name}'"


@dataclass
class InvalidConfiguration(ConfigurationError):
    """
    Raised when the value for a specific field is invalid.

    Most commonly raised when `ValueError` is raised from a field parser.
    """

    value: str

    def __str__(self) -> str:
        return f"invalid value '{self.value}' for configuration '{self.name}'"

    def __format__(self, __format_spec: str) -> str:
        if __format_spec == "value":
            return self.value
        return super().__format__(__format_spec)


class ConfigurationFileUnreadable(InvalidConfiguration):
    """
    Raised when an environment variable with a `__FILE` suffix is set and
    the value cannot be read from the file.
    """

    def __str__(self) -> str:
        return f"unreadable file '{self.value}' for configuration '{self.name}'"
