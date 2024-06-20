"""
Checks if the data of the profile to be recovered already
exists and, if so, offers the option to overwrite it
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
import winreg


class ProfileExistsCheck():
    """
    Class to check if profile data already exists
    """

    def __init__(self):
        self.__data_files = None
        self.__restore_data = None

    def exists_check(self):
        """
        Verifies whether profile data already exists
        before these are accidentally overwritten

        Returns a dictionary with 'success" true/false, a message on error
        and and the choice whether the files should be overwritten or not.
        """
        result = {
            "success": False,
            "overwrite": False
        }

        # Steps to be completed
        steps = [
            self.__check_reg,
            self.__check_profile_dir,
            self.__check_mind_file,
            self.__check_physique_file
        ]

        # Set any_step_failed to False
        files_exist = False

        # If any step returns False (profile data exists),
        # set files_exist to True.
        for step_method in steps:
            step_result = step_method()
            if step_result["success"]:
                files_exist = True

        # If no data exists, return it.
        # if data exists, let the user decide whether it should be overwritten
        if not files_exist:
            print(self.__data_files.lang["profile_exists_check"][0])
            result["success"] = True
        else:
            while True:
                user_query = input(
                    self.__data_files.lang["profile_exists_check"][1]
                ).strip().lower()
                if user_query == "y":
                    print(
                        self.__data_files.lang["profile_exists_check"][2]
                    )
                    result["success"] = True
                    result["overwrite"] = True
                    break
                elif user_query == "n":
                    print(
                        self.__data_files.lang["profile_exists_check"][3]
                    )
                    return result
                else:
                    continue

        return result

    def __check_reg(self):
        """
        Attempts to check if a profile with this name exists in
        the Windows registry.

        Returns a dictionary with 'success" true/false.
        """
        result = {
            "success": False
        }

        try:
            # Sets registry path and opens registry key
            reg_hive = winreg.__dict__[self.__data_files.conf["reg_hive"]]
            reg_subkey = winreg.OpenKeyEx(
                reg_hive,
                self.__data_files.conf["profiles"][0] +
                "\\" +
                self.__restore_data["backup_profile"]
                )

            # Closes the registry key
            winreg.CloseKey(reg_subkey)

            # If a profile with this name exists
            result["success"] = True

        except OSError:
            # If there is no profile with this name
            result["success"] = False

        return result

    def __check_profile_dir(self):
        """
        Attempts to check if a profile directory with this name exists.

        Returns a dictionary with 'success" true/false.
        """
        result = {
            "success": False
        }

        # Set the path to the directory
        dir_path = os.path.join(
            self.__restore_data["game_dir"],
            self.__data_files.conf["profile_dir"],
            self.__restore_data["backup_profile"]
            )

        try:
            # Checks if the directory exists
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                # If a directory with the profile name exists
                result["success"] = True
            else:
                raise FileNotFoundError

        except FileNotFoundError:
            # If there is no directory with the profile name
            result["success"] = False

        return result

    def __check_mind_file(self):
        """
        Attempts to check if a creature mind file
        with this name already exists.

        Returns a dictionary with 'success" true/false.
        """
        result = {
            "success": False
        }

        # Set the path to the file
        file_path = os.path.join(
            self.__restore_data["game_dir"],
            self.__data_files.conf["mind_files"],
            self.__restore_data["creature_mind"]
            )

        try:
            # Checks if the file exists
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # If a file with the name exists
                result["success"] = True
            else:
                raise FileNotFoundError

        except FileNotFoundError:
            # If there is no file with the name
            result["success"] = False

        return result

    def __check_physique_file(self):
        """
        Attempts to check if a creature physique file
        with this name already exists.

        Returns a dictionary with 'success" true/false.
        """
        result = {
            "success": False
        }

        # Set the path to the file
        file_path = os.path.join(
            self.__restore_data["game_dir"],
            self.__data_files.conf["mind_files"],
            self.__restore_data["creature_physique"]
            )

        try:
            # Checks if the file exists
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # If a file with the name exists
                result["success"] = True
            else:
                raise FileNotFoundError

        except FileNotFoundError:
            # If there is no file with the name
            result["success"] = False

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
