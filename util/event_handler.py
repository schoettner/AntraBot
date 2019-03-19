from irc.client import Event
import logging


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


def get_full_message(e: Event):
    """
    return the full message that the viewer sent

    :param e: the twitch event
    :return: the message
    """
    message = e.arguments[0]
    return str(message)


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
    badges = e.tags[0]
    badges_value = badges['value']
    if badges_value is None:
        return False
    return badge_name in badges_value


def get_twitch_name(e: Event):
    """
    get the twitch name of the event sender

    :param e: The twitch event
    :return: the name of the event sender in lower case
    """
    name = e.tags[2]['value']  # get the display name
    return str(name).lower()


def is_sub(e: Event):
    is_sub = e.tags[8]['value']  # is subbed this is 1 (as str)
    return is_sub == '1'


