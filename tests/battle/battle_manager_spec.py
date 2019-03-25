from mocks.player_mock import PlayerMock
from src.battle.battle_manager import BattleManager
from src.battle.boss_loader import BossLoader
from src.player.player import Player


class SpecBattleManager:

    def test_player_win(self):
        player = self.given_default_player()
        battle_manager = self.given_default_battle_manager()
        fight_results = battle_manager.fight_boss(player=player, boss_id=0)
        assert fight_results == 'Training Dummy was defeated. Glory to antrazith, the mighty warrior.'

    def test_player_defeat(self):
        player = self.given_default_player()
        battle_manager = self.given_default_battle_manager()
        fight_results = battle_manager.fight_boss(player=player, boss_id=45)
        assert fight_results == 'Absolute Radiance was victorious. antrazith disappears into the void.'

    def test_fight_random_boss(self):
        player = self.given_default_player()
        battle_manager = self.given_default_battle_manager()
        fight_results = battle_manager.fight_random_boss(player)
        assert fight_results is not None

    def test_boss_id_to_high(self):
        player = self.given_default_player()
        battle_manager = self.given_default_battle_manager()
        fight_results = battle_manager.fight_boss(player=player, boss_id=46)
        assert fight_results == 'The boss id you try to fight is not valid.'

    def test_boss_id_to_low(self):
        player = self.given_default_player()
        battle_manager = self.given_default_battle_manager()
        fight_results = battle_manager.fight_boss(player=player, boss_id=-1)
        assert fight_results == 'The boss id you try to fight is not valid.'

    @staticmethod
    def given_default_battle_manager():
        # this should rather be a mock but a real object
        return BattleManager(BossLoader())

    @staticmethod
    def given_default_player():
        return PlayerMock()
