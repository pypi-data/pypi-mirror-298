# `quesadilla` - an elegant background task queue for the more civilized age
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

from importlib.metadata import entry_points

import typer

app = typer.Typer(
    name="quesadilla",
    help="quesadilla - an elegant background task queue for the more civilized age",
    add_completion=False,
)


@app.command(help="Show license (GPL-3.0-or-later)")
def license() -> None:
    typer.echo(
        "quesadilla - an elegant background task queue for the more civilized age\n"
        "Copyright (C) 2024 Artur Ciesielski <artur.ciesielski@gmail.com>\n"
        "\n"
        "This program is free software: you can redistribute it and/or modify\n"
        "it under the terms of the GNU General Public License as published by\n"
        "the Free Software Foundation, either version 3 of the License, or\n"
        "(at your option) any later version.\n"
        "\n"
        "This program is distributed in the hope that it will be useful,\n"
        "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
        "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
        "GNU General Public License for more details.\n"
        "\n"
        "You should have received a copy of the GNU General Public License\n"
        "along with this program.  If not, see <https://www.gnu.org/licenses/>."
    )


@app.command(help="Show brief description of this library")
def about() -> None:
    name = typer.style("quesadilla", fg=typer.colors.BRIGHT_GREEN)
    link = typer.style(
        "https://gitlab.com/arcanery/python/quesadilla/quesadilla",
        fg=typer.colors.BRIGHT_BLUE,
    )
    typer.echo(
        f"Command line interface for {name}, \n"
        "an elegant background task queue for the more civilized age.\n"
        "\n"
        "For more information about the project, see the main project's homepage: \n"
        f"{link}"
    )


for entry_point in entry_points(group="quesadilla.cli"):
    app.add_typer(entry_point.load())


if __name__ == "__main__":
    app()
