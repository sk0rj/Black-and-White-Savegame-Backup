"""
Loads the configuration files.
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

import json
import os


class LoadConfig():
    """
    Class to load the configuration file.
    """

    def __init__(self):
        self.__config_file = None

    def load_config_file(self):
        """
        Attempts to load the configuration file.

        If successful, the configuration file will be
        stored in 'self.__config_file'.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            # Set file path for configuration file
            config_file_path = os.path.join(
                os.path.dirname(__file__), '../../data/config.json')

            # Load the configuration file
            with open(config_file_path, encoding="UTF-8") as json_file:
                self.__config_file = json.load(json_file)

            result["success"] = True

        except (FileNotFoundError, json.JSONDecodeError) as e:
            result["message"] = str(e)

        return result

    def get_config_file(self):
        """
        Getter

        Returns:
            dict: Loaded configuration file as a dictionary.
        """
        return self.__config_file
