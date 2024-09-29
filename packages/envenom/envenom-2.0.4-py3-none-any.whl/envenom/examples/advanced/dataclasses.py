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

from dataclasses import dataclass, field
from functools import cached_property

from envenom import config, optional, required, subconfig


def derive_public_key(private_key: str) -> str:
    return private_key[:8]


@config("jwt")
class JWTCfg:
    issuer: str = field(default="https://example.com")
    private_key: str = required()
    public_key: str | None = optional()

    @cached_property
    def current_public_key(self) -> str:
        return self.public_key or derive_public_key(self.private_key)


@dataclass
class OAuth2Cfg:
    jwt: JWTCfg = subconfig(JWTCfg)  # subconfig can be used in @dataclass!
    supports_oidc: bool = field(default=True)


@config()
class ApplicationCfg:
    secret_key: str = required()
    oauth2: OAuth2Cfg = subconfig(OAuth2Cfg)


if __name__ == "__main__":
    cfg = ApplicationCfg()

    # fmt: off
    # flake8: noqa
    print(f"cfg.secret_key ({type(cfg.secret_key)}): {repr(cfg.secret_key)}")
    print(f"cfg.oauth2.supports_oidc ({type(cfg.oauth2.supports_oidc)}): {repr(cfg.oauth2.supports_oidc)}")
    print(f"cfg.oauth2.jwt.issuer ({type(cfg.oauth2.jwt.issuer)}): {repr(cfg.oauth2.jwt.issuer)}")
    print(f"cfg.oauth2.jwt.private_key ({type(cfg.oauth2.jwt.private_key)}): {repr(cfg.oauth2.jwt.private_key)}")
    print(f"cfg.oauth2.jwt.public_key ({type(cfg.oauth2.jwt.public_key)}): {repr(cfg.oauth2.jwt.public_key)}")
    print(f"cfg.oauth2.jwt.current_public_key ({type(cfg.oauth2.jwt.current_public_key)}): {repr(cfg.oauth2.jwt.current_public_key)}")
    # fmt: on
