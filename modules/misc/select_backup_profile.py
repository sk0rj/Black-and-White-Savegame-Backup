"""
User prompt for backup profile selection
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


class SelectBackupProfile():
    """
    Class to select a profile for backup
    """

    def __init__(self):
        self.__lang_str = None
        self.__profile_list = None
        self.__backup_profile = None

    def select_profile(self):
        """
        Allows the user to select a profile for backup.

        Selected profile will be stored in 'self.__backup_profile.

        Returns a dictionary with 'success" true/false.
        """
        result = {
            "success": False,
        }

        # Initialize the profile list with numbers
        indexed_profiles = {
            i + 1: profile_name for i,
            profile_name in enumerate(self.__profile_list)
            }

        # Loop iterates until user makes a valid profile selection
        while True:
            print(self.__lang_str[0])
            for num, profile_name in indexed_profiles.items():
                print(f"({num}) \"{profile_name}\"")

            choice = input(self.__lang_str[1])

            if choice.isdigit() and int(choice) in indexed_profiles:
                self.__backup_profile = indexed_profiles[int(choice)]
                result["success"] = True
                break
            else:
                print(self.__lang_str[2])

        return result

    def get_backup_profile(self):
        """
        Getter

        Returns:
            str: Selected profile
        """
        return self.__backup_profile

    def set_data(self, lang_str, profile_list):
        """
        Setter

        Params:
            lang_str (str): Text in the selected language
            profile_list (list): Available profiles
        """
        self.__lang_str = lang_str
        self.__profile_list = profile_list
