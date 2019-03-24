import pymongo

from src.player.player_database import PlayerDatabase


class DisabledSpecPlayerDatabase:
    """
    !!!! CAUTION !!!!
    to run this test it is mandatory to have an mongo container running!
    use docker-compose up to make sure it is available
    """

    connection_url = 'mongodb://localhost:27017/'
    database_name = 'antrabot_testing'

    # def test_dummy(self):
    #     assert False

    def test_create_new_player(self):
        player_database = self.given_testing_database()
        player_name = 'player123'

        new_player = player_database.get_or_create_player(player_name)
        assert new_player['strength'] == 10
        assert new_player['name'] == player_name
        assert new_player['geo'] == 1
        assert new_player['upgrades'] == [0]

        self.teardown_testing_database()

    def test_reload_player(self):
        player_database = self.given_testing_database()
        player_name = 'yet another player'

        # first create the player and save its id
        new_player = player_database.get_or_create_player(player_name)
        creation_id = new_player['_id']

        # reload the player
        existing_player = player_database.get_or_create_player(player_name)
        loading_id = existing_player['_id']

        assert creation_id == loading_id
        self.teardown_testing_database()

    def test_change_existing_player_geo(self):
        player_database = self.given_testing_database()
        player_name = 'gimme more geo'
        player_geo = 123456789

        # create the player and update its geo
        player_database.get_or_create_player(player_name)
        player_database.set_player_geo(player_name=player_name, player_geo=player_geo)

        # reload the player
        existing_player = player_database.get_or_create_player(player_name)
        geo = existing_player['geo']

        assert geo == player_geo
        self.teardown_testing_database()

    def test_change_new_player_geo(self):
        player_database = self.given_testing_database()
        player_name = 'i am new, gimme geo'
        player_geo = 123456789

        # update geo without creating the player before
        player_database.set_player_geo(player_name=player_name, player_geo=player_geo)

        # reload the player
        existing_player = player_database.get_or_create_player(player_name)
        geo = existing_player['geo']

        assert geo == player_geo
        self.teardown_testing_database()

    def test_change_existing_player_upgrades(self):
        player_database = self.given_testing_database()
        player_name = 'gimme more upgrades'
        player_upgrades = [1, 3, 5]

        # create the player and update its upgrades
        player_database.get_or_create_player(player_name)
        player_database.set_player_upgrades(player_name=player_name, player_upgrades=player_upgrades)

        # reload the player
        existing_player = player_database.get_or_create_player(player_name)
        upgrades = existing_player['upgrades']

        assert upgrades == player_upgrades
        self.teardown_testing_database()

    def test_change_new_player_upgrades(self):
        # this should not be possible since new players dont have enough geo
        # yet better make sure no exception is thrown to crash the bot
        player_database = self.given_testing_database()
        player_name = 'i am new, gimme more upgrades'
        player_upgrades = [1, 3, 5]

        # update the upgrades without creating the player before
        player_database.set_player_upgrades(player_name=player_name, player_upgrades=player_upgrades)

        # reload the player
        existing_player = player_database.get_or_create_player(player_name)
        upgrades = existing_player['upgrades']

        assert upgrades == player_upgrades
        self.teardown_testing_database()

    # setup
    def given_testing_database(self):
        return PlayerDatabase(connection_url=self.connection_url,
                              database_name=self.database_name)

    # tear down
    def teardown_testing_database(self):
        mongo_client = pymongo.MongoClient(self.connection_url)
        mongo_client.drop_database(self.database_name)