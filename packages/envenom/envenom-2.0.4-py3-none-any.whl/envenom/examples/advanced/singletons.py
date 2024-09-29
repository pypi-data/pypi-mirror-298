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

from typing import Any, Generic, TypeVar

from envenom import config

T = TypeVar("T")


class Singleton(type, Generic[T]):
    __instances: dict[type[Any], Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> T:
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


@config()
class DefaultMainCfg:
    pass


@config()
class CachedMainCfg(metaclass=Singleton["CachedMainCfg"]):
    pass


if __name__ == "__main__":
    default_cfg1 = DefaultMainCfg()
    default_cfg2 = DefaultMainCfg()
    cached_cfg1 = CachedMainCfg()
    cached_cfg2 = CachedMainCfg()

    print("id(default_cfg1) should not be same as id(default_cfg2)")
    print(f"{id(default_cfg1)=}")
    print(f"{id(default_cfg2)=}")
    print("id(cached_cfg1) should be same as id(cached_cfg2)")
    print(f"{id(cached_cfg1)=}")
    print(f"{id(cached_cfg2)=}")
