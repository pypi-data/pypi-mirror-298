from helpers import (
    ResultKeeper,
    TransmitterErrorsKeeper,
    reraise,
)
from commonlisteners import Listeners, MultiSubscriberListener


def the_transmitter(instance: ResultKeeper, message: int):
    instance.result = instance.result / message


def test_ignore_reraised_errors():
    """
    Ignore reraised errors
    """
    instance = ResultKeeper(result=100)
    transmitter_errors_reciever = TransmitterErrorsKeeper(handlers=[reraise])
    listener = MultiSubscriberListener(
        message_transmitter=the_transmitter,
        message_transmitter_errors_receiver=transmitter_errors_reciever,
        subscribers=[instance],
    )
    listeners = Listeners([listener])
    message = 0
    assert len(transmitter_errors_reciever.exceptions) == 0
    listeners.send_message(message)
    assert len(transmitter_errors_reciever.exceptions) == 1
