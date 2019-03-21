from irc.client import Event, ServerConnection

from src.util.message_handler import MessageHandler


class CommandHandler(object):

    def __init__(self, connection: ServerConnection, channel: str):
        self.connection = connection
        self.channel = channel
        target = '#%s' % channel
        self.message_handler = MessageHandler(connection=connection, channel=target)

    def public_command(self, e: Event, cmd: str):
        pass

    def special_command(self, e: Event, cmd: str):
        pass

    @staticmethod
    def get_full_message(e: Event):
        """
        return the full message that the viewer sent

        :param e: the twitch event
        :return: the message
        """
        message = e.arguments[0]
        return str(message)

    @staticmethod
    def get_twitch_name(e: Event):
        """
        get the twitch name of the event sender

        :param e: The twitch event
        :return: the name of the event sender in lower case
        """
        name = e.tags[2]['value']  # get the display name
        return str(name).lower()

    @staticmethod
    def is_sub(e: Event):
        is_subscribed = e.tags[8]['value']  # is subbed this is 1 (as str)
        return is_subscribed == '1'
