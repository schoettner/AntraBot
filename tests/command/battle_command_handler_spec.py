# from mockito import mock

from src.command.battle_command_handler import BattleCommandHandler
from tests.mocks.event_mock import EventMock
from tests.mocks.player_database_mock import PlayerDatabaseMock
from tests.mocks.upgrade_loader_mock import UpgradeLoaderMock
from tests.mocks.battle_manager_mock import BattleManagerMock
from tests.mocks.message_handler_mock import MessageHandlerMock


class DisabledSpecBattleCommandHandler:

    battle_manager_mock = BattleManagerMock()
    message_handler_mock = MessageHandlerMock()
    player_database_mock = PlayerDatabaseMock()
    upgrade_loader_mock = UpgradeLoaderMock()
    # battle_manager_mock = mock()
    # message_handler_mock = mock()
    # player_database_mock = mock()
    # upgrade_loader_mock = mock()

    def test_public_commands(self):
        command_handler = self.given_default_command_handler()
        event = self.given_mock_event()

        command_handler.public_command(event, 'stats')
        assert self.message_handler_mock.message == "@antrazith you have 1 Geo, 46 total strength, a score of 0 and the upgrades: ['Pure Nail', 'Vengeful Spirit']"

        # todo leaderboard

        command_handler.public_command(event, 'bosses')
        assert self.message_handler_mock.message == 'All bosses can be found here: https://antrabot.fandom.com/wiki/Bosses'

        # todo ...


    def given_default_command_handler(self):

        command_handler = BattleCommandHandler(None, 'antrazith',
                                               self.battle_manager_mock,
                                               self.player_database_mock,
                                               self.upgrade_loader_mock)
        command_handler.message_handler = self.message_handler_mock
        return command_handler

    @staticmethod
    def given_mock_event():
        return EventMock()


