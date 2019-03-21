import logging

from irc.client import Event, ServerConnection

from src.command.command_handler import CommandHandler
from src.util.bot_utils import read_random_line_from_file


class VysCommandHandler(CommandHandler):
    """
    this class should handle all non battle relevant commands
    """

    def __init__(self, connection: ServerConnection, channel: str):
        super().__init__(connection, channel)
        self.count = 0
        self.quotation_file = 'config/quotation.txt'

    def public_command(self, e: Event, cmd: str):
        """
        public commands for vysualstv. those are more for fun purpose

        :param e: the chat event. containing arguments and tags
        :param cmd: the command as string
        """
        if cmd == "vysquote":
            message = read_random_line_from_file(self.quotation_file)
            logging.debug("The printed quote will be: %s" % message)
            self.message_handler.send_public_message(message)
            self.message_handler.send_public_message(message)
        elif cmd == "sub":
            name = self.get_twitch_name(e)
            sub = self.is_sub(e)
            if sub:
                message = (
                            "Well done %s, you are subscribed. Keep being subbed to increase your power even more!" % name)
            else:
                message = ("I see %s. You lack in power. You should subscribe to @%s to fix this." % (
                name, self.channel))
            self.message_handler.send_public_message(message)
        elif cmd == "purple":
            message = "Dont listen to StreamElements. The knight is purple due to black magic."
            self.message_handler.send_public_message(message)
        elif cmd == "zote":
            message = "He who must not be named. Just pass by and let Vengefly King do its job."
            self.message_handler.send_public_message(message)

    def special_command(self, e: Event, cmd: str):
        """
        those are the superior user commands designed for vysualstv

        :param e: the chat event. containing arguments and tags
        :param cmd: the command as string
        """
        if cmd == "vyscount":
            message = "Count is at %i" % self.count
            self.message_handler.send_public_message(message)
        elif cmd == "vysup":
            self.count += 1
            message = "Count increased to %i" % self.count
            self.message_handler.send_public_message(message)
        elif cmd == "vysdown":
            self.count -= 1
            message = "Count decreased to %i" % self.count
            self.message_handler.send_public_message(message)
        elif cmd == "vysreset":
            self.count = 0
            message = "Count reset to %i" % self.count
            self.message_handler.send_public_message(message)
        elif cmd == "welcome":
            message = (
                        "Welcome new follower. You made a wise choice to follow %s. Sit back and enjoy your time." % self.channel)
            self.message_handler.send_public_message(message)
