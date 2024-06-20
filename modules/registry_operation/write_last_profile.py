"""
Writes the profile name of the backup to be restored
as thelast used profile name.

If this value is empty (e.g. new installed game), the
game will otherwise crash at startup.
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


class WriteLastProfile:
    """
    Class for writing the last used profile in the registry
    """

    def __init__(self):
        self.__reg_hive = None
        self.__reg_path = None
        self.__profile_name = None

    def write_profile_name(self):
        """
        Writes the last used profile into the registration

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            # Converts the profile name to the corresponding format
            converted_name = self.__profile_name.replace("_", "") + "."
            binary_data = converted_name.encode('utf-16le')

            # Sets registry path and opens registry key
            reg_hive = winreg.__dict__[self.__reg_hive]
            reg_subkey = winreg.OpenKeyEx(
                reg_hive,
                self.__reg_path[0],
                0,
                winreg.KEY_SET_VALUE
                )

            # Writing the binary value to the registry
            winreg.SetValueEx(
                reg_subkey,
                self.__reg_path[3],
                0,
                winreg.REG_BINARY,
                binary_data
                )

            # Closes the registry key
            winreg.CloseKey(reg_subkey)

            result["success"] = True

        except FileNotFoundError as e:
            result["message"] = str(f"Excpetion: {e}")

        return result

    def set_data(self, reg_hive, reg_path, profile_name):
        """
        Setter

        Params:
            reg_hive (str): Registry hive
            reg_path (list): Registry path to directory
            profile_name (str): Selected restore profile
        """
        self.__reg_hive = reg_hive
        self.__reg_path = reg_path
        self.__profile_name = profile_name
