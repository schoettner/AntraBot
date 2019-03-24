from src.player.player_database import PlayerDatabase
from src.player.player import Player
from src.upgrade.upgrade_loader import UpgradeLoader


class SpecPlayer:

    # def test_dummy_failure(self):
    #     assert False

    def test_total_strength(self):
        player = self.given_default_player()

        expected_strength = 46  # 10 from player + 21 pure nail + 15 spirit
        actual_strength = player.get_strength()
        assert actual_strength == expected_strength

    def test_grant_geo_to_player(self):
        player = self.given_default_player()
        player.add_geo(10)
        assert player.profile['geo'] == 11  # 1 start + 10 granted

    def test_purchase_base_nail(self):
        player = self.given_default_player()

        expected_message = "You can not purchase 'Old Nail' again. You either have it already or upgraded it. Check https://antrabot.fandom.com/wiki/How_to_play for more details."
        purchase_message = player.buy_upgrade(upgrade_id=0)
        assert purchase_message == expected_message

    def test_purchase_owned_upgrade(self):
        player = self.given_default_player()
        player.upgrade_loader.set_upgrade(None)

        expected_message = 'You already own this upgrade. You can not purchase it again.'
        purchase_message = player.buy_upgrade(upgrade_id=1)
        assert purchase_message == expected_message

    def test_purchase_invalid_id(self):
        player = self.given_default_player()
        player.upgrade_loader.set_upgrade(None)  # return None as upgrade

        expected_message = 'Upgrade with the id: 99 could not be found. Check https://antrabot.fandom.com/wiki/Upgrades for to find valid Upgrade IDs.'
        purchase_message = player.buy_upgrade(upgrade_id=99)
        assert purchase_message == expected_message

    def test_purchase_to_expensive_upgrade(self):
        player = self.given_default_player()

        expected_message = 'Seems like you have not enough Geo. Come back when you collected some more. ' \
                           'Use !stats to check your Geo.'
        purchase_message = player.buy_upgrade(upgrade_id=2)
        assert purchase_message == expected_message

    def test_to_purchase_unavailable_item(self):
        player = self.given_default_player()
        player.upgrade_loader.set_requirements(False)  # return that the player does not meet the requirements
        player.profile['geo'] = 100000  # give the player enough money to purchase the item

        expected_message = "You do not meet the requirements to purchase 'Channelled Nail'. " \
                           "You either do not have the required upgrade or you already own a better version."
        purchase_message = player.buy_upgrade(upgrade_id=2)
        assert purchase_message == expected_message

    def test_success_purchase_of_upgrade(self):
        player = self.given_default_player()
        player.profile['geo'] = 800  # give the player enough money to purchase the item

        expected_message = "Congratulations, you purchased 'Channelled Nail'! " \
                           "Now get into some bosses with your new obtained power!"
        purchase_message = player.buy_upgrade(upgrade_id=2)
        assert purchase_message == expected_message
        assert player.profile['geo'] == 0  # drop back to 0 geo after the purchase
        assert player.profile['upgrades'] == [2]  # remove 1 from the list and now have only 2

    def given_default_player(self):
        return Player(profile=self.given_default_player_profile(),
                      player_database=self.given_default_database(),
                      upgrade_loader=self.given_default_upgrade_loader())

    @staticmethod
    def given_default_player_profile():
        return {"strength": 10, "name": 'player123', "geo": 1, "upgrades": [1]}

    @staticmethod
    def given_default_database():
        return DatabaseMock()

    @staticmethod
    def given_default_upgrade_loader():
        loader = UpgradeLoaderLoaderMock()
        return loader


class DatabaseMock(PlayerDatabase):

    def set_player_geo(self, player_name: str, player_geo: int):
        print('update geo was called')
        pass

    def set_player_upgrades(self, player_name: str, player_upgrades: list):
        print('update upgrades was called')
        pass


class UpgradeLoaderLoaderMock(UpgradeLoader):
    """
    create a simple to control mock element to handle upgrades in tests
    """

    def __init__(self):
        super().__init__()
        # set default values
        self.upgrade = {"id": 2, "name": "Channelled Nail", "strength": 13, "costs": 800, "requires": 1}
        self.upgrades = [{"id": 4, "name": "Pure Nail", "strength": 21, "costs": 4000, "requires": 3},
                         {"id": 5, "name": "Vengeful Spirit", "strength": 15, "costs": 1500, "requires": None}]
        self.requirements = True

    # setup the mock
    def set_upgrade(self, upgrade):
        self.upgrade = upgrade

    def set_upgrades(self, upgrades: list):
        self.upgrades = upgrades

    def set_requirements(self, meeting_requirements: bool):
        self.requirements = meeting_requirements

    # interface methods
    def meets_requirements(self, desired_upgrade: dict, owned_upgrades: list):
        return self.requirements

    def get_upgrades_by_ids(self, upgrade_ids: list):
        return self.upgrades

    def get_upgrade(self, upgrade_id: int = 0):
        return self.upgrade