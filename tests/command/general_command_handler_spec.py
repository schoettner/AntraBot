from command.general_command_handler import GeneralCommandHandler
from mocks.event_mock import EventMock
from mocks.message_handler_mock import MessageHandlerMock


class SpecGeneralCommandHandler:

    def test_public_commands(self):
        command_handler, message_mock = self.given_default_command_handler()
        event_mock = self.given_mock_event()

        # test the bot command
        command_handler.public_command(event_mock, 'bot')
        assert message_mock.message == "AntraBot is up and running. Getting more powerful. Check " \
                                       "https://antrabot.fandom.com/wiki/How_to_play for more details how to play."

        # test 'commands' command
        command_handler.public_command(event_mock, 'commands')
        assert message_mock.message == 'Check https://antrabot.fandom.com/wiki/Commands for more details.'

        # test sub command
        command_handler.public_command(event_mock, 'sub')
        assert message_mock.message == 'Well done antrazith, you are subscribed. Keep being subbed to increase your power even more!'

        # test sub command for non sub
        event_mock.tags[8]['value'] = '0'  # unsubscribe in the event
        command_handler.public_command(event_mock, 'sub')
        assert message_mock.message == 'I see antrazith. You lack in power. You should subscribe to @antrazith to fix this.'

    def test_special_commands(self):
        command_handler, message_mock = self.given_default_command_handler()
        event_mock = self.given_mock_event()

        # do not test the 'antra' command since it changes a looot

        # check the welcome command
        command_handler.special_command(event_mock, 'welcome')
        assert message_mock.message == 'Welcome new follower. You made a wise choice to follow antrazith. Sit back and enjoy your time.'

    @staticmethod
    def given_default_command_handler():
        message_handler_mock = MessageHandlerMock()
        command_handler = GeneralCommandHandler(None, 'antrazith')
        command_handler.message_handler = message_handler_mock
        return command_handler, message_handler_mock

    @staticmethod
    def given_mock_event():
        return EventMock()
