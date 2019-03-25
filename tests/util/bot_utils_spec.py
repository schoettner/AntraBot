from mocks.event_mock import EventMock
from mocks.player_mock import PlayerMock
from src.util import bot_utils


class SpecBotUtils:

    def test_get_command(self):
        event = self.given_event_mock()
        event.arguments = ['!sub']
        command = bot_utils.get_command(event)
        assert command == 'sub'

    def test_no_command(self):
        event = self.given_event_mock()
        event.arguments = ['sub']
        command = bot_utils.get_command(event)
        assert command is None

    def test_has_mod_badge(self):
        event = self.given_event_mock()

        is_mod = bot_utils.has_badge(event, 'moderator')
        is_broadcaster = bot_utils.has_badge(event, 'broadcaster')
        assert is_mod is True
        assert is_broadcaster is False

    def test_super_user_detection(self):
        event = self.given_event_mock()

        is_super_user = bot_utils.is_superior_user(event)
        assert is_super_user is True

    def test_player_stats(self):
        player = PlayerMock()
        stats = bot_utils.get_player_stats(player)
        assert stats == ('@antrazith you have 1 Geo, 10 total strength, a score of 0 and the upgrades: ', [0])

    @staticmethod
    def given_event_mock():
        return EventMock()






