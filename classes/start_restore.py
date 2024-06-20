"""
Start the recovery process

- Gathers required data
- Checks if the profile to be recovered already exists
- Restores the selected profile
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

from classes.restore.delete_old_files import DeleteOldFiles
from classes.restore.gather_restore_data import GatherRestoreData
from classes.restore.profile_exists_check import ProfileExistsCheck
from classes.restore.restore_backup import RestoreBackup
from modules.file_operation.create_temp_dir import CreateTempDir
from modules.file_operation.delete_temp_dir import DeleteTempDir


class StartRestore():
    """
    Class for runnign the restore procedure
    """

    def __init__(self):
        self.__data_files = None
        self.__restore_data = None
        self.__temp_dir = None

    def start_restore(self):
        """
        Starts the restore process

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        # Creates the temporary directory
        temp_dir_result = self.__create_temp_dir()
        if not temp_dir_result["success"]:
            return result

        # Gathers necessary restore data
        gather_result = self.__gather_data()
        if not gather_result["success"]:
            self.__delete_temp_dir()
            return result

        # Checks if the profile already exists
        check_exits_result = self.__check_if_data_exists()
        if not check_exits_result["success"]:
            self.__delete_temp_dir()
            return result

        # If the profile already exists and is to be overwritten
        if check_exits_result["overwrite"]:
            # Deletes the profile files
            delete_result = self.__delete_old_files()
            if not delete_result["success"]:
                self.__delete_temp_dir()
                return result

        # Restores the profile
        restore_result = self.__restore_profile()
        if not restore_result["success"]:
            self.__delete_temp_dir()
            return result

        # when everything has been successfully completed
        result["success"] = True
        self.__delete_temp_dir()

        return result

    def __gather_data(self):
        """
        Gathers necessary restore data.

        Stores the collected data in 'self.__restore_data'.
        """
        gather_data = GatherRestoreData()
        gather_data.set_data(self.__data_files, self.__temp_dir)
        result = gather_data.gather_data()
        if result["success"]:
            self.__restore_data = gather_data.get_restore_data()
            print(result["message"])
        else:
            print(result["message"])
            return result

        return result

    def __check_if_data_exists(self):
        """
        Checks if the profile to be rebuilt already exists.
        """
        exists_check = ProfileExistsCheck()
        exists_check.set_data(self.__data_files, self.__restore_data)
        result = exists_check.exists_check()

        return result

    def __delete_old_files(self):
        """
        Deletes existing profile data
        """
        delete_files = DeleteOldFiles()
        delete_files.set_data(self.__data_files, self.__restore_data)
        result = delete_files.delete_files()
        if result["success"]:
            print(result["message"])
        else:
            print(result["message"])
            return result

        return result

    def __restore_profile(self):
        """
        Restores the selected profile
        """
        restore_backup = RestoreBackup()
        restore_backup.set_data(self.__data_files, self.__restore_data)
        result = restore_backup.restore_backup()
        if result["success"]:
            print(result["message"])
        else:
            print(result["message"])
            return result

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

    def set_data(self, data_files):
        """
        Setter

        Params:
            data_files (dict): Combined configurations and language data
        """
        self.__data_files = data_files
