from irc.client import Event

class EventMock(Event):

    def __init__(self):
        super().__init__(None, None, None)
        self.arguments = ['!bot']
        self.tags = [
            {'key': 'badges', 'value': 'moderator/1,subscriber/0'},
            {'key': 'color', 'value': None},
            {'key': 'display-name', 'value': 'antrazith'},
            {'key': 'emotes', 'value': None},
            {'key': 'flags', 'value': None},
            {'key': 'id', 'value': 'b17cb0cc-020e-4870-b852-b41552293607'},
            {'key': 'mod', 'value': '1'},
            {'key': 'room-id', 'value': '40845619'},
            {'key': 'subscriber', 'value': '1'},
            {'key': 'tmi-sent-ts', 'value': '1551649272633'},
            {'key': 'turbo', 'value': '0'},
            {'key': 'user-id', 'value': '60432977'},
            {'key': 'user-type', 'value': 'mod'}
        ]