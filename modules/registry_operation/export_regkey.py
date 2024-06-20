"""
Export a custom registration key using a sub-process
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


class ExportRegkey():
    """
    Class for exporting registration keys.
    """

    def __init__(self):
        self.__reg_hive = None
        self.__reg_path = None
        self.__reg_file = None
        self.__backup_profile = None
        self.__temp_dir = None

    def export_regkey(self):
        """
        Attempts to export a registry key.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            # Constructs the full registry path
            reg_path = (
                self.__reg_hive +
                "\\" + self.__reg_path[0] +
                self.__reg_path[1]
                )
            regkey = reg_path + "\\" + self.__backup_profile
            export_file = self.__temp_dir + "\\" + self.__reg_file

            # Exports the registry key to a file using the 'reg' command
            subprocess.run(
                ["reg", "export", regkey, export_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
                )

            result["success"] = True

        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            result["message"] = str(f"Excpetion: {e}")

        return result

    def set_data(self, reg_hive, reg_path, reg_file, backup_profile, temp_dir):
        """
        Setter

        Params:
            reg_hive (str): Registry hive
            reg_path (str): Registry path to directory
            reg_file (str): Name of the file to be created
            backup_profile (str): Selected backup profile
            temp_dir (str): Temporary directory path
        """
        self.__reg_hive = reg_hive
        self.__reg_path = reg_path
        self.__reg_file = reg_file
        self.__backup_profile = backup_profile
        self.__temp_dir = temp_dir
