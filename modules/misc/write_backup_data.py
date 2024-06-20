"""
Writes important backup information to backup_info.json:
- Selected profile
- Creature Mind file
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


class WriteBackupData():
    """
    Class for writing important backup information
    """

    def __init__(self):
        self.__backup_data = None
        self.__backup_info = None
        self.__temp_dir = None

    def write_data(self):
        """
        Attempts to write the backup data to a JSON file.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            # Prepares backup information dictionary
            backup_info = {
                "backup_profile": self.__backup_data["backup_profile"],
                "creature_mind": self.__backup_data["creature_mind"],
                "creature_physique": self.__backup_data["creature_physique"]
            }

            # Constructs the path for the backup information file
            backup_info_path = os.path.join(
                self.__temp_dir, self.__backup_info)

            # Writes the backup information to a JSON file
            with open(backup_info_path, "w", encoding="UTF-8") as json_file:
                json.dump(backup_info, json_file)

            result["success"] = True

        except FileNotFoundError as e:
            result["message"] = str(f"Excpetion: {e}")

        return result

    def set_data(self, backup_data, backup_info, temp_dir):
        """
        Setter

        Params:
            backup_data (dict): Backup profile and creature mind file
            backup_info (str): Name of the .json-file
            temp_dir (str): Temporary directory path
        """
        self.__backup_data = backup_data
        self.__backup_info = backup_info
        self.__temp_dir = temp_dir
