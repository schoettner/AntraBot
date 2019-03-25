from src.player.player import Player


class PlayerMock(Player):

    def __init__(self):
        super().__init__(None, None, None)
        self.profile = {'strength': 10, 'name': 'antrazith', 'geo': 1, 'score': 0, 'upgrades': [0]}

    def get_strength(self):
        return 10

    def set_player_score(self, name: str, score: int):
        pass

    def reward_points(self, points: int = 0):
        pass

    def revoke_points(self, points: int = 0):
        pass
