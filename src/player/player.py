import logging

from src.player.player_database import PlayerDatabase
from src.upgrade.upgrade_loader import UpgradeLoader


class Player(object):
    """control the player who is able to battle"""

    def __init__(self, profile: dict, upgrade_loader: UpgradeLoader, player_database: PlayerDatabase):
        self.profile = profile
        self.player_database = player_database
        self.upgrade_loader = upgrade_loader

    def buy_upgrade(self, upgrade_id: int):
        """
        give the player an additional upgrade. check if the player can get the upgrade before

        :param upgrade_id: the id of the upgrade the player wants to buy
        :return: the result message of the purchase as string
        """

        # avoid that people buy start upgrade again
        if upgrade_id == 0:
            return "You can not purchase 'Old Nail' again. You either have it already or upgraded it. " \
                   "Check https://antrabot.fandom.com/wiki/How_to_play for more details."

        # check if the player owns the upgrade already
        if upgrade_id in self.profile['upgrades']:
            return 'You already own this upgrade. You can not purchase it again.'

        # get the upgrade
        upgrade = self.upgrade_loader.get_upgrade(upgrade_id)
        if upgrade is None:
            return 'Upgrade with the id: %i could not be found. ' \
                   'Check https://antrabot.fandom.com/wiki/Upgrades for to find valid Upgrade IDs.' % upgrade_id

        # check if the player has enough cash
        if self.profile['geo'] < upgrade['costs']:
            return 'Seems like you are %i Geo short. Use !stats to check your Geo.' % (upgrade['costs'] - self.profile['geo'])

        # check if the player owns the required item
        if not self.upgrade_loader.meets_requirements(upgrade, self.profile['upgrades']):
            return "You do not meet the requirements to purchase '%s'. " \
                   "You either do not have the required upgrade or you already own a better version." % upgrade['name']

        # time to buy the upgrade
        self.profile['geo'] -= upgrade['costs']  # reduce your geo count
        self.profile['upgrades'].append(upgrade['id'])
        requires_id = upgrade['requires']
        if requires_id is not None:
            self.profile['upgrades'].remove(requires_id)

        # save new upgrades and geo
        self.player_database.set_player_geo(player_name=self.profile['name'], player_geo=self.profile['geo'])
        self.player_database.set_player_upgrades(player_name=self.profile['name'],
                                                 player_upgrades=self.profile['upgrades'])

        message = "Congratulations, you purchased '%s'! Now get into some bosses with your new obtained power!" % \
                  upgrade['name']
        logging.info(message)
        return message

    def get_strength(self):
        """
        get the total strength of a player

        :return: the players base strength and the strength of all the upgrades
        """
        upgrade_strength = 0
        upgrade_list = self.upgrade_loader.get_upgrades_by_ids(self.profile['upgrades'])
        for upgrade in upgrade_list:
            upgrade_strength += upgrade['strength']
        total_strength = self.profile['strength'] + upgrade_strength
        return total_strength

    def add_geo(self, geo: int = 10):
        """
        give the player geo for interaction or time in chat. the amount of geo is added with its current geo

        :param geo: amount of geo you want to add
        """
        self.profile['geo'] += geo
        self.player_database.set_player_geo(player_name=self.profile['name'], player_geo=self.profile['geo'])

    def set_geo(self, geo: int = 10):
        """
        give the player geo for interaction or time in chat

        :param geo: amount of geo you want to set
        """
        self.profile['geo'] = geo
        self.player_database.set_player_geo(player_name=self.profile['name'], player_geo=self.profile['geo'])

    def reward_points(self, points: int = 0):
        """
        increase the number of points for a player

        :param points:
        """
        # also save PB for strongest boss defeated? but the value is already rounded here...
        self.profile['score'] += points
        self.player_database.set_player_score(player_name=self.profile['name'], player_score=self.profile['score'])

        msg = "player %s is rewarded %i points" % (self.profile['name'], self.profile['score'])
        logging.info(msg)

    def revoke_points(self, points: int = 0):
        """
        decrease the number of points for the player. points can not go lower than 0

        :param points:
        :return:
        """
        new_score = max(0, self.profile['score'] - points)  # prevent that the score can go negative
        self.profile['score'] = new_score
        self.player_database.set_player_score(player_name=self.profile['name'], player_score=new_score)

        msg = "player %s loses %i points" % (self.profile['name'], points)
        logging.info(msg)
