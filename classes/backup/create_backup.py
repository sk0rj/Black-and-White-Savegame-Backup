"""
Perform the backup.

Creates a temporary directory, copies important files,
and then archives them in a ZIP file.
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
from modules.file_operation.create_temp_dir import CreateTempDir
from modules.file_operation.delete_temp_dir import DeleteTempDir
from modules.misc.write_backup_data import WriteBackupData
from modules.registry_operation.export_regkey import ExportRegkey
from modules.zip_operation.zip_backup import ZipBackup


class CreateBackup():
    """
    Class for creating backups
    """

    def __init__(self):
        self.__data_files = None
        self.__backup_data = None
        self.__temp_dir = None
        self.__backup_file = None

    def create_backup(self):
        """
        Performs the backup steps.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        # Steps to be completed
        steps = [
            self.__create_temp_dir,
            self.__copy_profile_dir,
            self.__copy_mind_file,
            self.__copy_physique_file,
            self.__export_reg_key,
            self.__write_backup_data,
            self.__zip_backup,
            self.__delete_temp_dir
        ]

        # Check each step for success, return failure message
        # if any step fails and delete the temp directory
        for step_method in steps:
            step_result = step_method()
            if not step_result["success"]:
                result["message"] = \
                    self.__data_files.lang["create_backup"][1]
                self.__delete_temp_dir()

                return result

        # when everything has been successfully completed
        result["success"] = True
        result["message"] = self.__data_files.lang["create_backup"][0]

        return result

    def __create_temp_dir(self):
        """
        Creates a temporary directory.

        Stores the path in 'self.__temp_dir'.
        """
        create_dir = CreateTempDir()
        create_dir.set_data(
            self.__data_files.conf["temp"],
            self.__data_files.lang["create_temp"][2]
            )
        result = create_dir.create_temp_dir()
        if result["success"]:
            self.__temp_dir = create_dir.get_temp_dir()
            print(
                self.__data_files.lang["create_temp"][0],
                self.__temp_dir
            )
        else:
            print(
                f"{self.__data_files.lang['create_temp'][1]} "
                f"({result['message']})"
            )

        return result

    def __copy_profile_dir(self):
        """
        Copies the profile directory
        """
        src_dir = os.path.join(
            self.__backup_data["game_dir"],
            self.__data_files.conf["profile_dir"],
            self.__backup_data["backup_profile"]
        )

        dst_dir = os.path.join(
            self.__temp_dir,
            self.__backup_data["backup_profile"]
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
        Copies the creature mind file
        """
        src_file = os.path.join(
            self.__backup_data["game_dir"],
            self.__data_files.conf["mind_files"],
            self.__backup_data["creature_mind"]
        )

        mind_file = CopyFile()
        mind_file.set_data(src_file, self.__temp_dir)
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
        Copies the creature physique file
        """
        src_file = os.path.join(
            self.__backup_data["game_dir"],
            self.__data_files.conf["mind_files"],
            self.__backup_data["creature_physique"]
        )

        physique_file = CopyFile()
        physique_file.set_data(src_file, self.__temp_dir)
        result = physique_file.copy_file()
        if result["success"]:
            print(self.__data_files.lang["copy_physique"][0])
        else:
            print(
                f"{self.__data_files.lang['copy_physique'][1]} "
                f"({result['message']})"
            )

        return result

    def __export_reg_key(self):
        """
        Exports the registry key
        """
        key_export = ExportRegkey()
        key_export.set_data(
            self.__data_files.conf["reg_hive"],
            self.__data_files.conf["profiles"],
            self.__data_files.conf["reg_file"],
            self.__backup_data["backup_profile"],
            self.__temp_dir
            )
        result = key_export.export_regkey()
        if result["success"]:
            print(self.__data_files.lang["export_reg_key"][0])
        else:
            print(
                f"{self.__data_files.lang['export_reg_key'][1]} "
                f"({result['message']})"
            )

        return result

    def __write_backup_data(self):
        """
        Writes backup information,
        including selected profile and Creature Mind file.

        Stores it in the temporary directory in backup_info.json
        """
        write_data = WriteBackupData()
        write_data.set_data(
            self.__backup_data,
            self.__data_files.conf["backup_info"],
            self.__temp_dir
            )
        result = write_data.write_data()
        if result["success"]:
            print(self.__data_files.lang["backup_info"][0])
        else:
            print(
                f"{self.__data_files.lang['backup_info'][1]} "
                f"({result['message']})"
            )

        return result

    def __zip_backup(self):
        """
        Create a Zip archive of files.

        Stores the created zip file in 'self.__backup_file'.
        """
        zip_backup = ZipBackup()
        zip_backup.set_data(
            self.__data_files.lang["backup_exists"],
            self.__backup_data["backup_profile"],
            self.__backup_data["desktop_dir"],
            self.__temp_dir
        )
        result = zip_backup.zip_backup()
        if result["success"]:
            self.__backup_file = zip_backup.get_backup_file()
            print(self.__data_files.lang["backup_file"][0],
                  self.__backup_file)
        else:
            print(
                f"{self.__data_files.lang['backup_file'][1]} "
                f"({result['message']})"
            )

        return result

    def __delete_temp_dir(self):
        """
        Delete the temporary directory
        """
        delete_dir = DeleteTempDir()
        delete_dir.set_data(self.__temp_dir)
        result = delete_dir.delete_temp_dir()
        if result["success"]:
            print(self.__data_files.lang["del_temp"][0],
                  self.__temp_dir)
        else:
            print(
                f"{self.__data_files.lang['del_temp'][1]} "
                f"({result['message']})"
            )

        return result

    def set_data(self, data_files, backup_data):
        """
        Setter

        Params:
            data_files (dict): Combined configurations and language data
            backup_data (dict): Necessary backup data
        """
        self.__data_files = data_files
        self.__backup_data = backup_data
