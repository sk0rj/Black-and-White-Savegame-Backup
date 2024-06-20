"""
Deletes existing profile data when overwrite is selected by the user.
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
import shutil
import winreg


class DeleteOldFiles():
    """
    Class to delete profile data
    """

    def __init__(self):
        self.__data_files = None
        self.__restore_data = None

    def delete_files(self):
        """
        Delete existing profile data

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        # Steps to be completed
        steps = [
            self.__delete_reg,
            self.__delete_profile_dir,
            self.__delete_mind_file,
            self.__delete_physique_file
        ]

        # Check each step for success, return failure message
        for step_method in steps:
            step_result = step_method()
            if not step_result["success"]:
                result["message"] = \
                    self.__data_files.lang["delete_old_files"][1]

                return result

        # when everything has been successfully completed
        result["success"] = True
        result["message"] = self.__data_files.lang["delete_old_files"][0]

        return result

    def __delete_reg(self):
        """
        Attempts to delete the profile's registration key.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            # Sets registry path
            reg_hive = winreg.__dict__[self.__data_files.conf["reg_hive"]]
            reg_subkey = self.__data_files.conf["profiles"][0] + \
                "\\" + self.__restore_data["backup_profile"]

            # Deletes the registry key
            winreg.DeleteKey(reg_hive, reg_subkey)

            result["success"] = True

        except FileNotFoundError:
            result["success"] = True

        return result

    def __delete_profile_dir(self):
        """
        Attempts to delete the profile directory.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        # Set the path to the directory
        dir_path = os.path.join(
            self.__restore_data["game_dir"],
            self.__data_files.conf["profile_dir"],
            self.__restore_data["backup_profile"]
            )

        try:
            # Checks if the directory exists and if so, deletes it
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                shutil.rmtree(dir_path)
                result["success"] = True
            else:
                result["success"] = True

        except OSError as e:
            result["message"] = str(e)

        return result

    def __delete_mind_file(self):
        """
        Attempts to delete the creature mind file.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        # Set the path to the file
        file_path = os.path.join(
            self.__restore_data["game_dir"],
            self.__data_files.conf["mind_files"],
            self.__restore_data["creature_mind"]
            )

        try:
            # Checks if the file exists and if so, deletes it
            if os.path.exists(file_path) and os.path.isfile(file_path):
                os.remove(file_path)
                result["success"] = True
            else:
                result["success"] = True

        except OSError as e:
            result["message"] = str(e)

        return result

    def __delete_physique_file(self):
        """
        Attempts to delete the creature physique file.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        # Set the path to the file
        file_path = os.path.join(
            self.__restore_data["game_dir"],
            self.__data_files.conf["mind_files"],
            self.__restore_data["creature_physique"]
            )

        try:
            # Checks if the file exists and if so, deletes it
            if os.path.exists(file_path) and os.path.isfile(file_path):
                os.remove(file_path)
                result["success"] = True
            else:
                result["success"] = True

        except OSError as e:
            result["message"] = str(e)

        return result

    def set_data(self, data_files, restore_data):
        """
        Setter

        Params:
            data_files (dict): Combined configurations and language data
            restore_data (dict): Neccessary restore data
        """
        self.__data_files = data_files
        self.__restore_data = restore_data
