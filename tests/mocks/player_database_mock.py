import mongomock

from src.player.player_database import PlayerDatabase


class DatabaseMock(PlayerDatabase):

    def __init__(self):
        super().__init__(mongomock.MongoClient())

    def set_player_geo(self, player_name: str, player_geo: int):
        print('update geo was called')
        pass

    def set_player_upgrades(self, player_name: str, player_upgrades: list):
        print('update upgrades was called')
        pass