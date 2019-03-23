import logging

from irc.client import Event, ServerConnection

from src.command.command_handler import CommandHandler
from src.util.bot_utils import read_random_line_from_file


class VysCommandHandler(CommandHandler):
    """
    handles all VysualsTv related commands
    """

    def __init__(self, connection: ServerConnection, channel: str):
        super().__init__(connection, channel)
        self.count = 0
        self.quotation_file = 'config/quotation.txt'

    def public_command(self, e: Event, cmd: str):
        if cmd == "vysquote":
            message = read_random_line_from_file(self.quotation_file)
            logging.debug("The printed quote will be: %s" % message)
            self.message_handler.send_public_message(message)
        elif cmd == "purple":
            message = "Dont listen to StreamElements. The knight is purple due to black magic."
            self.message_handler.send_public_message(message)
        elif cmd == "zote":
            message = "He who must not be named. Just pass by and let Vengefly King do its job."
            self.message_handler.send_public_message(message)

    def special_command(self, e: Event, cmd: str):
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

