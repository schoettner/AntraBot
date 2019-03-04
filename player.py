import json

class Player(object):
    """control the player who is able to battle"""

    def __init__(self, name: str):
        self.player_list = 'players.json'
        self.name = name
        print("player %s is ready to go" % name)
        profile = self.load_player()

    def load_player(self):
        """ load a player from a database or file storage"""
        with open(self.player_list) as f:
            player_list = json.load(f)

        for entry in player_list:
            if self.name == entry['name']:
                print('player is already in database')
                return entry
        print('player is not yet in database')
        return None

    def create_player(self):
        """ if no player exists yet, create one"""
        return None

    def get_strength(self):
        """ get the battle strength of the player"""
        return 10

