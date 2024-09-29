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

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any, TypeVar

from envenom.entries import (
    Entry,
    EntryWithDefault,
    EntryWithDefaultFactory,
    OptionalEntry,
    RequiredEntry,
)
from envenom.vars import Var

# Why so much 'type: ignore' around here?
#
# It's a hard truth to accept, but dataclasses are lying to us.
#
# When the `field` function is called it creates a Field[T] object, but it tells
# us that it really returns a T (or sometimes None), I swear, pretty please.
#
# Because we're exposing a similar interface and hooking into this exact layer,
# we therefore need to:
#   1) ignore the return value from `field`; it's a lie anyway
#   2) lie to our consumers on the API side just like `field` would, except of
#      course we supply three versions of the `field` function, so we need
#      to lie on all three fronts.


T = TypeVar("T")


def config(
    namespace: Sequence[str] | str | None = None,
) -> Callable[[type[T]], type[T]]:
    """
    Defines a new config class.

    Parameters:
        namespace:  Namespace to pull config values from. This allows different
                    configuration items with the same base name to exist in different
                    contexts. Can be specified either as a single `str` or a Sequence
                    of `str`s.

    Returns:
        A callable which transforms a class into a new config class.

    Example:
        Use this as a class decorator:

        ```python
        from envenom import config, required


        @config()
        class AppCfg:
            secret_key: str = required()
        ```

    """

    def __wrapper(cls: type[T]) -> type[T]:
        var: Var[Any]
        new_fields: dict[str, Any] = {
            name: field(
                init=False,
                repr=True,
                hash=True,
                default_factory=(var := entry.get_var(name, namespace)).get,
                metadata={
                    "config": cls,
                    "type": cls.__annotations__[name],
                    "var": var,
                },
            )
            for name, entry in cls.__dict__.items()
            if isinstance(entry, Entry) and name in cls.__annotations__
        }

        for name, f in new_fields.items():
            setattr(cls, name, f)

        return dataclass(frozen=True, eq=True)(cls)

    return __wrapper


def required(parser: Callable[[str], T] = str, *, file: bool = True) -> T:
    """
    Creates a required config field.

    Fields created with this function will have a type of `T`.

    Parameters:
        parser: Callable which will convert a single `str` into the
                desired object type.
        file:   Whether to try and retrieve the configuration value from a file
                using the environment variable with the `__FILE` suffix.

    Returns:
        An object of type `T` instantiated from the environment.

    Example:
        ```python
        from envenom import config, required


        @config()
        class AppCfg:
            secret_key: str = required()
        ```

    """

    return RequiredEntry(parser, file=file)  # type: ignore (2)


def optional(parser: Callable[[str], T] = str, *, file: bool = True) -> T | None:
    """
    Creates an optional config field.

    Fields created with this function will have a type of `T | None`.

    Parameters:
        parser: Callable which will convert a single `str` into the
                desired object type.
        file:   Whether to try and retrieve the configuration value from a file
                using the environment variable with the `__FILE` suffix.

    Returns:
        An object of type `T` instantiated from the environment if available,
            otherwise `None`.

    Example:
        ```python
        from envenom import config, optional


        @config()
        class AppCfg:
            signature: str | None = optional()
        ```

    """

    return OptionalEntry(parser, file=file)  # type: ignore (2)


def with_default(
    parser: Callable[[str], T] = str, *, file: bool = True, default: T
) -> T:
    """
    Creates an optional config field with a default value.

    Fields created with this function will have a type of `T`.

    Parameters:
        parser:     Callable which will convert a single `str` into the
                    desired object type.
        file:       Whether to try and retrieve the configuration value from a file
                    using the environment variable with the `__FILE` suffix.
        default:    The default to return if value is not set in the environment.

    Returns:
        An object of type `T` instantiated from the environment if available,
            otherwise the default value.

    Example:
        ```python
        from envenom import config, with_default
        from envenom.parsers import bool_parser


        @config()
        class AppCfg:
            feature_flag: bool = with_default(bool_parser(), default=False)
        ```

    """

    return EntryWithDefault(parser, file=file, default=default)  # type: ignore (2)


def with_default_factory(
    parser: Callable[[str], T] = str,
    *,
    file: bool = True,
    default_factory: Callable[[], T],
) -> T:
    """
    Creates an optional config field with a default value factory.

    Fields created with this function will have a type of `T`.

    Parameters:
        parser:             Callable which will convert a single `str` into the
                            desired object type.
        file:               Whether to try and retrieve the configuration value from a
                            file using the environment variable with the `__FILE`
                            suffix.
        default_factory:    The default factory to call if value is not set in the
                            environment.

    Returns:
        An object of type `T` instantiated from the environment if available,
            otherwise the value created by calling the default factory.

    Example:
        ```python
        from uuid import UUID, uuid4

        from envenom import config, with_default_factory


        @config()
        class AppCfg:
            uuid: UUID = with_default_factory(UUID, default_factory=uuid4)
        ```

    """

    return EntryWithDefaultFactory(
        parser,
        file=file,
        default_factory=default_factory,
    )  # type: ignore (2)


def subconfig(cls: Callable[[], T], /) -> T:
    """
    Includes another config class as a field of the current config class.

    This is really a convenvience function for expressing a dataclass
    field with a default factory, but it expresses the intention better too.

    `subconfig(cls)` is equivalent to `field(default_factory=cls)`.

    This function, unlike others in this module, is compatible with the
    standard `@dataclass` decorator.

    Parameters:
        cls:  Subconfig class to include as a field in this config class.

    Returns:
        An instantiated object of the subconfig class.

    Example:
        ```python
        from envenom import config, required, subconfig


        @config()
        class SubCfg:
            secret_key: str = required()


        @config()
        class AppCfg:
            subcfg: SubCfg = subconfig(SubCfg)
        ```
    """

    return field(default_factory=cls)
