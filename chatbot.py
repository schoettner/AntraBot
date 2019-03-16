import sys
from random import randint

import irc.bot
import requests
import logging

import schedule
from irc.client import Event, ServerConnection

from util.battle_manager import BattleManager
from util.player_database import PlayerDatabase
from util.boss_loader import BossLoader
from util.player import Player
from util.upgrade_loader import UpgradeLoader


class TwitchBot(irc.bot.SingleServerIRCBot):

    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
        self.channel_plain = channel

        # command specific values
        self.quotation_file = 'config/quotation.txt'
        self.boss_file = 'config/bosses.txt'
        self.count = 0
        self.battle_manager = BattleManager(BossLoader())
        self.player_database = PlayerDatabase()
        self.upgrade_loader = UpgradeLoader()

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)

    def on_welcome(self, c: ServerConnection, e: Event):
        """
        join the channel in which the bot should operate
        check the 'Twitch IRC Capabilities' section at https://dev.twitch.tv/docs/irc/guide/
        for more details on this

        :param c: server connection
        :param e: event
        :return: None
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
        :return: None
        """

        # get the command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            logging.info('Received command: ' + cmd)
        else:
            # leave if its not a command
            return

        # execute public command
        self.public_command(e, cmd)

        # execute the moderator commands
        allowed = self.get_command_permission(e.tags[0])
        if allowed is True:
            self.special_command(e, cmd)

    def get_command_permission(self, badges: dict):
        """
        checks if the badge list contains either broadcaster, moderator or vip

        :param badges: the whole bade list
        :return: Boolean if one of the demanded badges is given
        """
        badge_value = badges['value']
        if badge_value is None:
            return False
        moderator = self.has_badge(badges)
        broadcaster = self.has_badge(badges, 'broadcaster')
        vip = self.has_badge(badges, 'vip')
        permission = moderator or broadcaster or vip
        logging.debug("Can use command: %s" % permission)
        return permission

    def has_badge(self, badges: dict, badge_name: str = 'moderator'):
        """
        check if the badge list contains a specific badge

        :param badges: the whole badge list
        :param badge_name: the badge you are looking for
        :return: if the badge is in the list
        """
        badges_value = badges['value']
        if badges_value is None:
            return False
        return badge_name in badges_value

    def public_command(self, e: Event, cmd: str):
        """
        commands that should be available for everyone. no vip/mod/broadcaster needed.
        the message for the command is directly printed to twitch chat

        :param e: the chat event. containing arguments and tags
        :param cmd: the command as string
        :return: None
        """
        c = self.connection

        # general commands
        if cmd == "bot":
            message = "AntraBot is up and running. Getting more powerful"
            c.privmsg(self.channel, message)
        elif cmd == "antrabot":
            message = "The public commands are: !bot, !vysquote, !sub, !boss, !zote, !random, !buy <upgrade_id>, !fight <boss_id>"
            print(message)
            c.privmsg(self.channel, message)
        elif cmd == "boss":
            # todo replace with json file. no need to maintain two separate boss files
            message = self.read_random_line_from_file(self.boss_file)
            c.privmsg(self.channel, message)
        elif cmd == "vysquote":
            message = self.read_random_line_from_file(self.quotation_file)
            logging.debug("The printed quote will be: %s" % message)
            c.privmsg(self.channel, message)
        elif cmd == "purple":
            message = "Dont listen to StreamElements. The knight is purple due to black magic."
            c.privmsg(self.channel, message)
        elif cmd == "zote":
            message = "He who must not be named. Just pass by and let Vengefly King do its job."
            c.privmsg(self.channel, message)
        elif cmd == "sub":
            name = self.get_twitch_name(e)
            sub = self.is_sub(e)
            if sub == "1":
                message = ("Well done %s, you are subscribed. Keep being subbed to increase your power even more!" % name)
            else:
                message = ("I see %s. You lack in power. You should subscribe to @VysuaLsTV to fix this." % name)
            c.privmsg(self.channel, message)
        elif cmd == "random":
            name = self.get_twitch_name(e)
            player = self.get_player(name)
            message = self.battle_manager.fight_random_boss(player)
            c.privmsg(self.channel, message)
        elif cmd == "fight":
            received_id = e.arguments[0][7:]  # get message and remove first 7 chars '!fight '
            if str(received_id).isnumeric():  # check if the given id is valid
                name = self.get_twitch_name(e)
                player = self.get_player(name)
                boss_id = int(received_id)
                message = self.battle_manager.fight_boss(player, boss_id)
            else:
                message = 'You entered an invalid number. Can not fight that boss'
            c.privmsg(self.channel, message)
        elif cmd == "buy":
            received_id = e.arguments[0][5:]  # get message and remove first 5 chars '!buy '
            if str(received_id).isnumeric():  # check if the given id is valid
                name = self.get_twitch_name(e)
                player = self.get_player(name)
                upgrade_id = int(received_id)  # need to cast the str i.e. to int
                message = player.buy_upgrade(upgrade_id)  # upgrade your nail
            else:
                message = 'You entered an invalid number. Can not buy the item.'
            c.privmsg(self.channel, message)

    def special_command(self, e: Event, cmd: str):
        """
        execute a command. the permissions are not checked in here. only moderator etc should be allowed to use those commands.
        the message for the command is directly printed to twitch chat

        :param e: the chat event. containing arguments and tags
        :param cmd: the command as string
        :return: None
        """
        c = self.connection

        # counting commands 'travesty' or 'unfortunate'
        if cmd == "counter":
            message = "count is at %s" % self.count
            c.privmsg(self.channel, message)
        elif cmd == "count":
            self.count += 1
            message = "count is at %s" % self.count
            c.privmsg(self.channel, message)
        elif cmd == "countdown":
            self.count -= 1
            message = "count is at %s" % self.count
            c.privmsg(self.channel, message)
        elif cmd == "countreset":
            self.count = 0
            message = "count is at %s" % self.count
            c.privmsg(self.channel, message)

        # give geo to the ppl!
        elif cmd == "geo":
            self.grant_geo()

        elif cmd == "timer":
            # todo this does crash at this point. fix later
            schedule.every(10).seconds.do(self.grant_geo())

        # special commands
        elif cmd == "modcommands":
            message = "Moderators use the public commands and: !counter, !count, !countdown, !countreset, !welcome, !antra"
            c.privmsg(self.channel, message)
        elif cmd == "welcome":
            message = ("Welcome new follower. You made a wise choice to follow %s. Sit back and enjoy your time." % self.channel)
            c.privmsg(self.channel, message)
        elif cmd == "antra":
            print(e)
            message = "This is a debug command for the dark lord himself. Do not worry about it."
            c.privmsg(self.channel, message)

    def grant_geo(self):
        c = self.connection
        viewers = self.get_viewers()
        for viewer in viewers:
            player = self.get_player(viewer)
            player.grant_geo(geo=10)
        message = 'All viewers in chat have been blessed by the gods. You all gained 10 Geo. Use !buy to get yourself an upgrade!'
        c.privmsg(self.channel, message)

    @staticmethod
    def get_twitch_name(e: Event):
        return e.tags[2]['value']  # get the display name

    @staticmethod
    def is_sub(e: Event):
        return e.tags[8]['value']  # is subbed this is 1 (as str)

    def get_player(self, name: str):
        player_profile = self.player_database.get_or_create_player(name)
        player = Player(profile=player_profile, upgrade_loader=self.upgrade_loader, player_database=self.player_database)
        return player

    @staticmethod
    def read_random_line_from_file(file_name: str):
        """
        read quote lines from a text file. The file is loaded every time to allow dynamic changes without a bot restart

        :param file_name: name of the text-file with the quotes. has to be in the same folder
        :return: None
        """
        file = open(file_name, 'r')
        lines = file.readlines()
        rand = randint(0, len(lines)-1)
        message = lines[rand]
        return message[:-1]  # remove the new line character. throws error in irc client

    def get_viewers(self):
        """
        use the switch REST API to get all current viewers of a channel

        :return: list of all viewers in the channel
        """
        url = 'https://tmi.twitch.tv/group/user/%s/chatters' % self.channel_plain
        channel_viewers = requests.get(url).json()['chatters']['viewers']  # not sure yet if mod/admin are separate or also in here
        return channel_viewers


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
