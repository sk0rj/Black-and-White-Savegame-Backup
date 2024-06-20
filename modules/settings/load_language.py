"""
Reads system language and loads language file.
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
import winreg


class LoadLanguage():
    """
    Class for reading the system language
    and setting the program language.
    """

    def __init__(self):
        self.__lang_file = None
        self.__sys_lang = None

    def system_language(self):
        """
        Reads out the system language.
        """
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                r'Control Panel\International') as key:
                lang = winreg.QueryValueEx(key, 'LocaleName')[0]

            self.__sys_lang = lang

        except FileNotFoundError:
            self.__sys_lang = None

    def load_lang_file(self):
        """
        Attempts to load the language file.

        If successful, the language file will be stored in 'self.__lang_file'.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        try:
            # Read system language
            self.system_language()

            # Determine file path based on system language
            if self.__sys_lang == "de-DE":
                file_path = '../../data/lang_de.json'
            else:
                file_path = '../../data/lang_en.json'

            # Construct full file path
            lang_file_path = os.path.join(
                os.path.dirname(__file__), file_path)

            # Load the language file
            with open(lang_file_path, encoding="UTF-8") as json_file:
                self.__lang_file = json.load(json_file)

            result["success"] = True

        except (FileNotFoundError, json.JSONDecodeError) as e:
            result["message"] = str(e)

        return result

    def get_lang_file(self):
        """
        Getter

        Returns:
            dict: Loaded language file as a dictionary.
        """
        return self.__lang_file
