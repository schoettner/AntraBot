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

    def get_or_create_player(self, player_name: str):
        """
        check if the player is found. if not, create a new player player with default values
        make sure to convert the player name to lower case. this is mandatory because the twitch REST api returns
        all player names in lower case

        :param player_name: the twitch display name of the player
        :return: the dict of the player
        """
        player = self.get_player_by_name(player_name.lower())
        if player is None:
            new_player = self.get_default_player(player_name)
            self.add_player(new_player)
            player = self.get_player_by_name(player_name)
        return player

    @staticmethod
    def get_default_player(player_name: str):
        """
        create a player that has only the base strenght, 1 geo and the old nail

        :param player_name:
        :return:
        """
        return {"strength": 10, "name": player_name, "geo": 1, "upgrades": [0]}


    ##########################################################################################
    ############################## UPDATE PLAYER ###################################
    ##########################################################################################

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