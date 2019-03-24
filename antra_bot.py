import sys

import irc.bot
from irc.client import Event, ServerConnection

from src.command.general_command_handler import GeneralCommandHandler
from src.command.battle_command_handler import BattleCommandHandler
from src.command.vys_command_handler import VysCommandHandler
from src.util.bot_utils import get_channel_id, get_command, is_superior_user


class AntraBot(irc.bot.SingleServerIRCBot):

    def __init__(self, username, client_id, token, channel, mongo_uri):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # Get the channel id, we will need this for v5 API calls
        self.channel_id = get_channel_id(client_id, channel)

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)

        # create the command handlers
        self.general_command_handler = GeneralCommandHandler(self.connection, channel)
        self.battle_command_handler = BattleCommandHandler(self.connection, channel, 50, mongo_uri)
        self.vys_command_handler = VysCommandHandler(self.connection, channel)

    def on_welcome(self, c: ServerConnection, e: Event):
        """
        join the channel in which the bot should operate
        check the 'Twitch IRC Capabilities' section at https://dev.twitch.tv/docs/irc/guide/
        for more details on this

        :param c: server connection
        :param e: event
        """
        print('Joining ' + self.channel)
        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c: ServerConnection, e: Event):
        """
        this is called every time a message is received. keep this signature due to the icr interface

        :param c: the server connection. can be used to transfer an message
        :param e: the event. it contains sender, message, badges etc
        """
        # get the command
        cmd = get_command(e)
        if cmd is None:
            # leave early if there is no command
            return

        # execute public command
        self.general_command_handler.public_command(e, cmd)
        self.battle_command_handler.public_command(e, cmd)
        self.vys_command_handler.public_command(e, cmd)

        # execute the super commands
        allowed = is_superior_user(e)
        if allowed is True:
            self.general_command_handler.special_command(e, cmd)
            self.battle_command_handler.special_command(e, cmd)
            self.vys_command_handler.special_command(e, cmd)


def main():
    print(len(sys.argv))
    if len(sys.argv) != 6:
        print("Usage: python3 antra_bot.py <username> <client id> <token> <channel> <mongo_uri>")
        sys.exit(1)

    username = sys.argv[1]
    client_id = sys.argv[2]
    token = sys.argv[3]
    channel = sys.argv[4]
    mongo_uri = sys.argv[5]

    print("Starting bot with username: %s, clinet: %s, token: %s, channel: %s" % (username, client_id, token, channel))
    bot = AntraBot(username, client_id, token, channel, mongo_uri)
    bot.start()


if __name__ == "__main__":
    main()
