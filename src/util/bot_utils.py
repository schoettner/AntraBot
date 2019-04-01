import logging
from random import randint

import requests
from irc.client import Event

from src.player.player import Player


def get_command(e: Event):
    """
    analyze the argument of the event to check if a command was received

    :param e: the received twitch event
    :return: the command as str or None if no command was received
    """
    # get the command
    if e.arguments[0][:1] == '!':
        cmd = e.arguments[0].split(' ')[0][1:]
        logging.info('Received command: ' + cmd)
        return cmd
    else:
        # leave if its not a command
        return None


def is_superior_user(e: Event):
    """
    checks if the badge list contains either broadcaster, moderator or vip

    since there is currently no information in the arguments about vip
    the badges are used to analyze if the user is superior

    :param e: the received twitch event
    :return: Boolean if one of the demanded badges is given
    """

    moderator = has_badge(e)
    broadcaster = has_badge(e, 'broadcaster')
    vip = has_badge(e, 'vip')
    permission = moderator or broadcaster or vip
    logging.debug("Can use command: %s" % permission)
    return permission


def has_badge(e: Event, badge_name: str = 'moderator'):
    """
    check if the badge list contains a specific badge

    :param e: the received event from twitch
    :param badge_name: the badge you are looking for
    :return: if the badge is in the list
    """

    badges_tag = list(filter(lambda tag: tag['key'] == 'badges', e.tags))
    badges_value = badges_tag[0]['value']
    if badges_value is None:
        return False
    return badge_name in badges_value


def get_channel_id(client_id: str, channel: str):
    url = 'https://api.twitch.tv/kraken/users?login=' + channel
    headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
    r = requests.get(url, headers=headers).json()
    return r['users'][0]['_id']


def transform_upgrades(upgrades: list):
    message = []
    for upgrade in upgrades:
        upgrade_id = upgrade['id']
        name = upgrade['name']
        cost = upgrade['costs']
        # str is an immutabel object! add multiple strings into one list instead of changing message
        message.append('Id: %i, Name: %s, Costs: %i' % (upgrade_id, name, cost))
    return str(message)


def get_viewers(channel: str, include_all: bool = True):
    """
    use the switch REST API to get all current viewers of a channel
    e.g. https://tmi.twitch.tv/group/user/antrazith/chatters

    :param channel: the twitch channel you want to check
    :param include_all: if true, all mods are included too
    :return: list of all viewers in the channel
    """
    url = 'https://tmi.twitch.tv/group/user/%s/chatters' % channel
    request_results = requests.get(url).json()['chatters']
    channel_viewers = request_results['viewers']
    if not include_all:
        return channel_viewers
    broadcaster = request_results['broadcaster']
    vips = request_results['vips']
    mods = request_results['moderators']

    # only return viewers if the broadcaster is online itself
    return channel_viewers + broadcaster + vips + mods if len(broadcaster) == 1 else []


def read_random_line_from_file(file_name: str):
    """
    read quote lines from a text file. The file is loaded every time to allow dynamic changes without a bot restart

    :param file_name: name of the text-file with the quotes. has to be in the same folder
    :return: None
    """
    file = open(file_name, 'r')
    lines = file.readlines()
    rand = randint(0, len(lines) - 1)
    message = lines[rand]
    return message[:-1]  # remove the new line character. throws error in irc client


def get_player_stats(player: Player):
    profile = player.profile
    name = profile['name']
    strength = player.get_strength()
    geo = profile['geo']
    score = profile['score']
    return '@%s you have %i Geo, %i total strength, a score of %i and the upgrades: ' % (name, geo, strength, score), \
           profile['upgrades']
