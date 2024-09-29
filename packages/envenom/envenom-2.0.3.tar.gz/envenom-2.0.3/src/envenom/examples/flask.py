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

from typing import TypedDict

from flask import Flask

from envenom import config, with_default
from envenom.parsers import bool_parser


@config()
class FlaskCfg:
    static_docs: bool = with_default(bool_parser(), default=True)
    interactive_docs: bool = with_default(bool_parser(), default=False)


@config(namespace="app")
class AppCfg:
    motd: str = with_default(default="This is the default message of the day.")


cfg = FlaskCfg()
app = Flask(__name__)


class IndexResponse(TypedDict):
    motd: str


@app.route("/")
def index() -> IndexResponse:
    return {"motd": AppCfg().motd}


if cfg.static_docs:

    @app.route("/redoc")
    def static_docs() -> str:
        return "Static docs would be here if Flask had them built-in."


if cfg.interactive_docs:

    @app.route("/docs")
    def interactive_docs() -> str:
        return "Interactive docs would be here if Flask had them built-in."
