from boss import Boss
from player import Player


class SpecBoss:

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

    def test_player_win(self):
        player = self.given_default_player()
        bosses = self.given_default_bosses()
        fight_results = bosses.fight_boss(player=player, boss_id=0)
        assert fight_results == 'Training Dummy was defeated. Glory to the mighty warrior.'

    def test_player_defeat(self):
        player = self.given_default_player()
        bosses = self.given_default_bosses()
        fight_results = bosses.fight_boss(player=player, boss_id=45)
        assert fight_results == 'Absolute Radiance was victorious. You disappear into the void.'

    def test_fight_random_boss(self):
        player = self.given_default_player()
        bosses = self.given_default_bosses()
        fight_results = bosses.fight_random_boss(player)
        assert fight_results is not None

    @staticmethod
    def given_default_bosses():
        return Boss()

    @staticmethod
    def given_default_player():
        return PlayerMock()


# player mock
class PlayerMock(Player):

    def __init__(self):
        super().__init__(None, None, None)

    def get_strength(self):
        return 10
