# coding=utf-8
"""
Utils
"""


class Hashable:
    """
    Mixin to make object hashable
    """
    def __hash__(self):
        return hash(self)
