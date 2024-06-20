"""
Restores the previously selected backup.
- Copy profile directory and creature mind file to game directory
- Imports the registration key
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
from modules.file_operation.copy_dir import CopyDir
from modules.file_operation.copy_file import CopyFile
from modules.registry_operation.import_regkey import ImportRegkey
from modules.registry_operation.write_last_profile import WriteLastProfile


class RestoreBackup():
    """
    Class to restore the backup
    """

    def __init__(self):
        self.__data_files = None
        self.__restore_data = None

    def restore_backup(self):
        """
        Restores the backup

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        # Steps to be completed
        steps = [
            self.__copy_profile_dir,
            self.__copy_mind_file,
            self.__copy_physique_file,
            self.__write_last_profile,
            self.__import_reg_key
        ]

        # Check each step for success, return failure message if any step fails
        for step_method in steps:
            step_result = step_method()
            if not step_result["success"]:
                result["message"] = \
                    self.__data_files.lang["restore_backup"][1]

                return result

        # when everything has been successfully completed
        result["success"] = True
        result["message"] = self.__data_files.lang["restore_backup"][0]

        return result

    def __copy_profile_dir(self):
        """
        Copy the profile directory from the
        temporary directory to the game directory.

        Returns:
            dict: The result of the copy operation,
            including success status and message.
        """
        # Set the source directory
        src_dir = os.path.join(
            self.__restore_data["temp_dir"],
            self.__restore_data["backup_profile"]
        )

        # Set the destination directory
        dst_dir = os.path.join(
            self.__restore_data["game_dir"],
            self.__data_files.conf["profile_dir"],
            self.__restore_data["backup_profile"]
        )

        profile_dir = CopyDir()
        profile_dir.set_data(src_dir, dst_dir)
        result = profile_dir.copy_dir()
        if result["success"]:
            print(self.__data_files.lang["copy_profile"][0])
        else:
            print(
                f"{self.__data_files.lang['copy_profile'][1]} "
                f"({result['message']})"
            )

        return result

    def __copy_mind_file(self):
        """
        Copy the creature mind file from the
        temporary directory to the game directory.

        Returns:
            dict: The result of the copy operation,
                  including success status and message.
        """
        # Set the source
        src_file = os.path.join(
            self.__restore_data["temp_dir"],
            self.__restore_data["creature_mind"]
        )

        # Set the destination
        dst_file = os.path.join(
            self.__restore_data["game_dir"],
            self.__data_files.conf["mind_files"]
        )

        mind_file = CopyFile()
        mind_file.set_data(src_file, dst_file)
        result = mind_file.copy_file()
        if result["success"]:
            print(self.__data_files.lang["copy_mind"][0])
        else:
            print(
                f"{self.__data_files.lang['copy_mind'][1]} "
                f"({result['message']})"
            )

        return result

    def __copy_physique_file(self):
        """
        Copy the creature physique file from the
        temporary directory to the game directory.

        Returns:
            dict: The result of the copy operation,
                  including success status and message.
        """
        # Set the source
        src_file = os.path.join(
            self.__restore_data["temp_dir"],
            self.__restore_data["creature_physique"]
        )

        # Set the destination
        dst_file = os.path.join(
            self.__restore_data["game_dir"],
            self.__data_files.conf["mind_files"]
        )

        mind_file = CopyFile()
        mind_file.set_data(src_file, dst_file)
        result = mind_file.copy_file()
        if result["success"]:
            print(self.__data_files.lang["copy_physique"][0])
        else:
            print(
                f"{self.__data_files.lang['copy_physique'][1]} "
                f"({result['message']})"
            )

        return result

    def __import_reg_key(self):
        """
        Imports the registration key.

        Returns:
            dict: The result of the import operation,
                  including success status and message.
        """
        key_import = ImportRegkey()
        key_import.set_data(
            self.__restore_data["temp_dir"],
            self.__data_files.conf["reg_file"]
            )
        result = key_import.import_regkey()
        if result["success"]:
            print(self.__data_files.lang["import_reg_key"][0])
        else:
            print(
                f"{self.__data_files.lang['import_reg_key'][1]}"
                f"({result['message']})"
            )

        return result

    def __write_last_profile(self):
        """
        Writes the last used profile name to the registry

        Returns:
            dict: The result of the import operation,
                  including success status and message.
        """
        write_profile = WriteLastProfile()
        write_profile.set_data(
            self.__data_files.conf["reg_hive"],
            self.__data_files.conf["profiles"],
            self.__restore_data["backup_profile"]
            )
        result = write_profile.write_profile_name()
        if result["success"]:
            print(self.__data_files.lang["write_last_profile"][0])
        else:
            print(
                f"{self.__data_files.lang['write_last_profile'][1]}"
                f"({result['message']})"
            )

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
