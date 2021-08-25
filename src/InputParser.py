from enum import Enum


class InputParser(object):
    def __init__(self):
        pass




class ValidCommand(Enum):
    DEPEND = 1
    INSTALL = 2
    REMOVE = 3
    LIST = 4
    END = 5
