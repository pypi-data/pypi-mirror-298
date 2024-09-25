from helpers import ResultSaver, TransmitterErrorsReciever
from commonlisteners import DistributingListener, Listeners


def transmitter_for_distributing_testing(instance: ResultSaver, message: int):
    instance.result = instance.result / message


def test_distributing_listening():
    """
    Ignore reraised errors
    """
    subscriber = ResultSaver(result=100)
    transmitter_errors_reciever = TransmitterErrorsReciever()
    listener = DistributingListener(
        message_transmitter=transmitter_for_distributing_testing,
        message_transmitter_errors_receiver=transmitter_errors_reciever,
        subscribers=[subscriber],
    )
    assert subscriber.result == 100
    listeners = Listeners([listener])
    message = 2
    listeners.send_message(message)
    assert subscriber.result == 50
    assert len(transmitter_errors_reciever.exceptions) == 0
