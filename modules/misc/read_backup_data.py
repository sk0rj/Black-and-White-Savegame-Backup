"""
Reads backup restore information from backup_info.json
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

import json
import os


class ReadBackupData():
    """
    Class to read backup data
    """
    def __init__(self):
        self.__temp_dir = None
        self.__backup_data = None

    def read_data(self):
        """
        Attempts to read backup data.

        If successful, the file will be stored in 'self.__backup_data'.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            # Construct the path to the backup info JSON file
            info_file_path = os.path.join(
                os.path.dirname(__file__),
                self.__temp_dir,
                'backup_info.json'
                )

            # Open and read the JSON file
            # then load its contents into self.__backup_data
            with open(info_file_path, encoding="UTF-8") as json_file:
                self.__backup_data = json.load(json_file)

            result["success"] = True

        except FileNotFoundError as e:
            result["message"] = str(f"Excpetion: {e}")

        return result

    def get_backup_data(self):
        """
        Getter

        Returns:
            dict: Backup data
        """
        return self.__backup_data

    def set_data(self, temp_dir):
        """
        Setter

        Params:
            temp_dir (str): Temporary directory path
        """
        self.__temp_dir = temp_dir
