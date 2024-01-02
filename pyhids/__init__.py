"""
pyHIDS. Python HIDS. Security software.
pyHIDS verify the integrity of your system.
Copyright (C) 2010-2024 Cedric Bonhomme

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

pyHIDS Copyright (C) 2010-2024 Cedric Bonhomme
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
"""

import importlib
import os
import subprocess
from importlib.metadata import PackageNotFoundError

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_version() -> str:
    """Returns the version of the software.
    Checks if the Python package is installed or uses the Git tag."""
    try:
        version = (
            os.environ.get("PKGVER")
            or subprocess.run(
                ["git", "-C", BASE_DIR, "describe", "--tags"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )
            .stdout.decode()
            .strip()
        ) or ""
    except Exception:
        version = ""
    if not version:
        try:
            version = "v" + importlib.metadata.version("pyhids")  # type: ignore
        except PackageNotFoundError:
            version = ""
    return version
