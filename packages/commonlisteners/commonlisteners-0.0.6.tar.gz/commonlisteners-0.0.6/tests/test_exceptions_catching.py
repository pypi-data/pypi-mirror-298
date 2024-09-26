from helpers import (
    ResultSaver,
    TransmitterErrorsReciever,
    reraise,
)
from commonlisteners import Listeners, MultiSubscriberListener


def transmitter_for_multiobject_listener(instance: ResultSaver, message: int):
    instance.result = instance.result / message


def test_ignore_reraised_errors():
    """
    Ignore reraised errors
    """
    instance = ResultSaver(result=100)
    transmitter_errors_reciever = TransmitterErrorsReciever(handlers=[reraise])
    listener = MultiSubscriberListener(
        message_transmitter=transmitter_for_multiobject_listener,
        message_transmitter_errors_receiver=transmitter_errors_reciever,
        subscribers=[instance],
    )
    listeners = Listeners([listener])
    message = 0
    assert len(transmitter_errors_reciever.exceptions) == 0
    listeners.send_message(message)
    assert len(transmitter_errors_reciever.exceptions) == 1
