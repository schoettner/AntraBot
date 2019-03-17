import logging
from irc.client import Event, ServerConnection

from util.bot_utils import read_random_line_from_file
from util.event_handler import get_twitch_name, is_sub


class VysCommandHandler(object):
    """
    this class should handle all non battle relevant commands
    """

    def __init__(self, connection: ServerConnection, channel: str):
        self.connection = connection
        self.channel = '#%s' % channel
        self.channel_plain = channel
        self.count = 0
        self.quotation_file = 'config/quotation.txt'

    def public_command(self, e: Event, cmd: str):
        """
        public commands for vysualstv. those are more for fun purpose

        :param e: the chat event. containing arguments and tags
        :param cmd: the command as string
        :return: None
        """
        connection = self.connection

        if cmd == "vysquote":
            message = read_random_line_from_file(self.quotation_file)
            logging.debug("The printed quote will be: %s" % message)
            connection.privmsg(self.channel, message)
        elif cmd == "sub":
            name = get_twitch_name(e)
            sub = is_sub(e)
            if sub:
                message = ("Well done %s, you are subscribed. Keep being subbed to increase your power even more!" % name)
            else:
                message = ("I see %s. You lack in power. You should subscribe to @%s to fix this." % (name, self.channel_plain))
            connection.privmsg(self.channel, message)
        elif cmd == "purple":
            message = "Dont listen to StreamElements. The knight is purple due to black magic."
            connection.privmsg(self.channel, message)
        elif cmd == "zote":
            message = "He who must not be named. Just pass by and let Vengefly King do its job."
            connection.privmsg(self.channel, message)


    def special_command(self, e: Event, cmd: str):
        """
        those are the superior user commands designed for vysualstv

        :param e: the chat event. containing arguments and tags
        :param cmd: the command as string
        """
        connection = self.connection

        if cmd == "vyscount":
            message = "Count is at %i" % self.count
            connection.privmsg(self.channel, message)
        elif cmd == "vysup":
            self.count += 1
            message = "Count increased to %i" % self.count
            connection.privmsg(self.channel, message)
        elif cmd == "vysdown":
            self.count -= 1
            message = "Count decreased to %i" % self.count
            connection.privmsg(self.channel, message)
        elif cmd == "vysreset":
            self.count = 0
            message = "Count reset to %i" % self.count
            connection.privmsg(self.channel, message)
        elif cmd == "welcome":
            message = ("Welcome new follower. You made a wise choice to follow %s. Sit back and enjoy your time." % self.channel)
            connection.privmsg(self.channel, message)
