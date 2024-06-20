"""
Locating a directory using the Windows registry
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

import os
import winreg


class LocateDir():
    """
    Locate the path to a directory
    """

    def __init__(self):
        self.__reg_hive = None
        self.__reg_path = None
        self.__located_dir = None

    def locate_dir(self):
        """
        Attempts to read the path to a specific directory.

        If successful, the located directory will be
        stored in 'self.__located_dir'.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            # Sets registry path and opens registry key
            reg_hive = winreg.__dict__[self.__reg_hive]
            reg_subkey = winreg.OpenKeyEx(
                reg_hive, self.__reg_path[0])
            reg_value = winreg.QueryValueEx(
                reg_subkey,
                self.__reg_path[1]
                )

            # Closes the registry key
            winreg.CloseKey(reg_subkey)

            # Expand environment variables in the registry value
            # and set the located directory
            self.__located_dir = os.path.expandvars(reg_value[0])
            result["success"] = True

        except FileNotFoundError as e:
            result["message"] = str(f"Excpetion: {e}")

        return result

    def get_dir(self):
        """
        Getter

        Returns:
            str: The located directory """
        return self.__located_dir

    def set_data(self, reg_hive, reg_path):
        """
        Setter

        Params:
            reg_hive (str): Registry hive
            reg_path (str): Registry path to directory
        """
        self.__reg_hive = reg_hive
        self.__reg_path = reg_path
