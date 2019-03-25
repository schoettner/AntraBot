from irc.client import ServerConnection


class ConnectionMock(ServerConnection):

    def __init__(self):
        # ignore the default
        super().__init__(None)
        self.text = None
        self.target = None

    def privmsg(self, target, text):
        # store the values to assert them later
        self.target = target
        self.text = text