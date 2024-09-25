from typing import Callable, List, Optional


class ResultSaver:
    def __init__(self, result):
        self.result = result


class TransmitterErrorsReciever:
    def __init__(self, handlers: Optional[List[Callable]] = None):
        self.exceptions = []
        self.handlers = handlers or []

    def __call__(self, exc):
        self.exceptions.append(exc)
        for handler in self.handlers or []:
            handler(exc)


def reraise(exc):
    raise exc
