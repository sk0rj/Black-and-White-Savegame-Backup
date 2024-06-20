"""
Gathers the necessary backup data:
- Game directory
- Desktop directory
- Backup profile
- Creature mind file
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

from modules.misc.select_backup_profile import SelectBackupProfile
from modules.registry_operation.locate_dir import LocateDir
from modules.registry_operation.locate_mind_file import LocateMindFile
from modules.registry_operation.read_profiles import ReadProfiles


class GatherBackupData():
    """
    Class for the collection of the necessary backup data
    """

    def __init__(self):
        self.__data_files = None
        self.__game_dir = None
        self.__desktop_dir = None
        self.__profile_list = None
        self.__backup_profile = None
        self.__creature_mind = None
        self.__backup_data = None

    def gather_data(self):
        """
        Gathers the required data.

        Returns a dictionary with 'success" true/false and a message on error.
        """
        result = {
            "success": False,
            "message": None
        }

        # Steps to be completed
        steps = [
            self.__locate_game_dir,
            self.__locate_desktop_dir,
            self.__read_profiles,
            self.__select_backup_profile,
            self.__locate_creature_mind
        ]

        # Check each step for success, return failure message if any step fails
        for step_method in steps:
            step_result = step_method()
            if not step_result["success"]:
                result["message"] = \
                    self.__data_files.lang["gather_backup_data"][1]

                return result

        # If all steps succeeded, collect and return backup data
        self.__backup_data = {
            "game_dir": self.__game_dir,
            "desktop_dir": self.__desktop_dir,
            "backup_profile": self.__backup_profile,
            "creature_mind": self.__creature_mind,
            "creature_physique": (
                self.__data_files.conf["physique_file"] +
                self.__creature_mind
                )
        }

        # when everything has been successfully completed
        result["success"] = True
        result["message"] = self.__data_files.lang["gather_backup_data"][0]

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

    def __locate_desktop_dir(self):
        """
        Locates the desktop directory.

        Stores the path in 'self.__desktop_dir'.
        """
        desktop_dir = LocateDir()
        desktop_dir.set_data(
            self.__data_files.conf["reg_hive"],
            self.__data_files.conf["desktop_dir"])
        result = desktop_dir.locate_dir()
        if result["success"]:
            self.__desktop_dir = desktop_dir.get_dir()
            print(
                self.__data_files.lang['desktop_dir'][0],
                self.__desktop_dir
            )
        else:
            print(
                f"{self.__data_files.lang['desktop_dir'][1]} "
                f"({result['message']})"
            )

        return result

    def __read_profiles(self):
        """
        Lists available profiles.

        Stores the list in 'self.__profile_list'.
        """
        profile_list = ReadProfiles()
        profile_list.set_data(
            self.__data_files.conf["reg_hive"],
            self.__data_files.conf["profiles"],
            self.__data_files.lang["profile_list"][2]
        )
        result = profile_list.read_profiles()
        if result["success"]:
            self.__profile_list = profile_list.get_profile_list()
            print(
                self.__data_files.lang["profile_list"][0],
                self.__profile_list
            )
        else:
            print(
                f"{self.__data_files.lang['profile_list'][1]} "
                f"({result['message']})"
            )

        return result

    def __select_backup_profile(self):
        """
        Allows the user to select a backup profile.

        Stores the selected profile in 'self.__backup_profile'.
        """
        backup_profile = SelectBackupProfile()
        backup_profile.set_data(
            self.__data_files.lang["select_profile"],
            self.__profile_list
        )
        result = backup_profile.select_profile()
        if result["success"]:
            self.__backup_profile = backup_profile.get_backup_profile()
            print(
                self.__data_files.lang["select_profile"][3],
                self.__backup_profile
            )
        else:
            print(self.__data_files.lang["select_profile"][4])

        return result

    def __locate_creature_mind(self):
        """
        Locate the creature mind file.

        Stores the file in 'self.__creature_mind'.
        """
        creature_mind = LocateMindFile()
        creature_mind.set_data(
            self.__data_files.conf["reg_hive"],
            self.__data_files.conf["profiles"],
            self.__backup_profile
        )
        result = creature_mind.locate_file()
        if result["success"]:
            self.__creature_mind = creature_mind.get_mind_file()
            print(
                self.__data_files.lang["mind_file"][0],
                self.__creature_mind
            )
            print(
                self.__data_files.lang["physique_file"],
                self.__data_files.conf["physique_file"] + self.__creature_mind
            )
        else:
            print(
                f"{self.__data_files.lang['mind_file'][1]} "
                f"({result['message']})"
            )

        return result

    def get_backup_data(self):
        """
        Getter

        Returns:
            dict: Necessary backup data
        """
        return self.__backup_data

    def set_data(self, data_files):
        """
        Setter

        Params:
            data_files (dict): Combined configurations and language data
        """
        self.__data_files = data_files
