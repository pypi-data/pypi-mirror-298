# coding=utf-8
"""
Listeners
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional, Iterable
from .interfaces import (
    IListener,
    IMessageTransmitter,
    IMessageForSubscriberTransmitter,
    IErrorsReciever,
    IMessageAdapter,
)


@dataclass
class Listener(IListener):
    """
    Listener that can get and transmitt message.
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
class MultiSubscriberListener(IListener):
    """
    Listener that can adapt message and distribute it to instances of subscribers.
    Args:
        message_transmitter: has to support __call__(self, subcsriber: Any, message: Any) interface.
        message_transmitter_errors_receiver (optional): has to support __call__(self, exc: Exception) interface.
        subscribers (optional, but useless without it): list of instances. Message will be distributed to each instance by message_transmitter.
        message_adapter (optional): has to support __call__(self, message: Any) interface.
        message_adapter_errors_receiver (optional): has to support __call__(self, exc: Exception) interface.
    """
    message_transmitter: IMessageForSubscriberTransmitter
    message_transmitter_errors_receiver: Optional[IErrorsReciever] = None
    subscribers: List[Any] = field(default_factory=list)
    message_adapter: Optional[IMessageAdapter] = None
    message_adapter_errors_receiver: Optional[IErrorsReciever] = None

    def listen(self, message: Any):
        """
        Listen message and distribute it to subcribers
        """
        if self.subscribers:
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


class Listeners:
    """
    Registry of local listeners.
    It is not possible to subscribe listener more than once.
    """

    def __init__(self, listeners: Optional[Iterable[IListener]] = None):
        self.registry = {id(x): x for x in listeners or []}

    def __bool__(self):
        return bool(self.registry)

    def __iter__(self):
        return iter(self.registry.values())

    def __len__(self):
        return len(self.registry)

    def subscribe(self, listener: Any):
        """
        Subscribe listener
        """
        self.registry[id(listener)] = listener

    def unsubscribe(self, listener: Any):
        """
        Unsubscribe listener
        """
        self.registry.pop(id(listener), None)

    def send_message(self, message: Any):
        """
        Send message for listeners
        """
        for listener in self:
            # protection from reraise of errors receivers
            try:
                listener.listen(message)
            except Exception:  # pylint: disable=broad-exception-caught
                continue
