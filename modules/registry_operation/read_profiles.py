"""
Reads the available game profiles from the Windows registry.
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


class ReadProfiles():
    """ Class for reading out the available profiles """

    def __init__(self):
        self.__reg_hive = None
        self.__reg_path = None
        self.__lang_str = None
        self.__profile_list = None

    def read_profiles(self):
        """
        Attempts to list the profiles.

        If successful, the profile(s) will be stored in 'self.__profile_list'.

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
                reg_hive, self.__reg_path[0] + self.__reg_path[1])

            index = 0
            profiles = []

            # Loop iterates until all profiles are added to the profile list
            while True:
                try:
                    key_name = winreg.EnumKey(reg_subkey, index)
                    profiles.append(key_name)
                    index += 1

                except OSError:
                    break

            # Closes the registry key
            winreg.CloseKey(reg_subkey)

            # If no profiles were found
            if not profiles:
                result["success"] = False
                result["message"] = self.__lang_str

                return result

            # If profiles are found
            self.__profile_list = profiles
            result["success"] = True

        except (FileNotFoundError, PermissionError) as e:
            result["message"] = str(f"Excpetion: {e}")

        return result

    def get_profile_list(self):
        """
        Getter

        Returns:
            dict: List of available profiles
        """
        return self.__profile_list

    def set_data(self, reg_hive, reg_path, lang_str):
        """
        Setter

        Params:
            reg_hive (str): Registry hive
            reg_path (dict): Registry path to directory
            lang_str (str): Text in the selected language
        """
        self.__reg_hive = reg_hive
        self.__reg_path = reg_path
        self.__lang_str = lang_str
