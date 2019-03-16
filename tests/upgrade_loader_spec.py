from util.upgrade_loader import UpgradeLoader


class SpecUpgrade:

    def test_full_upgrade_list(self):
        upgrades = self.given_default_upgrades()
        upgrade_list, upgrade_count = upgrades.get_all_upgrades()
        assert upgrade_count == 11

    def test_get_first_upgrade(self):
        upgrades = self.given_default_upgrades()
        upgrade = upgrades.get_upgrade(0)
        assert upgrade['id'] == 0
        assert upgrade['name'] == 'Old Nail'
        assert upgrade['strength'] == 5
        assert upgrade['costs'] == 0
        assert upgrade['requires'] is None

    def test_get_last_upgrade(self):
        upgrades = self.given_default_upgrades()
        upgrade = upgrades.get_upgrade(10)
        assert upgrade['id'] == 10
        assert upgrade['name'] == 'Abyss Shriek'
        assert upgrade['strength'] == 80
        assert upgrade['costs'] == 15000
        assert upgrade['requires'] == 9

    def test_get_multiple_upgrades(self):
        upgrades = self.given_default_upgrades()
        nails = upgrades.get_upgrades_by_ids([0, 1, 2, 3, 4])
        assert len(nails) == 5

    def test_nail_upgrade_success(self):
        upgrades = self.given_default_upgrades()
        owned_upgrades = [0]
        nail_upgrade = upgrades.get_upgrade(1)
        purchasable = upgrades.meets_requirements(nail_upgrade, owned_upgrades)
        assert purchasable is True

    def test_nail_upgrade_fails(self):
        upgrades = self.given_default_upgrades()
        owned_upgrades = [0]
        # try to skip one upgrade
        nail_upgrade = upgrades.get_upgrade(2)
        purchasable = upgrades.meets_requirements(nail_upgrade, owned_upgrades)
        assert purchasable is False

    def test_buy_owned_upgrade(self):
        upgrades = self.given_default_upgrades()
        owned_upgrades = [2]
        # you already own this upgrade
        nail_upgrade = upgrades.get_upgrade(2)
        purchasable = upgrades.meets_requirements(nail_upgrade, owned_upgrades)
        assert purchasable is False

    def test_downgrade_your_nail(self):
        upgrades = self.given_default_upgrades()
        owned_upgrades = [4]
        # you already own a better
        nail_upgrade = upgrades.get_upgrade(2)
        purchasable = upgrades.meets_requirements(nail_upgrade, owned_upgrades)
        assert purchasable is False

    def test_buy_a_spell(self):
        upgrades = self.given_default_upgrades()
        owned_upgrades = [0]
        # spell has no requirements
        nail_upgrade = upgrades.get_upgrade(9)
        purchasable = upgrades.meets_requirements(nail_upgrade, owned_upgrades)
        assert purchasable is True

    def test_to_downgrade_your_spell(self):
        upgrades = self.given_default_upgrades()
        owned_upgrades = [10]
        # already have an higher version
        nail_upgrade = upgrades.get_upgrade(9)
        purchasable = upgrades.meets_requirements(nail_upgrade, owned_upgrades)
        assert purchasable is False

    @staticmethod
    def given_default_upgrades():
        return UpgradeLoader()
