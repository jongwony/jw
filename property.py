import enum
import curses

import key_event


class WindowHierarchy:
    pass


class Mode(enum.Enum):
    READY = 0
    SEARCH = 1
    RESULT = 2
    CLOSE = -1


