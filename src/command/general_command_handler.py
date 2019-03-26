from irc.client import Event, ServerConnection

from src.command.command_handler import CommandHandler


class GeneralCommandHandler(CommandHandler):
    """
    handles all general commands
    """

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

    def special_command(self, e: Event, cmd: str):
        # special commands
        if cmd == "antra":
            print(e)
            # self.message_handler.send_public_cooldown_message(message='hello', target='antrazith')
            message = "This is a debug command for the dark lord himself. Do not worry about it."
            self.message_handler.send_public_message(message)
        elif cmd == "welcome":
            message = ("Welcome new follower. You made a wise choice to follow %s. Sit back and enjoy your time." % self.channel)
            self.message_handler.send_public_message(message)
