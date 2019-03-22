from threading import Timer

from irc.client import Event, ServerConnection

from src.battle.battle_manager import BattleManager
from src.battle.boss_loader import BossLoader
from src.player.player_database import PlayerDatabase
from src.command.command_handler import CommandHandler
from src.player.player import Player
from src.util.bot_utils import get_viewers, get_player_stats
from src.upgrade.upgrade_loader import UpgradeLoader


class BattleCommandHandler(CommandHandler):

    def __init__(self, connection: ServerConnection, channel: str):
        super().__init__(connection, channel)

        self.enable_geo_timer = True
        self.geo_time = 600  # seconds until ppl get geo
        self.geo_reward = 10  # amount of geo people get every tick
        self.boss_loader = BossLoader()
        self.battle_manager = BattleManager(self.boss_loader)
        self.player_database = PlayerDatabase()
        self.upgrade_loader = UpgradeLoader()

        # wait for the connection to be established than start the geo timer
        if self.enable_geo_timer:
            Timer(interval=self.geo_time, function=self.schedule_geo).start()

        print('battle command handler created')

    def public_command(self, e: Event, cmd: str):
        """
        commands that should be available for everyone.
        the message for the command is directly printed to twitch chat

        :param e: the chat event. containing arguments and tags
        :param cmd: the command as string
        :return: None
        """
        # general commands
        if cmd == "bot":
            message = "AntraBot is up and running. Getting more powerful. Check " \
                      "https://antrabot.fandom.com/wiki/How_to_play for more details how to play."
            self.message_handler.send_public_message(message)
        if cmd == "commands":
            message = "Check https://antrabot.fandom.com/wiki/Commands for more details."
            self.message_handler.send_public_message(message)

        # stats commands
        if cmd == "stats":
            player = self.get_player_by_event(e)
            stats, upgrades = get_player_stats(player)
            message = stats + self.get_player_upgrades(upgrades)
            self.message_handler.send_public_message(message)
        if cmd == "leaderboard":
            message = self.player_database.get_leaderboard()
            self.message_handler.send_public_message(message)

        # boss fight commands
        elif cmd == "bosses":
            message = 'All bosses can be found here: https://antrabot.fandom.com/wiki/Bosses'
            self.message_handler.send_public_message(message)
        elif cmd == "random":
            player = self.get_player_by_event(e)
            message = self.battle_manager.fight_random_boss(player)
            self.message_handler.send_public_message(message)
        elif cmd == "fight":
            received_id = e.arguments[0][7:]  # get message and remove first 7 chars '!fight '
            if str(received_id).isnumeric():  # check if the given id is valid
                player = self.get_player_by_event(e)
                boss_id = int(received_id)
                message = self.battle_manager.fight_boss(player, boss_id)
            else:
                message = 'You entered an invalid number. Can not fight that boss.'
            self.message_handler.send_public_message(message)

        # upgrade commands
        elif cmd == "upgrades":
            message = 'All upgrades can be found here: https://antrabot.fandom.com/wiki/Upgrades'
            self.message_handler.send_public_message(message)
        elif cmd == "buy":
            received_id = e.arguments[0][5:]  # get message and remove first 5 chars '!buy '
            if str(received_id).isnumeric():  # check if the given id is valid
                player = self.get_player_by_event(e)
                upgrade_id = int(received_id)  # need to cast the str i.e. to int
                message = player.buy_upgrade(upgrade_id)  # upgrade your nail
            else:
                message = 'You entered an invalid number. Can not buy that item. Use !buy <upgrade_id>'
            self.message_handler.send_public_message(message)

    def special_command(self, e: Event, cmd: str):
        """
        commands that are only available super users (broadcaster,mod,vip)
        the message for the command is directly printed to twitch chat

        :param e: the chat event. containing arguments and tags
        :param cmd: the command as string
        """
        # give geo to the people
        if cmd == "geo":
            self.grant_geo()
        if cmd == "geoset":
            message = self.set_player_geo(e)
            self.message_handler.send_public_message(message)
        if cmd == "reset":
            message = self.reset_player(e)
            self.message_handler.send_public_message(message)

        # special commands
        elif cmd == "antra":
            print(e)
            self.message_handler.send_private_message(message='hello from antrabot', target='antrazith')
            # message = "This is a debug command for the dark lord himself. Do not worry about it."
            # self.message_handler.send_public_message(message)

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
        viewers = get_viewers(self.channel)
        for viewer in viewers:
            player = self.get_player_by_name(viewer)
            player.add_geo(geo=self.geo_reward)
        message = 'All viewers in chat have been blessed by the gods. You all gained %i Geo. Use !bot to see ' \
                  'how to play.' % self.geo_reward
        c.privmsg(self.channel, message)

    def set_player_geo(self, event: Event):
        """
        set the geo for a certain player

        :param event: The twitch bot event
        """
        message_splits = self.get_full_message(event).split()
        if len(message_splits) is not 3:
            print('invalid command results given: %i' % len(message_splits))
            return "You did not enter the correct number of arguments. Please use 'geoset! <player name> <geo amount>'"
        name = message_splits[1]
        geo = message_splits[2]
        if not str(geo).isnumeric():  # does also handle negative values
            return "You did not enter a valid number for the amount of Geo."
        player = self.get_player_by_name(name)
        player.set_geo(int(geo))
        return "Player %s now has %s Geo." % (name, geo)

    def reset_player(self, event: Event):
        """
        reset a player by deleting it from the database

        :param event: the event that tells to delete a character
        :return: the delete message
        """
        message_splits = self.get_full_message(event).split()
        if len(message_splits) is not 2:
            print('invalid command results given: %i' % len(message_splits))
            return "You did not enter the correct number of arguments. Please use 'reset! <player name>'"
        name = message_splits[1]
        self.player_database.delete_player(name)
        return 'You did reset the player: %s' % name

    def get_player_by_name(self, name: str):
        """
        get the player from the database

        :param name: name of the player
        :return: the player
        """
        player_profile = self.player_database.get_or_create_player(name)
        player = Player(profile=player_profile, upgrade_loader=self.upgrade_loader,
                        player_database=self.player_database)
        return player

    def get_player_by_event(self, e: Event):
        """
        get the player from the database

        :param e: the twitch event which contains the name of the sender
        :return: the player
        """
        name = self.get_twitch_name(e)
        return self.get_player_by_name(name)

    def get_player_upgrades(self, upgrade_ids: list):
        upgrade_names = []
        upgrades = self.upgrade_loader.get_upgrades_by_ids(upgrade_ids)
        for upgrade in upgrades:
            upgrade_names.append(upgrade['name'])
        return str(upgrade_names)
