"""
Creates a Zip archive of the data
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
import zipfile


class ZipBackup():
    """
    Class to create the backup zip file
    """

    def __init__(self):
        self.__backup_exists = None
        self.__backup_profile = None
        self.__desktop_dir = None
        self.__temp_dir = None
        self.__backup_file = None

    def zip_backup(self):
        """
        Attempts to create a Zip archive.

        If successful, the file will be stored in 'self.__backup_file'.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            # Set do_zip to True to perform zipping
            do_zip = True

            # Path to the created zip file
            zip_file = \
                self.__desktop_dir + "\\" + self.__backup_profile + ".zip"

            # Check if the zip file already exists
            if os.path.exists(zip_file):
                while True:
                    # If file already exists let user decide
                    user_query = input(self.__backup_exists[0])
                    # if 'y' overwrite
                    if user_query == "y":
                        print(self.__backup_exists[1])
                        os.remove(zip_file)
                        break
                    # if 'n' abort
                    elif user_query == "n":
                        do_zip = False
                        result["message"] = self.__backup_exists[2]
                        break
                    # Incorrect input
                    else:
                        print(self.__backup_exists[3])

            # If do_zip is True, create the zip file
            if do_zip:
                with zipfile.ZipFile(
                        (zip_file), "w", zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(self.__temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, os.path.relpath(
                                file_path, self.__temp_dir)
                            )

                # Set the path to the created backup file
                self.__backup_file = zip_file

                result["success"] = True

        except FileNotFoundError as e:
            result["message"] = str(f"Excpetion: {e}")

        return result

    def get_backup_file(self):
        """
        Getter

        Returns:
            str: Backup file
        """
        return self.__backup_file

    def set_data(self, backup_exists, backup_profile, desktop_dir, temp_dir):
        """
        Setter

        Paras:
            backup_exists (list): Text in the selected language
            backup_profile (str): Selected backup profile
            desktop_dir (str): Desktop path
            temp_dir (str): Temporary directory path
        """
        self.__backup_exists = backup_exists
        self.__backup_profile = backup_profile
        self.__desktop_dir = desktop_dir
        self.__temp_dir = temp_dir
