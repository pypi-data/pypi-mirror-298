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


from envenom import config, optional, required


@config()
class MainCfg:
    some_value: str = required()
    other_value: str | None = optional(file=False)


if __name__ == "__main__":
    cfg = MainCfg()

    # fmt: off
    # flake8: noqa
    print(f"cfg.some_value ({type(cfg.some_value)}): {repr(cfg.some_value)}")
    print(f"cfg.other_value ({type(cfg.other_value)}): {repr(cfg.other_value)}")
    # fmt: on
