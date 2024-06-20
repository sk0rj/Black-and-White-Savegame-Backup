"""
Gathers the necessary files for recovery
- Selected backup
- Temporary directory
- Restore data (profilename, creature mind file)
- Game diretory
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

from modules.misc.read_backup_data import ReadBackupData
from modules.misc.select_restore_profile import SelectRestoreProfile
from modules.registry_operation.locate_dir import LocateDir
from modules.zip_operation.unzip_files import UnzipBackup


class GatherRestoreData():
    """
    Class to gather the necessary information
    """

    def __init__(self):
        self.__data_files = None
        self.__backup_file = None
        self.__temp_dir = None
        self.__backup_data = None
        self.__restore_data = None
        self.__game_dir = None

    def gather_data(self):
        """
        Gathers data required for restore

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        # Steps to be completed
        steps = [
            self.__select_backup,
            self.__unzip_backup,
            self.__read_backup_data,
            self.__locate_game_dir,
            self.__combine_data
        ]

        # Check each step for success, return failure message
        # if any step fails
        for step_method in steps:
            step_result = step_method()
            if not step_result["success"]:
                result["message"] = \
                    self.__data_files.lang["gather_restore_data"][1]

                return result

        # when everything has been successfully completed
        result["success"] = True
        result["message"] = self.__data_files.lang["gather_restore_data"][0]

        return result

    def __select_backup(self):
        """
        User selects the profile to be restored.

        Stores the profile in 'self.__backup_file'.
        """
        restore_backup = SelectRestoreProfile()
        restore_backup.set_data(self.__data_files.lang["restore_file"])
        result = restore_backup.select_profile()
        if result["success"]:
            self.__backup_file = restore_backup.get_restore_profile()
            print(
                self.__data_files.lang["restore_file"][2],
                self.__backup_file
            )
        else:
            print(
                f"{self.__data_files.lang['restore_file'][3]} "
                f"({result['message']})"
            )

        return result

    def __unzip_backup(self):
        """
        Unpack the backup archive.
        """
        unzip_backup = UnzipBackup()
        unzip_backup.set_data(self.__backup_file, self.__temp_dir)
        result = unzip_backup.unzip_backup()
        if result["success"]:
            print(self.__data_files.lang["unzip_backup"][0])
        else:
            print(
                f"{self.__data_files.lang['unzip_backup'][1]} "
                f"({result['message']})"
            )

        return result

    def __read_backup_data(self):
        """
        Read neccessary data from backup_info.json

        Stores the data in 'self.__backup_data'
        """
        read_data = ReadBackupData()
        read_data.set_data(self.__temp_dir)
        result = read_data.read_data()
        if result["success"]:
            self.__backup_data = read_data.get_backup_data()
            print(self.__data_files.lang["read_data"][0])
        else:
            print(
                f"{self.__data_files.lang['read_data'][1]}"
                f"({result['message']})"
            )

        return result

    def __locate_game_dir(self):
        """
        Locates the game directory.

        Stores the path in 'self.__game_dir'.
        """
        game_dir = LocateDir()
        game_dir.set_data(
            self.__data_files.conf["reg_hive"],
            self.__data_files.conf["game_dir"])
        result = game_dir.locate_dir()
        if result["success"]:
            self.__game_dir = game_dir.get_dir()
            print(
                self.__data_files.lang["game_dir"][0],
                self.__game_dir
            )
        else:
            print(
                f"{self.__data_files.lang['game_dir'][1]} "
                f"({result['message']})"
            )

        return result

    def __combine_data(self):
        """
        Takes the backup data from 'self.__backup_data' and
        saves it along with the desktop and temporary
        directory to 'self.__restore_data'.
        """
        result = {
            "success": False
        }

        self.__restore_data = self.__backup_data

        self.__restore_data.update({
            "game_dir": self.__game_dir,
            "temp_dir": self.__temp_dir
        })

        if len(self.__restore_data) == 5:
            result["success"] = True

        return result

    def get_restore_data(self):
        """
        Getter

        Returns:
            dict: Neccessary restore data
        """
        return self.__restore_data

    def set_data(self, data_files, temp_dir):
        """
        Setter

        Params:
            data_files (dict): Combined configurations and language data
            temp_dir (str): Temporary directory path
        """
        self.__data_files = data_files
        self.__temp_dir = temp_dir
