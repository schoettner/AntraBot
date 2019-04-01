from threading import Timer

from expiringdict import ExpiringDict
from irc.client import Event, ServerConnection

from src.battle.battle_manager import BattleManager
from src.command.command_handler import CommandHandler
from src.player.player import Player
from src.player.player_database import PlayerDatabase
from src.upgrade.upgrade_loader import UpgradeLoader
from src.util.bot_utils import get_viewers, get_player_stats, has_badge


class BattleCommandHandler(CommandHandler):
    """
    handles all battle related commands
    """

    def __init__(self,
                 connection: ServerConnection,
                 channel: str,
                 battle_manager: BattleManager,
                 player_database: PlayerDatabase,
                 upgrade_loader: UpgradeLoader,
                 geo_reward: int = 10,
                 ):
        super().__init__(connection, channel)

        self.battle_manager = battle_manager
        self.player_database = player_database
        self.upgrade_loader = upgrade_loader

        self.enable_geo_timer = True
        self.geo_time = 600  # seconds until ppl get geo
        self.geo_reward = geo_reward  # amount of geo people get every tick

        cache_time = 60  # time to cache the last message of someone
        self.cache = ExpiringDict(max_len=100, max_age_seconds=cache_time)

        # wait for the connection to be established than start the geo timer
        if self.enable_geo_timer:
            print('starting geo timer')
            Timer(interval=self.geo_time, function=self.schedule_geo).start()

    def public_command(self, e: Event, cmd: str):

        # prevent people spam
        name = self.get_twitch_name(e)
        if self.cache.get(name) is not None:
            print('viewer %s is still locked' % name)
            self.message_handler.send_private_message(message='You recently used !stats, !fight, !upgrade or another battle command.'
                                                              'Please wait 60 seconds before the next try.',
                                                      target=name)
            return

        # stats commands
        if cmd == "stats":
            player = self.get_player_by_event(e)
            stats, upgrades = get_player_stats(player)
            message = stats + self.get_player_upgrades(upgrades)
            self.message_handler.send_public_message(message)
        elif cmd == "leaderboard":
            message = self.player_database.get_leaderboard()
            self.message_handler.send_public_message(message)

        # boss fight commands
        elif cmd == "bosses":
            message = 'All bosses can be found here: https://antrabot.fandom.com/wiki/Bosses'
            self.message_handler.send_public_message(message)
        elif cmd == "random":
            player = self.get_player_by_event(e)
            message = self.battle_manager.fight_random_boss(player)
            self.message_handler.send_private_message(message=message, target=name)
        elif cmd == "fight":
            received_id = e.arguments[0][7:]  # get message and remove first 7 chars '!fight '
            player = self.get_player_by_event(e)
            if str(received_id).isnumeric():  # check if the given id is valid
                boss_id = int(received_id)
                message = self.battle_manager.fight_boss(player, boss_id)
            else:
                message = 'You entered an invalid number. Can not fight that boss.'
            self.message_handler.send_private_message(message=message, target=name)

        # upgrade commands
        elif cmd == "upgrades":
            message = 'All upgrades can be found here: https://antrabot.fandom.com/wiki/Upgrades'
            self.message_handler.send_public_message(message)
        elif cmd == "buy":
            received_id = e.arguments[0][5:]  # get message and remove first 5 chars '!buy '
            player = self.get_player_by_event(e)
            if str(received_id).isnumeric():  # check if the given id is valid
                upgrade_id = int(received_id)  # need to cast the str i.e. to int
                message = player.buy_upgrade(upgrade_id)  # upgrade your nail
            else:
                message = 'You entered an invalid number. Can not buy that item. Use !buy <upgrade_id>'
            self.message_handler.send_private_message(message=message, target=name)
        else:
            # not a valid command
            return

        # a valid command was executed, now lock the user for using one again soon
        self.cache[name] = 'locked'

    def special_command(self, e: Event, cmd: str):
        is_broadcaster = has_badge(e, 'broadcaster')
        sender = self.get_twitch_name(e)
        if is_broadcaster or sender == 'antrazith':
            # geo commands
            if cmd == "geo":
                self.grant_geo()
            if cmd == "geoset":
                message = self.set_player_geo(e)
                self.message_handler.send_public_message(message)
            if cmd == "reset":
                message = self.reset_player(e)
                self.message_handler.send_public_message(message)

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
        viewers = get_viewers(self.channel)
        if len(viewers) == 0:  # no viewers or broadcaster not online
            return
        for viewer in viewers:
            player = self.get_player_by_name(viewer)
            player.add_geo(geo=self.geo_reward)
        message = 'All viewers in chat have been blessed by the gods. You all gained %i Geo. Use !bot to see ' \
                  'how to play.' % self.geo_reward
        self.message_handler.send_public_message(message)

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
