import json
from random import randint


class BossLoader(object):
    """
    allow a twitch chat member to fight hollow knight boss enemies
    """

    def __init__(self, bosses: str = 'config/bosses.json'):
        self.bosses_file = bosses

    def get_boss(self, boss_id: int = 0):
        """
        load a boss from the provided json file

        :param boss_id: the id of the boss you want
        :return: the name of the boss as str, the strength of the boss as int
        """
        boss_list, boss_count = self.get_all_bosses()

        # check if the id is in a valid range
        if boss_id >= boss_count:
            return 'no boss', 0

        boss = boss_list[boss_id]
        boss_name = boss['name']
        boss_strength = boss['strength']
        return boss_name, boss_strength

    def get_random_boss_id(self):
        """
        get the id of a random boss. can be used to fight a random boss

        :return: a valid id (int) of an existing boss
        """
        _, boss_count = self.get_all_bosses()
        max_index = boss_count - 1  # zero based index
        boss_id = randint(0, max_index)
        return boss_id

    def get_all_bosses(self):
        """
        get all bosses

        :return: list of bosses (dict), number of bosses available (int)
        """
        with open(self.bosses_file) as f:
            boss_list = json.load(f)
        boss_count = len(boss_list)
        return boss_list, boss_count
