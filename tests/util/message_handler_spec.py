from mocks.connection_mock import ConnectionMock
from src.util.message_handler import MessageHandler


class SpecMessageHandler:

    def test_public_message(self):
        message_handler = self.given_default_message_handler()
        message_handler.send_public_message('i am a test')

        assert message_handler.connection.text == 'i am a test'
        assert message_handler.connection.target == 'testing_channel'

    def test_cooldown_message(self):
        message_handler = self.given_default_message_handler()
        # send two messages direct after each other from the same sender
        message_handler.send_public_cooldown_message('i am a test 1', 'random sender')
        message_handler.send_public_cooldown_message('i am a test 2', 'random sender')

        # check that the second message was not send
        assert message_handler.connection.text == 'i am a test 1'

    def test_cooldown_message_for_other_people(self):
        message_handler = self.given_default_message_handler()
        # send two messages direct after each other from different sender
        message_handler.send_public_cooldown_message('i am a test 1', 'random sender 1')
        message_handler.send_public_cooldown_message('i am a test 2', 'random sender 2')

        # since two different senders try to send a message, the second one is sent too
        assert message_handler.connection.text == 'i am a test 2'


    def test_whisper_message(self):
        # todo the whisper function does not work yet. have to look that up later
        message_handler = self.given_default_message_handler()
        message_handler.send_private_message(message='secret whisper', target='hidden_person')

        assert message_handler.connection.text == '.w hidden_person secret whisper'
        assert message_handler.connection.target == 'jtv'

    def given_default_message_handler(self):
        return MessageHandler(connection=ConnectionMock(), channel='testing_channel')



