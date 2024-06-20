"""
Starts the backup process.

- Gathers the information required for the backup (game directory,
  profile to be backed up, creature mind file, registry key, desktop path)

- Performs the backup (creates a temporary directory, copies the required
  files, archives the files in a zip, deletes the temporary directory)
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

from classes.backup.create_backup import CreateBackup
from classes.backup.gather_backup_data import GatherBackupData


class StartBackup():
    """
    Class for running the backup process
    """

    def __init__(self):
        self.__data_files = None
        self.__backup_data = None

    def start_backup(self):
        """
        Starts the backup process.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        # Gathers necessary backup data
        gather_result = self.__gather_data()
        if not gather_result["success"]:
            return result

        # Creates the backup
        backup_result = self.__create_backup()
        if not backup_result["success"]:
            return result

        # when everything has been successfully completed
        result["success"] = True

        return result

    def __gather_data(self):
        """
        Gathers necessary backup data.

        Stores the collected data in 'self.__backup_data'.
        """
        gather_data = GatherBackupData()
        gather_data.set_data(self.__data_files)
        result = gather_data.gather_data()
        if result["success"]:
            self.__backup_data = gather_data.get_backup_data()
            print(result["message"])
        else:
            print(result["message"])
            return result

        return result

    def __create_backup(self):
        """
        Create the backup
        """
        create_backup = CreateBackup()
        create_backup.set_data(self.__data_files, self.__backup_data)
        result = create_backup.create_backup()
        if result["success"]:
            print(result["message"])
        else:
            print(result["message"])
            return result

        return result

    def set_data(self, data_files):
        """
        Setter

        Params:
            data_files (dict): Combined configurations and language data
        """
        self.__data_files = data_files
