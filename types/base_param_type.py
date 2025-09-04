from enum import Enum


class UseField(object):
    def __init__(self, arg):
        super().__init__()
        self.arg = arg


class FilterType(Enum):
    All: str = 'All'
    No: str = 'No'
