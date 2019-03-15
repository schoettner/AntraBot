from database import PlayerDatabase
from upgrade import Upgrade


class Player(object):
    """control the player who is able to battle"""

    def __init__(self, profile: dict, upgrade_loader: Upgrade, player_database: PlayerDatabase):
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
            return 'You can not buy this upgrade. This thing is way to old for an experienced warrior like yourself.'

        # check if the player owns the upgrade already
        if upgrade_id in self.profile['upgrades']:
            return 'You already own this upgrade. You can not purchase it again.'

        # get the upgrade
        upgrade = self.upgrade_loader.get_upgrade(upgrade_id)
        if upgrade is None:
            return 'Upgrade with the id: %i could not be found.' % upgrade_id

        # check if the player has enough cash
        if self.profile['geo'] < upgrade['costs']:
            return 'Seems like you have not enough Geo. Come back when you collected some more.'

        # check if the player owns the required item
        if not self.upgrade_loader.meets_requirements(upgrade, self.profile['upgrades']):
            return 'You do not own the required item to do the upgrade. Or you already own a better version.'

        # time to buy the upgrade
        self.profile['geo'] -= upgrade['costs']  # reduce your geo count
        self.profile['upgrades'].append(upgrade['id'])
        self.profile['upgrades'].remove(upgrade['requires'])

        # save new upgrades and geo
        self.player_database.update_player_geo(player_name=self.profile['name'], player_geo=self.profile['geo'])
        self.player_database.update_player_upgrades(player_name=self.profile['name'], player_upgrades=self.profile['upgrades'])

        return 'Congratulations, you purchased an upgrade! Now get into some bosses with your new obtained power!'

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

    def grant_geo(self, geo: int = 10):
        """
        give the player geo for interaction or time in chat
        :param geo: amount of geo you want to grant
        :return:
        """
        self.profile['geo'] += geo
        self.player_database.update_player_geo(player_name=self.profile['name'], player_geo=self.profile['geo'])
