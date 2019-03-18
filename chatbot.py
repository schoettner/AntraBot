import sys

import irc.bot
from threading import Timer

from irc.client import Event, ServerConnection

from util.battle_manager import BattleManager
from util.bot_utils import get_viewers, get_channel_id, get_player_stats
from util.event_handler import get_twitch_name, is_superior_user, get_command
from util.player_database import PlayerDatabase
from util.boss_loader import BossLoader
from util.player import Player
from util.upgrade_loader import UpgradeLoader
from vys_command_handler import VysCommandHandler


class TwitchBot(irc.bot.SingleServerIRCBot):

    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
        self.channel_plain = channel

        # command specific values
        self.enable_geo_timer = True
        self.geo_time = 600  # seconds until ppl get geo
        self.geo_reward = 10  # amount of geo people get every tick
        self.boss_loader = BossLoader()
        self.battle_manager = BattleManager(self.boss_loader)
        self.player_database = PlayerDatabase()
        self.upgrade_loader = UpgradeLoader()

        # Get the channel id, we will need this for v5 API calls
        self.channel_id = get_channel_id(client_id, channel)

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)

        # wait for the connection to be established than start the geo timer
        if self.enable_geo_timer:
            Timer(interval=self.geo_time, function=self.schedule_geo).start()
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
        self.public_command(e, cmd)
        self.vys_command_handler.public_command(e, cmd)

        # execute the super commands
        allowed = is_superior_user(e)
        if allowed is True:
            self.special_command(e, cmd)
            self.vys_command_handler.special_command(e, cmd)

    def public_command(self, e: Event, cmd: str):
        """
        commands that should be available for everyone.
        the message for the command is directly printed to twitch chat

        :param e: the chat event. containing arguments and tags
        :param cmd: the command as string
        :return: None
        """
        connection = self.connection

        # general commands
        if cmd == "bot":
            message = "AntraBot is up and running. Getting more powerful. Check " \
                      "https://antrabot.fandom.com/wiki/How_to_play for more details how to play. "
            connection.privmsg(self.channel, message)
        if cmd == "commands":
            message = "Check https://antrabot.fandom.com/wiki/Commands for more details."
            connection.privmsg(self.channel, message)

        # stats commands
        if cmd == "stats":
            player = self.get_player_by_event(e)
            message = get_player_stats(player)
            connection.privmsg(self.channel, message)
        if cmd == "leaderboard":
            message = "print leader board. tbd."
            connection.privmsg(self.channel, message)

        # boss fight commands
        elif cmd == "bosses":
            message = 'All bosses can be found here: https://antrabot.fandom.com/wiki/Bosses'
            connection.privmsg(self.channel, message)
        elif cmd == "random":
            player = self.get_player_by_event(e)
            message = self.battle_manager.fight_random_boss(player)
            connection.privmsg(self.channel, message)
        elif cmd == "fight":
            received_id = e.arguments[0][7:]  # get message and remove first 7 chars '!fight '
            if str(received_id).isnumeric():  # check if the given id is valid
                player = self.get_player_by_event(e)
                boss_id = int(received_id)
                message = self.battle_manager.fight_boss(player, boss_id)
            else:
                message = 'You entered an invalid number. Can not fight that boss.'
            connection.privmsg(self.channel, message)

        # upgrade commands
        elif cmd == "upgrades":
            message = 'All upgrades can be found here: https://antrabot.fandom.com/wiki/Upgrades'
            connection.privmsg(self.channel, message)
        elif cmd == "buy":
            received_id = e.arguments[0][5:]  # get message and remove first 5 chars '!buy '
            if str(received_id).isnumeric():  # check if the given id is valid
                player = self.get_player_by_event(e)
                upgrade_id = int(received_id)  # need to cast the str i.e. to int
                message = player.buy_upgrade(upgrade_id)  # upgrade your nail
            else:
                message = 'You entered an invalid number. Can not buy that item. Use !buy <upgrade_id>'
            connection.privmsg(self.channel, message)

    def special_command(self, e: Event, cmd: str):
        """
        commands that are only available super users (broadcaster,mod,vip)
        the message for the command is directly printed to twitch chat

        :param e: the chat event. containing arguments and tags
        :param cmd: the command as string
        """
        connection = self.connection

        # give geo to the people
        if cmd == "geo":
            self.grant_geo()

        # special commands
        elif cmd == "antra":
            print(e)
            message = "This is a debug command for the dark lord himself. Do not worry about it."
            connection.privmsg(self.channel, message)

    def schedule_geo(self):
        """
        create an infinite loop to grant geo every few minutes
        """
        self.grant_geo()
        Timer(interval=self.geo_time, function=self.schedule_geo).start()  # timer to grant geo again in 10 minutes

    def grant_geo(self):
        """
        give geo to everyone who is in chat
        """
        c = self.connection
        viewers = get_viewers(self.channel_plain)
        for viewer in viewers:
            player = self.get_player_by_name(viewer)
            player.grant_geo(geo=self.geo_reward)
        message = 'All viewers in chat have been blessed by the gods. You all gained %i Geo. Use !bot to see ' \
                  'how to play.' % self.geo_reward
        c.privmsg(self.channel, message)

    def get_player_by_name(self, name: str):
        """
        get the player from the database

        :param name: name of the player
        :return: the player
        """
        player_profile = self.player_database.get_or_create_player(name)
        player = Player(profile=player_profile, upgrade_loader=self.upgrade_loader, player_database=self.player_database)
        return player

    def get_player_by_event(self, e: Event):
        """
        get the player from the database

        :param e: the twitch event which contains the name of the sender
        :return: the player
        """
        name = get_twitch_name(e)
        return self.get_player_by_name(name)

def main():
    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <client id> <token> <channel>")
        sys.exit(1)

    username = sys.argv[1]
    client_id = sys.argv[2]
    token = sys.argv[3]
    channel = sys.argv[4]

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()


if __name__ == "__main__":
    main()
