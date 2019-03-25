from src.upgrade.upgrade_loader import UpgradeLoader


class UpgradeLoaderMock(UpgradeLoader):
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