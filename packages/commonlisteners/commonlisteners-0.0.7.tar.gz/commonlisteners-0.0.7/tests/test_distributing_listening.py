from helpers import ResultKeeper, TransmitterErrorsKeeper
from commonlisteners import MultiSubscriberListener, Listeners


def the_transmitter(instance: ResultKeeper, message: int):
    instance.result = instance.result / message


def test_distributing_listening():
    """
    Ignore reraised errors
    """
    subscriber = ResultKeeper(result=100)
    transmitter_errors_reciever = TransmitterErrorsKeeper()
    listener = MultiSubscriberListener(
        message_transmitter=the_transmitter,
        message_transmitter_errors_receiver=transmitter_errors_reciever,
        subscribers=[subscriber],
    )
    assert subscriber.result == 100
    listeners = Listeners([listener])
    message = 2
    listeners.send_message(message)
    assert subscriber.result == 50
    assert len(transmitter_errors_reciever.exceptions) == 0
