import requests
from random import randint

from util.player import Player


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

    return channel_viewers + broadcaster + vips + mods


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


def get_player_stats(player: Player):
    profile = player.profile
    name = profile['name']
    strength = player.get_strength()
    geo = profile['geo']
    score = profile['score']
    return '@%s you have %i Geo, %i total strength, a score of %i and the upgrades: ' % (name, geo, strength, score), profile['upgrades']