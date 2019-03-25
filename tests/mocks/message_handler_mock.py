from src.util.message_handler import MessageHandler


class MessageHandlerMock(MessageHandler):

    def __init__(self):
        super().__init__(None, None)
        self.message = None

    def send_public_message(self, message: str):
        self.message = message
