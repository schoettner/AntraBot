from util.boss_loader import BossLoader
from util.player import Player
from random import randint


class BattleManager(object):

    def __init__(self, boss_loader: BossLoader):
        self.boss_loader = boss_loader
        self.reward_rate = 0.5
        self.punish_rate = 0.5
        self.lower_border = 0.9  # multiplier on how low your strength can randomize
        self.upper_border = 1.1  # multiplier on how high your strength can randomize

    def fight_random_boss(self, player: Player):
        """
        fight a random boss from the list

        :param player: the player that fights the boss
        :return: the result message of the fight
        """
        boss_id = self.boss_loader.get_random_boss_id()
        return self.fight_boss(player, boss_id)

    def fight_boss(self, player: Player, boss_id: int):
        """
        fight a specific boss in the list

        :param player: the player that fights the boss
        :param boss_id: the result message of the fight
        :return:
        """

        # check if the id is valid?
        _, boss_count = self.boss_loader.get_all_bosses()
        if boss_id < 0 or boss_id >= boss_count:
            return 'The boss id you try to fight is not valid.'
        boss_name, boss_strength = self.boss_loader.get_boss(boss_id)
        strength = player.get_strength()
        actual_strength = randint(int(self.lower_border * strength), int(self.upper_border * strength))
        print("player str: %i, boss str: %i" % (actual_strength, boss_strength))
        if actual_strength > boss_strength:
            self.reward_player(player, boss_strength)
            return '%s was defeated. Glory to %s, the mighty warrior.' % (boss_name, player.profile['name'])
        else:
            self.penalize_player(player, boss_strength)
            return '%s was victorious. %s disappears into the void.' % (boss_name, player.profile['name'])

    def reward_player(self, player: Player, boss_strength: int):
        player.reward_points(int(boss_strength * self.reward_rate))

    def penalize_player(self, player: Player, boss_strength: int):
        player.revoke_points(int(boss_strength * self.punish_rate))
