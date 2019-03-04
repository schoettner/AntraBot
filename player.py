import json
import logging


class Player(object):
    """control the player who is able to battle"""

    def __init__(self, name: str):
        self.player_list = 'players.json'
        self.default_strength = 10
        self.name = name
        logging.info("player %s is ready to go" % name)
        profile = self.load_player()
        if profile is None:
            profile = self.create_player()
        self.profile = profile

    def load_player(self):
        """
         load a player from a database or file storage
        :return: the player profile as dict or None if the player does not exist yet
        """
        with open(self.player_list) as f:
            player_list = json.load(f)

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
        data = {'name': self.name,
                'strength': self.default_strength,
                'upgrades': []}
        data['upgrades'].append({
            'item': 'nail',
            'strength': 1,
        })

        # todo this is terrible! read and overwrite every time. fix this later
        # read all players
        with open(self.player_list, 'r') as players_file:
            players = json.load(players_file)

        # add new player
        players.append(data)

        # write new player ist
        with open(self.player_list, 'w') as players_file:
            json.dump(players, players_file)

        return data

    def give_upgrade(self, upgrade: dict):
        """
        give the player an additional upgrade. if the player has the upgrade already, ignore it
        :param upgrade:
        :return:
        """
        # todo overwrite the player profile with the new upgrades. add any validation if the player can use the item?
        # e.g. can use shade soul without having vengeful spirit? and do i overwrite spirit or add shade soul on top?

        return None


    def get_strength(self):
        """
        get the total strength of a player
        :return: the players base strength and the strength of all the upgrades
        """
        upgrade_strength = 0
        for upgrade in self.profile['upgrades']:
            upgrade_strength += upgrade['strength']
        total_strength = self.profile['strength'] + upgrade_strength
        return total_strength

