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
from typing import Generic, TypeVar

from envenom import config, optional, required
from envenom.parsers import bool_parser, list_parser

T = TypeVar("T")


@dataclass
class Box(Generic[T]):
    item: T


def boxed_int(v: str) -> Box[int]:
    return Box(item=int(v))


def boxed_bytes(v: str) -> Box[bytes]:
    return Box(item=v.encode())


@config()
class MainCfg:
    boxed_int: Box[int] = required(boxed_int)
    boxed_bytes: Box[bytes] = required(boxed_bytes)

    default_boolean: bool = required(bool_parser())
    custom_boolean: bool = required(
        bool_parser(true_values={"mhm"}, false_values={"uhhuh"})
    )

    required_list: list[str] = required(list_parser())
    required_empty_list: list[str] = required(list_parser())
    optional_list: list[str] | None = optional(list_parser())
    optional_empty_list: list[str] | None = optional(list_parser())
    optional_not_provided_list: list[str] | None = optional(list_parser())
    custom_list: list[int] = required(list_parser(int, separator=";"))


if __name__ == "__main__":
    cfg = MainCfg()

    # fmt: off
    # flake8: noqa
    print(f"cfg.boxed_int ({type(cfg.boxed_int)}): {repr(cfg.boxed_int)}")
    print(f"cfg.boxed_int.item ({type(cfg.boxed_int.item)}): {repr(cfg.boxed_int.item)}")
    print(f"cfg.boxed_bytes ({type(cfg.boxed_bytes)}): {repr(cfg.boxed_bytes)}")
    print(f"cfg.boxed_bytes.item ({type(cfg.boxed_bytes.item)}): {repr(cfg.boxed_bytes.item)}")
    print(f"cfg.default_boolean ({type(cfg.default_boolean)}): {repr(cfg.default_boolean)}")
    print(f"cfg.custom_boolean ({type(cfg.custom_boolean)}): {repr(cfg.custom_boolean)}")
    print(f"cfg.required_list ({type(cfg.required_list)}): {repr(cfg.required_list)}")
    print(f"cfg.required_empty_list ({type(cfg.required_empty_list)}): {repr(cfg.required_empty_list)}")
    print(f"cfg.optional_list ({type(cfg.optional_list)}): {repr(cfg.optional_list)}")
    print(f"cfg.optional_empty_list ({type(cfg.optional_empty_list)}): {repr(cfg.optional_empty_list)}")
    print(f"cfg.optional_not_provided_list ({type(cfg.optional_not_provided_list)}): {repr(cfg.optional_not_provided_list)}")
    print(f"cfg.custom_list ({type(cfg.custom_list)}): {repr(cfg.custom_list)}")
    # fmt: on
