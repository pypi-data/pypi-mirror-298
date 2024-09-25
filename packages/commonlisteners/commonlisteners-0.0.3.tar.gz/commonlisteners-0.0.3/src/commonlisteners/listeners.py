# coding=utf-8
"""
Listeners
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional, Iterable
from .interfaces import (
    IListener,
    IMessageTransmitter,
    IMessageDistributingTransmitter,
    IErrorsReciever,
    IMessageAdapter,
)
from .utils import Hashable


@dataclass
class Listener(IListener, Hashable):
    """
    Hashable listener that can get and transmitt message.
    Args:
        message_transmitter: has to support __call__(self, message: Any) interface.
        message_transmitter_errors_receiver (optional): has to support __call__(self, exc: Exception) interface.
    """

    message_transmitter: IMessageTransmitter
    message_transmitter_errors_receiver: Optional[IErrorsReciever] = None

    def listen(self, message: Any):
        """
        Listen message
        """
        try:
            self.message_transmitter(message)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            if callable(self.message_transmitter_errors_receiver):
                self.message_transmitter_errors_receiver(exc)


@dataclass
class DistributingListener(IListener, Hashable):
    """
    Hashable listener that can get, adapt message and distribute it to instances of subscribers.
    Args:
        message_transmitter: has to support __call__(self, subscriber: Any, message: Any) interface.
        message_transmitter_errors_receiver (optional): has to support __call__(self, exc: Exception) interface.
        subscribers (optional, but useless without it): list of instances. Message will be distributed to each instance by message_transmitter.
        message_adapter (optional): has to support __call__(self, message: Any) interface.
        message_adapter_errors_receiver (optional): has to support __call__(self, exc: Exception) interface.
    """

    message_transmitter: IMessageDistributingTransmitter
    message_transmitter_errors_receiver: Optional[IErrorsReciever] = None
    subscribers: List[Any] = field(default_factory=list)
    message_adapter: Optional[IMessageAdapter] = None
    message_adapter_errors_receiver: Optional[IErrorsReciever] = None

    def listen(self, message: Any):
        """
        Listen message and distribute it to subcribers
        """
        if self. subscribers:
            if self.message_adapter:
                try:
                    message = self.message_adapter(message)
                except Exception as exc:  # pylint: disable=broad-exception-caught
                    if callable(self.message_adapter_errors_receiver):
                        self.message_adapter_errors_receiver(exc)
                    return

            for subscriber in self.subscribers:
                try:
                    self.message_transmitter(subscriber, message)
                except Exception as exc:  # pylint: disable=broad-exception-caught
                    if callable(self.message_transmitter_errors_receiver):
                        self.message_transmitter_errors_receiver(exc)
                    continue


class UnhashableListeners:
    """
    Registry of local listeners
    """
    REGISTRY_TYPE = list
    ADD_METHOD = 'append'
    REMOVE_METHOD = 'remove'

    def __init__(self, listeners: Optional[Iterable[IListener]] = None):
        self.registry = self.REGISTRY_TYPE(listeners or [])

    def subscribe(self, listener: Any):
        """
        Subscribe listener
        """
        if not listener in self.registry:
            getattr(self.registry, self.ADD_METHOD)(listener)

    def unsubscribe(self, listener: Any):
        """
        Unsubscribe listener
        """
        if listener in self.registry:
            getattr(self.registry, self.REMOVE_METHOD)(listener)

    def send_message(self, message: Any):
        """
        Send message for listeners
        """
        for listener in self.registry:
            # protection from reraise of errors receivers
            try:
                listener.listen(message)
            except Exception:  # pylint: disable=broad-exception-caught
                continue


class Listeners(UnhashableListeners):
    """
    Registry of local listeners
    """
    REGISTRY_INITIALIZATOR = set
    ADD_METHOD = 'add'
