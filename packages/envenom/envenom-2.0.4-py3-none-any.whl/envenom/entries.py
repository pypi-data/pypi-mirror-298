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

from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from envenom.vars import (
    Namespace,
    OptionalVar,
    Parser,
    RequiredVar,
    Var,
    VarWithDefault,
    VarWithDefaultFactory,
)

T = TypeVar("T")


@dataclass
class Entry(Generic[T], metaclass=ABCMeta):
    parser: Parser[T] = field()
    file: bool = field(kw_only=True, default=True)

    @abstractmethod
    def get_var(self, name: str, namespace: Namespace) -> Var[T]: ...


class RequiredEntry(Entry[T]):
    def get_var(self, name: str, namespace: Namespace) -> RequiredVar[T]:
        return RequiredVar(name, namespace, parser=self.parser, file=self.file)


class OptionalEntry(Entry[T]):
    def get_var(self, name: str, namespace: Namespace) -> OptionalVar[T]:
        return OptionalVar(name, namespace, parser=self.parser, file=self.file)


@dataclass
class EntryWithDefault(Entry[T]):
    default: T = field(kw_only=True)

    def get_var(self, name: str, namespace: Namespace) -> VarWithDefault[T]:
        return VarWithDefault(
            name,
            namespace,
            parser=self.parser,
            file=self.file,
            default=self.default,
        )


@dataclass
class EntryWithDefaultFactory(Entry[T]):
    default_factory: Callable[[], T] = field(kw_only=True)

    def get_var(self, name: str, namespace: Namespace) -> VarWithDefaultFactory[T]:
        return VarWithDefaultFactory(
            name,
            namespace,
            parser=self.parser,
            file=self.file,
            default_factory=self.default_factory,
        )
