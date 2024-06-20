"""
Locates the Creature Mind file using the Windows registry.
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

import winreg


class LocateMindFile():
    """
    Class to locate the creature mind file
    """

    def __init__(self):
        self.__reg_hive = None
        self.__reg_path = None
        self.__backup_profile = None
        self.__creature_mind = None

    def locate_file(self):
        """
        Attempts to locate the creature mind file.

        If successful, the mind file will be stored in 'self.__creature_mind'.

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
                reg_hive,
                self.__reg_path[0] +
                self.__reg_path[1] +
                "\\" +
                self.__backup_profile
                )

            # Queries the specified value from the registry key
            reg_value = winreg.QueryValueEx(
                reg_subkey, self.__reg_path[2])

            # Closes the registry key
            winreg.CloseKey(reg_subkey)

            # Sets the creature mind with the retrieved registry value
            self.__creature_mind = reg_value[0]
            result["success"] = True

        except FileNotFoundError as e:
            result["message"] = str(f"Excpetion: {e}")

        return result

    def get_mind_file(self):
        """
        Getter

        Returns:
            str: Located creature mind
        """
        return self.__creature_mind

    def set_data(self, reg_hive, reg_path, backup_profile):
        """
        Setter

        Params:
            reg_hive (str): Registry hive
            reg_path (list): Registry path to directory
            backup_profile (str): Selected backup profile
        """
        self.__reg_hive = reg_hive
        self.__reg_path = reg_path
        self.__backup_profile = backup_profile
