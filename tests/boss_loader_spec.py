from util.boss_loader import BossLoader
from util.player import Player


class SpecBossLoader:

    def test_all_bosses(self):
        bosses = self.given_default_bosses()
        all_bosses, boss_number = bosses.get_all_bosses()
        assert boss_number == 46

    def test_first_boss(self):
        bosses = self.given_default_bosses()
        boss_name, boss_strength = bosses.get_boss(boss_id=0)
        assert boss_name == 'Training Dummy'
        assert boss_strength == 1

    def test_last_boss(self):
        bosses = self.given_default_bosses()
        boss_name, boss_strength = bosses.get_boss(boss_id=45)
        assert boss_name == 'Absolute Radiance'
        assert boss_strength == 191

    @staticmethod
    def given_default_bosses():
        return BossLoader()
