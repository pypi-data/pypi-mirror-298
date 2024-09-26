from helpers import TransmitterErrorsKeeper
from commonlisteners import Listener, Listeners


def test_listening():
    """
    Ignore reraised errors
    """
    transmitter_errors_reciever = TransmitterErrorsKeeper()
    messages = []
    listener = Listener(
        message_transmitter=lambda message: messages.append(message),
        message_transmitter_errors_receiver=transmitter_errors_reciever,
    )
    listeners = Listeners([listener])
    assert len(messages) == 0
    message = 1
    listeners.send_message(message)
    assert len(messages) == 1
    assert len(transmitter_errors_reciever.exceptions) == 0
