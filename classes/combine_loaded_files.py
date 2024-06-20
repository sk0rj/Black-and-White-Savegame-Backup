"""
Combines loaded language and configuration files
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

from dataclasses import dataclass
from modules.settings.load_config import LoadConfig
from modules.settings.load_language import LoadLanguage


@dataclass
class CombinedData:
    """
    Dataclass to hold combined files.
    """
    conf: dict
    lang: dict


class CombineLoadedFiles():
    """
    Class to combine language and configuration files.
    """

    def __init__(self):
        self.__data_files = None

    def combine_files(self):
        """
        Attempts to combine language and configuration files.

        If successful, they will be stored in a data class 'self.__data_files'.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }
        config_file = None
        lang_file = None

        try:
            # Loads the language file
            lang_loader = LoadLanguage()
            lang_loader_result = lang_loader.load_lang_file()
            if lang_loader_result["success"]:
                lang_file = lang_loader.get_lang_file()
                print(lang_file["language_loaded"])
            else:
                print(
                    f"Failed to load language file: "
                    f"({lang_loader_result['message']})"
                    )
                return result

            # Loads the config file
            config_loader = LoadConfig()
            config_loader_result = config_loader.load_config_file()
            if config_loader_result["success"]:
                config_file = config_loader.get_config_file()
                print(lang_file["load_config"][0])
            else:
                print(
                    f"{lang_file['load_config'][1]} "
                    f"({result['message']})"
                    )
                return result

            # Combine and store files
            self.__data_files = CombinedData(config_file, lang_file)
            result["success"] = True

        except OSError as e:
            result["message"] = str(e)

        return result

    def get_files(self):
        """
        Getter

        Returns:
            dict: Combined configuration and language files
        """
        return self.__data_files
