from expiringdict import ExpiringDict
from irc.client import ServerConnection


class MessageHandler(object):

    def __init__(self, connection: ServerConnection, channel: str):
        self.connection = connection
        # self.whisper_connection = ServerConnection()
        self.channel = channel
        self.cool_down = 60  # cool_down time in seconds before sending a message to the
        self.cache = ExpiringDict(max_len=100, max_age_seconds=10)

    def send_public_message(self, message: str):
        """
        sends a message to the public chat. no cooldown on the message

        :param message: the message for the chat
        """
        self.connection.privmsg(self.channel, message)

    def send_public_cooldown_message(self, message: str, sender: str):
        """
        send a message to the public chat. to prevent spam, the sender is set to a cooldown time
        :param message:
        :param sender:
        """
        if self.cache.get(sender) is None:
            self.cache[sender] = 'locked'
            self.connection.privmsg(self.channel, message)
            return
        else:
            print('chatter %s is still on cooldown' % sender)

    def send_private_message(self, message: str, target: str):
        """
        send a whisper message from the bot to the target

        keep in mind that this requires your token to have the whispers:read whispers:edit scopes!
        you can whisper from your own channel. jtv as channel is not required anymore

        :param message: the message you want to send
        :param target: the twitch player nick to receive the whisper
        """
        formatted_message = '.w %s %s' % (target, message)
        self.connection.privmsg(target=self.channel, text=formatted_message)
