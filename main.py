"""
Tool for backing up and restoring black & white savegames.
"""

__version__ = "1.0"

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

from classes.combine_loaded_files import CombineLoadedFiles
from classes.start_backup import StartBackup
from classes.start_restore import StartRestore


class Main():
    """
    Main class to initialize the backup/restore process.
    """

    def __init__(self):
        self.__data_files = None

    def run_program(self):
        """
        Starts the program, loads important data and starts
        the query of what should happen.
        """

        try:
            load_data_result = self.__load_data_files()
            if load_data_result["success"]:
                self.__choose_action()
            else:
                print("Error loading important data.")

        # Error processing of general OS errors
        except OSError as e:
            print(e)

    def __load_data_files(self):
        """
        Initializes CombineLoadedFiles class to load the
        combined configuration and language files.
        """
        load_files = CombineLoadedFiles()
        result = load_files.combine_files()
        if result:
            self.__data_files = load_files.get_files()

        return result

    def __run_backup(self):
        """
        Initializes StartBackup class to start the backup process.
        """
        backup = StartBackup()
        backup.set_data(self.__data_files)
        result = backup.start_backup()
        if result["success"]:
            input(self.__data_files.lang["process_success"][0])
        else:
            input(self.__data_files.lang["process_success"][1])

    def __run_restore(self):
        """
        Initializes StartRestore class to start the restore process.
        """
        restore = StartRestore()
        restore.set_data(self.__data_files)
        result = restore.start_restore()
        if result["success"]:
            input(self.__data_files.lang["process_success"][0])
        else:
            input(self.__data_files.lang["process_success"][1])

    def __choose_action(self):
        """
        Ask the user if they want to create or restore a backup.
        """
        while True:
            choice = input(self.__data_files.lang["choose_action"][0])

            if choice == 'b':
                self.__run_backup()
                break
            elif choice == 'r':
                self.__run_restore()
                break
            else:
                print(self.__data_files.lang["choose_action"][1])


if __name__ == "__main__":
    main = Main()
    main.run_program()
