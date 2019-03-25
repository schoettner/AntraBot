from src.command.battle_command_handler import BattleCommandHandler
from tests.mocks.event_mock import EventMock
from tests.mocks.message_handler_mock import MessageHandlerMock


class SpecBattleCommandHandler:

    def test_dummy(self):
        assert True

    @staticmethod
    def given_default_command_handler():
        message_handler_mock = MessageHandlerMock()
        command_handler = BattleCommandHandler(None, 'antrazith')
        command_handler.message_handler = message_handler_mock
        return command_handler, message_handler_mock

    @staticmethod
    def given_mock_event():
        return EventMock()