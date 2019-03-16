from util.battle_manager import BattleManager
from util.boss_loader import BossLoader
from util.player import Player


class SpecBattleManager:

    def test_player_win(self):
        player = self.given_default_player()
        battle_manager = self.given_default_battle_manager()
        fight_results = battle_manager.fight_boss(player=player, boss_id=0)
        assert fight_results == 'Training Dummy was defeated. Glory to the mighty warrior.'

    def test_player_defeat(self):
        player = self.given_default_player()
        battle_manager = self.given_default_battle_manager()
        fight_results = battle_manager.fight_boss(player=player, boss_id=45)
        assert fight_results == 'Absolute Radiance was victorious. You disappear into the void.'

    def test_fight_random_boss(self):
        player = self.given_default_player()
        battle_manager = self.given_default_battle_manager()
        fight_results = battle_manager.fight_random_boss(player)
        assert fight_results is not None

    @staticmethod
    def given_default_battle_manager():
        # this should rather be a mock but a real object
        return BattleManager(BossLoader())

    @staticmethod
    def given_default_player():
        return PlayerMock()


# player mock
class PlayerMock(Player):

    def __init__(self):
        super().__init__(None, None, None)

    def get_strength(self):
        return 10