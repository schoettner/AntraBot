import logging

import pymongo


class PlayerDatabase(object):

    def __init__(self, connection_url: str = 'mongodb://localhost:27017/', database_name: str = 'antrabot'):
        """
        connect to a mongo database. if the database does not exist yet, create it
        with the name of the database it is possible to create an own for each channel or testing

        :param connection_url: the url to the mongoDB. use localhost if running on docker container
        :param database_name: the name of the database
        """
        self.mongo_client = pymongo.MongoClient(connection_url)
        self.database = self.mongo_client[database_name]  # create the database
        self.player_table = self.database['player']  # create the document / table
        logging.debug(self.mongo_client.list_database_names())

    def __add_player(self, player: dict):
        """
        create a new player in the database. before the player is added, check if it already exists

        :param player:
        :return:
        """
        player_name = player['name']
        if self.__get_player_by_name(player_name) is None:
            self.player_table.insert_one(player)

    def __get_player_by_name(self, name: str):
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
        player_name = player_name.lower()
        player = self.__get_player_by_name(player_name.lower())
        if player is None:
            new_player = self.__get_default_player(player_name)
            self.__add_player(new_player)
            player = self.__get_player_by_name(player_name)
        return player

    def delete_player(self, player_name: str):
        """
        delete a player to reset all his values back to defaults

        :param player_name: the player you want to delete
        """
        player_name = player_name.lower()
        query_search_query = {"name": player_name}
        self.player_table.delete_one(query_search_query)

    def set_player_geo(self, player_name: str, player_geo: int):
        """
        set the geo value for a player

        :param player_name: the twitch display name of the player
        :param player_geo: the new geo value of the player
        :return:
        """
        player_name = player_name.lower()
        self.get_or_create_player(player_name)  # make sure the player exists
        query_search_query = {"name": player_name}
        update_command = {"$set": {"geo": player_geo}}
        self.player_table.update_one(query_search_query, update_command)

    def set_player_upgrades(self, player_name: str, player_upgrades: list):
        """
        set the list of upgrades the player has

        :param player_name: the twitch display name of the player
        :param player_upgrades: the new upgrades the player should have
        :return:
        """
        player_name = player_name.lower()
        self.get_or_create_player(player_name)  # make sure the player exists
        query_search_query = {"name": player_name}
        update_command = {"$set": {"upgrades": player_upgrades}}
        self.player_table.update_one(query_search_query, update_command)

    def set_player_score(self, player_name: str, player_score: int):
        """
        set the score of a player

        :param player_name: the twitch display name of the player
        :param player_score: the new score of the player
        :return:
        """
        player_name = player_name.lower()
        self.get_or_create_player(player_name)  # make sure the player exists
        query_search_query = {"name": player_name}
        update_command = {"$set": {"score": player_score}}
        self.player_table.update_one(query_search_query, update_command)

    def get_leaderboard(self, number_of_players=3):
        """
        return the leader board of the people
        :param number_of_players: number of people to return for the board
        :return: list of players
        """
        board = self.player_table.find(sort=[("score", pymongo.DESCENDING)]).limit(number_of_players)
        # now this is a list of dicts with players in it.
        result = []
        for place, player in enumerate(board):
            details = '%i. place: %s with score: %i' % (place + 1, player['name'], player['score'])
            result.append(details)
        print(result)
        return str(result)

    @staticmethod
    def __get_default_player(player_name: str):
        """
        create a player that has only the base strenght, 1 geo and the old nail

        :param player_name:
        :return:
        """
        player_name = player_name.lower()
        return {'strength': 10, 'name': player_name, 'geo': 1, 'score': 0, 'upgrades': [0]}
