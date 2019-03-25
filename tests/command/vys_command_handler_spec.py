from command.vys_command_handler import VysCommandHandler
from mocks.event_mock import EventMock
from mocks.message_handler_mock import MessageHandlerMock


class SpecVysCommandHandler:

    def test_public_commands(self):
        command_handler, message_mock = self.given_default_command_handler()
        event_mock = self.given_mock_event()

        # test purple command
        command_handler.public_command(event_mock, 'purple')
        assert message_mock.message == 'Dont listen to StreamElements. The knight is purple due to black magic.'

        # test zote command
        command_handler.public_command(event_mock, 'zote')
        assert message_mock.message == 'He who must not be named. Just pass by and let Vengefly King do its job.'

    def test_special_commands(self):
        command_handler, message_mock = self.given_default_command_handler()
        event_mock = self.given_mock_event()

        # test vyscount
        command_handler.special_command(event_mock, 'vyscount')
        assert message_mock.message == 'Count is at 0'

        # test vysup
        command_handler.special_command(event_mock, 'vysup')
        assert message_mock.message == 'Count increased to 1'

        # test vysdown
        command_handler.special_command(event_mock, 'vysdown')
        assert message_mock.message == 'Count decreased to 0'  # goes back from 1 to zero

        # test vysreset
        command_handler.special_command(event_mock, 'vysreset')
        assert message_mock.message == 'Count reset to 0'

    @staticmethod
    def given_default_command_handler():
        message_handler_mock = MessageHandlerMock()
        command_handler = VysCommandHandler(None, 'antrazith')
        command_handler.message_handler = message_handler_mock
        return command_handler, message_handler_mock

    @staticmethod
    def given_mock_event():
        return EventMock()
