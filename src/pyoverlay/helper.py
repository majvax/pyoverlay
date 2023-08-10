from dataclasses import dataclass
from typing import NamedTuple
from itertools import cycle

class Point(NamedTuple):
    """
    Represents a point in a 2D space.
    https://learn.microsoft.com/en-us/windows/win32/api/windef/ns-windef-point
    """
    x: int
    y: int

@dataclass
class Rect:
    """
    Represents a rectangle in a 2D space.
    https://learn.microsoft.com/en-us/windows/win32/api/windef/ns-windef-rect
    """
    left: int
    top: int
    right: int
    bottom: int

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top

    @property
    def center(self) -> Point:
        return Point(self.left+int(self.width / 2), int(self.top+self.height / 2))

class RGBA(NamedTuple):
    """Represents a color in RGBA format."""
    r: int
    g: int
    b: int
    a: float

class Color:
    """Contains a list of various colors."""
    RED = RGBA(255, 0, 0, 1.0)
    GREEN = RGBA(0, 255, 0, 1.0)
    BLUE = RGBA(0, 0, 255, 1.0)
    BLACK = RGBA(0, 0, 0, 1.0)
    WHITE = RGBA(255, 255, 255, 1.0)
    YELLOW = RGBA(255, 255, 0, 1.0)
    CYAN = RGBA(0, 255, 255, 1.0)
    MAGENTA = RGBA(255, 0, 255, 1.0)
    ORANGE = RGBA(255, 165, 0, 1.0)
    PURPLE = RGBA(128, 0, 128, 1.0)
    PINK = RGBA(255, 192, 203, 1.0)
    GRAY = RGBA(128, 128, 128, 1.0)
    DARK_GRAY = RGBA(169, 169, 169, 1.0)
    LIGHT_GRAY = RGBA(211, 211, 211, 1.0)
    BROWN = RGBA(165, 42, 42, 1.0)
    OLIVE = RGBA(128, 128, 0, 1.0)
    DARK_GREEN = RGBA(0, 100, 0, 1.0)
    DARK_RED = RGBA(139, 0, 0, 1.0)
    DARK_BLUE = RGBA(0, 0, 139, 1.0)
    DARK_ORANGE = RGBA(255, 140, 0, 1.0)
    DARK_PURPLE = RGBA(128, 0, 128, 1.0)
    DARK_PINK = RGBA(255, 20, 147, 1.0)
    DARK_CYAN = RGBA(0, 139, 139, 1.0)
    DARK_BROWN = RGBA(101, 67, 33, 1.0)
    DARK_OLIVE = RGBA(85, 107, 47, 1.0)
    DARK_GOLD = RGBA(184, 134, 11, 1.0)
    DARK_TEAL = RGBA(0, 128, 128, 1.0)
    DARK_SALMON = RGBA(233, 150, 122, 1.0) 
    DARK_LIME = RGBA(50, 205, 50, 1.0)
    DARK_LAVENDER = RGBA(230, 230, 250, 1.0)
    DARK_BEIGE = RGBA(245, 245, 220, 1.0)
    DARK_MAROON = RGBA(128, 0, 0, 1.0)
    DARK_MINT = RGBA(189, 252, 201, 1.0)
    DARK_PEACH = RGBA(255, 218, 185, 1.0)
    DARK_MUSTARD = RGBA(255, 219, 88, 1.0)
    DARK_CORAL = RGBA(205, 92, 92, 1.0)
    DARK_NAVY = RGBA(0, 0, 128, 1.0)
    DARK_TURQUOISE = RGBA(0, 206, 209, 1.0)
    DARK_INDIGO = RGBA(75, 0, 130, 1.0)
    DARK_SAND = RGBA(255, 235, 205, 1.0)
    DARK_RASPBERRY = RGBA(135, 38, 87, 1.0)

