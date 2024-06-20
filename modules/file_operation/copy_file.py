"""
Copy a specific file
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


class CopyFile():
    """
    Class to copy a specific file
    """

    def __init__(self):
        self.__src_file = None
        self.__dst_file = None

    def copy_file(self):
        """
        Attempts to copy a file.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            # Copy from source to destination
            shutil.copy2(self.__src_file, self.__dst_file)

            result["success"] = True

        except FileNotFoundError as e:
            result["message"] = str(f"Excpetion: {e}")

        return result

    def set_data(self, src_file, dst_file):
        """
        Setter

        Params:
            src_file (str): Source directory
            dst_file (str): Destination directory
        """
        self.__src_file = src_file
        self.__dst_file = dst_file
