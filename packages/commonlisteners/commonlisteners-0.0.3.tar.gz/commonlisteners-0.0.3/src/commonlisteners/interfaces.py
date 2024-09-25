# coding=utf-8
"""
Interfaces
"""

from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol


class IMessageTransmitter(Protocol):
    @abstractmethod
    def __call__(self, message: Any):
        raise NotImplementedError()


class IMessageDistributingTransmitter(Protocol):
    @abstractmethod
    def __call__(self, instance: Any, message: Any):
        raise NotImplementedError()


class IErrorsReciever(Protocol):
    @abstractmethod
    def __call__(self, exc: Exception):
        raise NotImplementedError()


class IMessageAdapter(Protocol):
    @abstractmethod
    def __call__(self, message: Any):
        raise NotImplementedError()


@dataclass
class IListener:
    """
    Class can get and adapt message for instances
    """
    @abstractmethod
    def listen(self, message: Any):
        """
        Listen message
        """
        raise NotImplementedError()
