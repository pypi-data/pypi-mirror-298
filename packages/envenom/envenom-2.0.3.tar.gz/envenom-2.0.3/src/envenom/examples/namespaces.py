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

from envenom import config, required, subconfig


@config(("app", "cfg"))
class OtherNamespaceCfg:
    some_value: str = required()


@config(("ns1", "ns-2"))
class NestedNamespaceCfg:
    some_value: str = required()


@config("ns1")
class SimpleNamespaceCfg:
    some_value: str = required()
    nested_namespace: NestedNamespaceCfg = subconfig(NestedNamespaceCfg)


@config()
class MainCfg:
    some_value: str = required()
    simple_namespace: SimpleNamespaceCfg = subconfig(SimpleNamespaceCfg)
    other_namespace: OtherNamespaceCfg = subconfig(OtherNamespaceCfg)


if __name__ == "__main__":
    cfg = MainCfg()

    # fmt: off
    # flake8: noqa
    print(f"cfg.some_value ({type(cfg.some_value)}): {repr(cfg.some_value)}")
    print(f"cfg.simple_namespace.some_value ({type(cfg.simple_namespace.some_value)}): {repr(cfg.simple_namespace.some_value)}")
    print(f"cfg.simple_namespace.nested_namespace.some_value ({type(cfg.simple_namespace.nested_namespace.some_value)}): {repr(cfg.simple_namespace.nested_namespace.some_value)}")
    print(f"cfg.other_namespace.some_value ({type(cfg.other_namespace.some_value)}): {repr(cfg.other_namespace.some_value)}")
    # fmt: on
