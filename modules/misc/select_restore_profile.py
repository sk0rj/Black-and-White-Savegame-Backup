"""
User prompt to select the backup to restore
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


class SelectRestoreProfile():
    """
    Class for selecting backup data
    """

    def __init__(self):
        self.__restore_file = None
        self.__restore_profile = None

    def select_profile(self):
        """
        Attempts to accept the user input.

        If successful, the file will be stored in 'self.__restore_profile'.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            while True:
                # Input for backup data
                restore_profile = input(self.__restore_file[0])

                # Checks if the file exists, and if so,
                # saves it to the self.__restore_profile.
                if os.path.exists(restore_profile):
                    self.__restore_profile = restore_profile
                    result["success"] = True
                    break
                else:
                    print(self.__restore_file[1])

        except FileNotFoundError as e:
            result["message"] = str(f"Excpetion: {e}")

        return result

    def get_restore_profile(self):
        """
        Getter

        Returns:
            str: Path to backup file
        """
        return self.__restore_profile

    def set_data(self, restore_file):
        """
        Setter

        Params:
            restore_file (dict): Text in the selected language
        """
        self.__restore_file = restore_file
