"""
Imports the registry key of the backup
"""

# This file is part of Black & White Savegame Backup.
#
# Black & White Savegame Backup is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# Black & White Savegame Backup is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the  GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Black & White Savegame Backup.
# If not, see <http://www.gnu.org/licenses/>.

import subprocess


class ImportRegkey():
    """
    Class for importing the registration key
    """

    def __init__(self):
        self.__path = None
        self.__reg_file = None

    def import_regkey(self):
        """
        Attempts to import the registry key.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            # Set path to .reg-file
            import_file = self.__path + "\\" + self.__reg_file

            # imports the key
            subprocess.run(
                ["reg", "import", import_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
                )

            result["success"] = True

        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            result["message"] = str(f"Exception: {e}")

        return result

    def set_data(self, path, reg_file):
        """
        Setter

        Params:
            path (str): Path to .reg file
            reg_file (str): name of .reg file
        """
        self.__path = path
        self.__reg_file = reg_file
