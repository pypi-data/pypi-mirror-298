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

from uuid import UUID, uuid4

from envenom import config, optional, required, with_default_factory


@config()
class UUIDCfg:
    admin_user_uuid: UUID = required(UUID)
    manager_user_uuid: UUID | None = optional(UUID)
    random_uuid_if_unset: UUID = with_default_factory(UUID, default_factory=uuid4)


if __name__ == "__main__":
    cfg = UUIDCfg()

    # fmt: off
    # flake8: noqa
    print(f"cfg.admin_user_uuid ({type(cfg.admin_user_uuid)}): {repr(cfg.admin_user_uuid)}")
    print(f"cfg.manager_user_uuid ({type(cfg.manager_user_uuid)}): {repr(cfg.manager_user_uuid)}")
    print(f"cfg.random_uuid_if_unset ({type(cfg.random_uuid_if_unset)}): {repr(cfg.random_uuid_if_unset)}")
    # fmt: on
