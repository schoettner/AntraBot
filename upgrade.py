import json
import logging


class Upgrade(object):
    """
    handle all battle upgrades for the player.
    """

    def __init__(self):
        self.upgrades_file = 'config/upgrades.json'

    def get_upgrade(self, upgrade_id: int = 0):
        """
        load a specific upgrade from the list
        :param upgrade_id: the identifier of the upgrade
        :return: returns the dict of the upgrade or None if the identifier was not found
        """
        upgrades_list = self.get_all_upgrades()

        if upgrade_id >= len(upgrades_list):
            return None

        for entry in upgrades_list:
            if upgrade_id == entry['id']:
                return entry
            logging.debug('upgrade not found in database')
        return None

    def get_upgrades(self, upgrade_ids: list):
        """
        load multiple upgrades at once

        :param upgrade_ids: list of upgrade ids you want to load
        :return: list of upgrades (as dict)
        """
        upgrades = []
        for upgrade_id in upgrade_ids:
            upgrades.append(self.get_upgrade(upgrade_id))
        return upgrades

    def get_all_upgrades(self):
        """
        load all available upgrades from the config file. they are reloaded every time to allow changes without a bot restart
        an upgrade has the following attributes:
            id - int: identifier of the upgrade
            name - str: name of the upgrade
            strength - int: strength bonus of the upgrade
            cost - int: geo costs of the upgrade
            requires - int: id of an item required for the upgrade. this prevents that you can jump from old to pure nail in one purchase

        :return: a dict with all upgrades
        """
        with open(self.upgrades_file) as f:
            upgrades_list = json.load(f)
        return upgrades_list

    def meets_requirements(self, desired_upgrade: dict, owned_upgrades: list):
        """
        This method allows you to verify if someone meets the requirements to purchase an upgrade.
        return false if the item does not have a requirement and the next id is already owned
        This is because the next id is the next version of the desired_upgrade and you want avoid downgrading

        :param desired_upgrade: the upgrade you want to acquire
        :param owned_upgrades: the list of owned upgrades
        :return: Boolean if the player meets the requirements to by the item
        """

        required_upgrade = desired_upgrade['requires']
        next_upgrade = desired_upgrade['id'] + 1

        # if nothing is required and you dont have the next upgrade already
        if required_upgrade is None and next_upgrade not in owned_upgrades:
            return True

        return required_upgrade in owned_upgrades


if __name__ == "__main__":
    upgrade = Upgrade()
    msg = upgrade.get_upgrade(1)
    print(msg)
