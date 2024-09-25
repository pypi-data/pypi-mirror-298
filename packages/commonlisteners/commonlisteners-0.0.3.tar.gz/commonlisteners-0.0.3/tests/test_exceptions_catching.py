from helpers import (
    ResultForTesting,
    TransmitterToResultForTesting,
    TransmitterErrorsReciever,
    reraise,
)
from commonlisteners import Listener, Listeners


def test_ignore_reraised_errors():
    """
    Ignore reraised errors
    """
    instance = ResultForTesting(result=100)
    transmitter_errors_reciever = TransmitterErrorsReciever(handlers=[reraise])
    listener = Listener(
        message_transmitter=TransmitterToResultForTesting(
            lambda instance, message: instance.result / message
        ),
        instances=[instance],
        message_transmitter_errors_receiver=transmitter_errors_reciever,
    )
    listeners = Listeners([listener])
    message = 0
    assert len(transmitter_errors_reciever.exceptions) == 0
    listeners.send_message(message)
    assert len(transmitter_errors_reciever.exceptions) == 1
