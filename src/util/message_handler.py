from irc.client import ServerConnection


class MessageHandler(object):

    def __init__(self, connection: ServerConnection, channel: str):
        self.connection = connection
        self.channel = channel
        self.cooldown = 60  # cooldown time in seconds

    def send_public_message(self, message: str):
        """
        sends a message to the public chat. no cooldown on the message

        :param message: the message for the chat
        """
        self.connection.privmsg(self.channel, message)

    def send_public_cooldown_message(self, message: str, target: str):
        """
        send a message to the public chat. to prevent spam, the sender is set to a cooldown time
        :param message:
        :param target:
        """
        self.connection.privmsg(self.channel, message)

    def send_private_message(self, message: str, target: str):
        """
        send a whisper message from the bot to the target
        :param message: the message you want to send
        :param target: the twitch player nick to receive the whisper
        """
        self.connection.privmsg(target=target, text=message)
        return None
