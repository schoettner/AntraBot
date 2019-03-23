from src.command.command_handler import CommandHandler
from irc.client import Event, ServerConnection


class GeneralCommandHandler(CommandHandler):

    def __init__(self, connection: ServerConnection, channel: str):
        super().__init__(connection, channel)

    def public_command(self, e: Event, cmd: str):
        # general commands
        if cmd == "bot":
            message = "AntraBot is up and running. Getting more powerful. Check " \
                      "https://antrabot.fandom.com/wiki/How_to_play for more details how to play."
            self.message_handler.send_public_message(message)
        elif cmd == "commands":
            message = "Check https://antrabot.fandom.com/wiki/Commands for more details."
            self.message_handler.send_public_message(message)

    def special_command(self, e: Event, cmd: str):
        # special commands
        if cmd == "antra":
            print(e)
            # self.message_handler.send_public_cooldown_message(message='hello', target='antrazith')
            # message = "This is a debug command for the dark lord himself. Do not worry about it."
            # self.message_handler.send_public_message(message)
