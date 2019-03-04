import sys
from random import randint

import irc.bot
import requests
import logging
from irc.client import Event, ServerConnection

from battle import Battle


class TwitchBot(irc.bot.SingleServerIRCBot):

    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # command specific values
        self.count = 0
        self.battle = Battle()

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

    def on_welcome(self, c : ServerConnection, e: Event):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c : ServerConnection, e: Event):
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
        c = self.connection

        # general commands
        if cmd == "bot":
            message = "AntraBot is up and running. Getting more powerful"
            c.privmsg(self.channel, message)
        elif cmd == "antrabot":
            message = "The public commands are: !bot, !vysquote, !sub, !boss, !zote"
            print(message)
            c.privmsg(self.channel, message)
        elif cmd == "boss":
            message = self.read_file('bosses.txt')
            c.privmsg(self.channel, message)
        elif cmd == "vysquote":
            message = self.read_file()
            logging.debug("The printed quote will be: %s" % message)
            c.privmsg(self.channel, message)
        elif cmd == "purple":
            message = "Dont listen to StreamElements. The knight is purple due to black magic."
            c.privmsg(self.channel, message)
        elif cmd == "zote":
            message = "He who must not be named. Just pass by and let Vengefly King do its job."
            c.privmsg(self.channel, message)
        elif cmd == "sub":
            sub = e.tags[8]['value']  # is subbed this is 1 (as str)
            name = e.tags[2]['value']  # get the display name
            if sub == "1":
                message = ("Well done %s, you are subscribed. Keep being subbed to increase your power even more!" % name)
            else:
                message = ("I see %s. You lack in power. You should subscribe to @VysuaLsTV to fix this." % name)
            c.privmsg(self.channel, message)
        elif cmd == "battle":
            message = self.battle.fight_random_boss(10)
            # message = self.battle.fight_boss(10, 2)
            c.privmsg(self.channel, message)

    def special_command(self, e: Event, cmd: str):
        """
        execute a command. the permissions are not checked in here.
        only moderator etc should be allowed to use those commands.
        :param e: the event if required for any more details of the command
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

    def read_file(self, file_name: str = 'quotation.txt'):
        """
        read quote lines from a text file. The file is loaded every time to allow dynamic changes without a bot restart
        :param file_name: name of the textfile with the quotes. has to be in the same folder
        :return: None
        """
        file = open(file_name, 'r')
        lines = file.readlines()
        rand = randint(0, len(lines)-1)
        message = lines[rand]
        return message[:-1]  # remove the new line character. throws error in icr client


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
