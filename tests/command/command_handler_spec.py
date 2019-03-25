from irc.client import Event

from mocks.event_mock import EventMock
from src.command.command_handler import CommandHandler


class SpecCommandHandler:

    def test_describes_interface(self):
        handler = self.given_default_command_handler()
        handler.public_command(None, None)
        handler.special_command(None, None)

    def test_full_message(self):
        handler = self.given_default_command_handler()
        event = EventMock()
        event.arguments = ['!buy whatever']

        message = handler.get_full_message(event)
        assert message == '!buy whatever'

    @staticmethod
    def given_default_command_handler():
        return CommandHandler(None, 'antrazith')
