from src.command.command_handler import CommandHandler
from tests.mocks.event_mock import EventMock


class SpecCommandHandler:

    def test_describes_interface(self):
        handler = self.given_default_command_handler()
        handler.public_command(None, None)
        handler.special_command(None, None)

    def test_event_support_commands(self):
        # test all the support commands for all command handler
        handler = self.given_default_command_handler()
        event = self.given_default_event()

        message = handler.get_full_message(event)
        assert message == '!buy 10'

        name = handler.get_twitch_name(event)
        assert name == 'antrazith'

        sub = handler.is_sub(event)
        assert sub is True

    @staticmethod
    def given_default_event():
        return EventMock()

    @staticmethod
    def given_default_command_handler():
        return CommandHandler(None, 'antrazith')
