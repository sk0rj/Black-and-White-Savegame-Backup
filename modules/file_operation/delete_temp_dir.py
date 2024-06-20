"""
Delete the temporary directory
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

import shutil


class DeleteTempDir():
    """
    Class to delete the temporary directory
    """

    def __init__(self):
        self.__temp_dir = None

    def delete_temp_dir(self):
        """
        Attempts to delete the temporary directory.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            # Deletes temporary directory
            shutil.rmtree(self.__temp_dir)
            result["success"] = True

        except FileNotFoundError as e:
            result["message"] = str(f"Excpetion: {e}")

        return result

    def set_data(self, temp_dir):
        """
        Setter

        Params:
            temp_dir (str): Temporary directory path
        """
        self.__temp_dir = temp_dir
