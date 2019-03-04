import json
from random import randint

from player import Player


class Boss(object):
    """
    allow a twitch chat member to fight hollow knight boss enemies
    """

    def __init__(self, bosses: str = 'config/bosses.json'):
        self.bosses_file = bosses
        self.lower_border = 0.9  # multiplier on how low your strength can randomize
        self.upper_border = 1.1  # multiplier on how high your strength can randomize

    def fight_random_boss(self, player: Player):
        """
        fight a random boss from the list

        :param player: the player that fights the boss
        :return: the result message of the fight
        """
        _, boss_count = self.get_all_bosses()
        max_index = boss_count - 1  # zero based index
        boss_id = randint(0, max_index)
        return self.fight_boss(player, boss_id)

    def fight_boss(self, player: Player, boss_id: int):
        """
        fight a specific boss in the list

        :param player: the player that fights the boss
        :param boss_id: the result message of the fight
        :return:
        """
        boss_name, boss_strength = self.get_boss(boss_id)
        strength = player.get_strength()
        actual_strength = randint(int(self.lower_border * strength), int(self.upper_border * strength))
        print("player str: %i, boss str: %i" % (actual_strength, boss_strength))
        if actual_strength > boss_strength:
            return '%s was defeated. Glory to the mighty warrior. ' % boss_name
        else:
            return '%s was victorious. You disappear into the void.' % boss_name

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

    def get_all_bosses(self):
        """
        get all bosses
        :return: list of bosses, number of bosses available
        """
        with open(self.bosses_file) as f:
            boss_list = json.load(f)
        boss_count = len(boss_list)
        return boss_list, boss_count
