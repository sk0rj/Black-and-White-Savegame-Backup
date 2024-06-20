"""
Creates the temporary directory.
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


class CreateTempDir():
    """
    Class to create the temporary directory.
    """

    def __init__(self):
        self.__dir_name = None
        self.__lang_str = None
        self.__temp_dir = None

    def create_temp_dir(self):
        """
        Attempts to create the temporary directory.

        If successful, the path will be stored in 'self.__temp_dir'.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            # Gets the appdata\local directory path from environment variables
            bw_temp = os.getenv("tmp")

            # Checks if the temporary directory path is None
            if bw_temp is None:
                result["message"] = self.__lang_str

                return result

            # Combines the temporary directory path
            # with the specified directory name
            bw_temp = os.path.join(bw_temp, self.__dir_name)

            # Checks if the temporary directory already
            # exists and removes it if it does
            if os.path.exists(bw_temp):
                shutil.rmtree(bw_temp)

            # Creates the temporary directory
            os.makedirs(bw_temp, exist_ok=True)

            # Sets the temporary directory path to the instance variable
            self.__temp_dir = bw_temp
            result["success"] = True

        except FileNotFoundError as e:
            result["message"] = str(f"Excpetion: {e}")

        return result

    def get_temp_dir(self):
        """
        Getter

        Returns:
            str: Path to temporary directory
        """
        return self.__temp_dir

    def set_data(self, dir_name, lang_str):
        """
        Setter

        Params:
            dir_name (str): Name for the temporary directory
            lang_str (str): Text in the selected language
        """
        self.__dir_name = dir_name
        self.__lang_str = lang_str
