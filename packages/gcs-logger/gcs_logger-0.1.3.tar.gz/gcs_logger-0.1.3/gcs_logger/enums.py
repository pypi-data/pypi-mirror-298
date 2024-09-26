from enum import Enum


class FontWeight(Enum):
    """Represents a font weight for ColorHandler, specifying the thickness of messages printed in a console that
    supports ANSI colors."""

    # Don't ask me why.
    NORMAL = 20
    BOLD = 1


class LogColor(Enum):
    """Represents a color for ColorHandler, specifying the color of messages printed in a console that supports ANSI
    colors."""

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    GRAY = 38
