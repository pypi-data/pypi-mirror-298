# coding=utf-8
"""
Listeners
"""

from dataclasses import dataclass, field
from collections import UserList
from typing import Any, List, Optional
from .interfaces import (
    IListener,
    IMessageTransmitter,
    IMessageDistributingTransmitter,
    IErrorsReciever,
    IMessageAdapter,
)


@dataclass
class Listener(IListener):
    """
    Class can get and adapt message for instances.
    Args:
        message_transmitter: has to support __call__(self, message: Any) interface.
        message_transmitter_errors_receiver: has to support __call__(self, exc: Exception) interface.
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
class DistributingListener(IListener):
    """
    Class can get and adapt message and distribute it to instances.
    Args:
        message_transmitter: has to support __call__(self, subscriber: Any, message: Any) interface.
        message_transmitter_errors_receiver: has to support __call__(self, exc: Exception) interface.
        subscribers: list of instances. Message will be distributed to each instance by message_transmitter.
        message_adapter: has to support __call__(self, message: Any) interface.
        message_adapter_errors_receiver: has to support __call__(self, exc: Exception) interface.
    """

    message_transmitter: IMessageDistributingTransmitter
    message_transmitter_errors_receiver: Optional[IErrorsReciever] = None
    subscribers: List[Any] = field(default_factory=list)
    message_adapter: Optional[IMessageAdapter] = None
    message_adapter_errors_receiver: Optional[IErrorsReciever] = None

    def listen(self, message: Any):
        """
        Listen message and distribute it to instances
        """
        if self.message_adapter:
            try:
                message = self.message_adapter(message)
            except Exception as exc:  # pylint: disable=broad-exception-caught
                if callable(self.message_adapter_errors_receiver):
                    self.message_adapter_errors_receiver(exc)
                return

        for subscriber in self.subscribers or []:
            try:
                self.message_transmitter(subscriber, message)
            except Exception as exc:  # pylint: disable=broad-exception-caught
                if callable(self.message_transmitter_errors_receiver):
                    self.message_transmitter_errors_receiver(exc)
                continue


class Listeners(UserList):
    """
    Registry of local listeners
    """

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
