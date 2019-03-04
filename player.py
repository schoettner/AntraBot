import json
import logging

from upgrade import Upgrade


class Player(object):
    """control the player who is able to battle"""

    def __init__(self, name: str):
        logging.info("player %s is ready to go" % name)

        # default values
        self.player_list = 'config/players.json'
        self.default_strength = 10
        self.default_geo = 1

        # parameter
        self.name = name
        self.upgrade_loader = Upgrade()
        profile = self.load_player()
        if profile is None:
            profile = self.create_player()
        self.profile = profile

    def load_player(self):
        """
        load a player from a database or file storage

        :return: the player profile as dict or None if the player does not exist yet
        """
        player_list = self.load_all_players()

        for entry in player_list:
            if self.name == entry['name']:
                logging.debug('player is already in database')
                return entry
        logging.debug('player is not yet in database')
        return None

    def create_player(self):
        """
        create the new player in your storage

        :return: the new player profile
        """
        new_player = {'name': self.name,
                      'strength': self.default_strength,
                      'geo': self.default_geo,
                      'upgrades': []}
        new_player['upgrades'].append({
            'item': 'nail',
            'strength': 1,
        })

        # todo this is terrible! read and overwrite every time. fix this later
        # read all players
        players = self.load_all_players()

        # add new player
        players.append(new_player)

        # write new player ist
        with open(self.player_list, 'w') as players_file:
            json.dump(players, players_file)

        return new_player

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

        # todo save the new profile
        return 'Congratulations, you purchased an upgrade! Now get into some bosses with your new obtained power!'

    def get_strength(self):
        """
        get the total strength of a player

        :return: the players base strength and the strength of all the upgrades
        """
        upgrade_strength = 0
        upgrade_list = self.upgrade_loader.get_upgrades(self.profile['upgrades'])
        for upgrade in upgrade_list:
            upgrade_strength += upgrade['strength']
        total_strength = self.profile['strength'] + upgrade_strength
        return total_strength

    def load_all_players(self):
        """
        load all players from the database. a player has the following attributes
        name - str: twitch display name
        strength - int: base strength of the player without upgrades
        geo - int: currency that allows the player to buy items
        upgrades - list[int]: list of owned upgrades

        :return: list of all players
        """
        with open(self.player_list, 'r') as players_file:
            players = json.load(players_file)
        return players

    def save_player_upgrade(self):
        # save the players progress so its the same after the next restart
        return None


if __name__ == "__main__":
    player = Player("antrazith")
    msg = player.buy_upgrade(4)
    # msg = player.get_strength()
    print(msg)
