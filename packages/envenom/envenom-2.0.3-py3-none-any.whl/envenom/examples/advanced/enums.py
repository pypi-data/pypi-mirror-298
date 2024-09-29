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

import enum

from envenom import config, optional, required, with_default


class ExitCode(enum.IntEnum):
    OK = 0
    MISSING_CONFIG = 1
    INVALID_CONFIG = 2
    CONFIG_FILE_UNREADABLE = 3


class LaunchCode(enum.StrEnum):
    OK = enum.auto()
    LAUNCHPAD_OBSTRUCTED = enum.auto()
    NOT_ENOUGH_FUEL = enum.auto()
    OVERRIDDEN = enum.auto()


class DaVinciCode(enum.Enum):
    UNSOLVED = enum.auto()
    SOLVED = enum.auto()


@config()
class EnumCfg:
    exit_code: ExitCode = required(lambda c: ExitCode(int(c)))
    launch_code: LaunchCode | None = optional(lambda c: LaunchCode(c))
    davinci_code: DaVinciCode = with_default(
        lambda c: DaVinciCode(int(c)), default=DaVinciCode.UNSOLVED
    )


if __name__ == "__main__":
    cfg = EnumCfg()

    print(f"cfg.exit_code ({type(cfg.exit_code)}): {repr(cfg.exit_code)}")
    print(f"cfg.launch_code ({type(cfg.launch_code)}): {repr(cfg.launch_code)}")
    print(f"cfg.davinci_code ({type(cfg.davinci_code)}): {repr(cfg.davinci_code)}")
