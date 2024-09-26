from commonlisteners import Listener, Listeners, MultiSubscriberListener


def test_listener_subscribe():
    listener = Listener(
        message_transmitter=lambda message: print(message),
    )
    listeners = Listeners()
    assert len(listeners) == 0
    listeners.subscribe(listener)
    assert len(listeners) == 1

def test_listener_unsubscribe():
    listener = Listener(
        message_transmitter=lambda message: print(message),
    )
    listeners = Listeners()
    assert len(listeners) == 0
    listeners.subscribe(listener)
    assert len(listeners) == 1
    listeners.unsubscribe(listener)
    assert len(listeners) == 0

def test_multi_subscriber_listener_registration():
    listener = MultiSubscriberListener(
        message_transmitter=lambda subscriber, message: print(message),
    )
    listeners = Listeners()
    assert len(listeners) == 0
    listeners.subscribe(listener)
    assert len(listeners) == 1

def test_twice_registration():
    """
    Ignore reraised errors
    """
    listener = Listener(
        message_transmitter=lambda message: print(message),
    )
    listeners = Listeners()
    assert len(listeners) == 0
    listeners.subscribe(listener)
    assert len(listeners) == 1
    listeners.subscribe(listener)
    assert len(listeners) == 1
