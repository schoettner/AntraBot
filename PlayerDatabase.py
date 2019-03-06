import pymongo
import logging

class PlayerDatabase(object):

    def __init__(self, connection_url: str = 'mongodb://localhost:27017/'):
        """
        connect to a mongo database. if the database does not exist yet, create it

        :param connection_url: the url to the mongoDB. use localhost if running on docker container
        """

        self.mongo_client = pymongo.MongoClient(connection_url)
        self.player_db = self.mongo_client['antrabot']  # create the database
        self.player_table = self.player_db['player']  # create the document / table
        logging.debug(self.mongo_client.list_database_names())

    def add_player(self, player: dict):
        """
        create a new player in the database. before the player is added, check if it already exists

        :param player:
        :return:
        """

        player_name = player['name']
        if self.get_player_by_name(player_name) is None:
            self.player_table.insert_one(player)

    def get_player_by_name(self, name: str):
        """
        load a player from the database

        :param name: the twitch-display name of the player
        :return: the player dict or None when there was no player found
        """

        query_search_query = {"name": name}
        player = self.player_table.find_one(query_search_query)
        return player

    def update_player_geo(self, player_name: str, player_geo: int):
        """
        set the geo value for a player
        :param player_name: the twitch display name of the player
        :param player_geo: the new geo value of the player
        :return:
        """

        query_search_query = {"name": player_name}
        update_command = {"$set": {"geo": player_geo}}
        self.player_table.update_one(query_search_query, update_command)

    def update_player_upgrades(self, player_name: str, player_upgrades: list):
        """
        update the list of upgrades the player has

        :param player_name: the twitch display name of the player
        :param player_upgrades: the new upgrades the player should have
        :return:
        """
        query_search_query = {"name": player_name}
        update_command = {"$set": {"upgrades": player_upgrades}}
        self.player_table.update_one(query_search_query, update_command)


if __name__ == "__main__":
    # initialize the database (running in a docker container)
    database = PlayerDatabase()

    # create and store example player
    example_player = {"strength": 10, "name": "antrazith", "geo": 9999, "upgrades": [3,6]}
    database.add_player(example_player)  # works

    # get the player, that was created
    query_result = database.get_player_by_name('antrazith')  # works
    print(query_result)

    # not_a_valid_player = database.get_player_by_name('i_am_not_in_the_database')
    # print(not_a_valid_player)

    updated_example_player = {"strength": 999, "name": "antrazith", "geo": 9999, "upgrades": [3,6]}
    database.update_player_geo('antrazith', 123456)

    # load the updated user again from the database
    query_result = database.get_player_by_name('antrazith')  # should now have 999 instead of 10 strength
    print(query_result)




# example of a player dict
# [{"strength": 10, "name": "antrazith", "geo": 9999, "upgrades": [3,6]}]