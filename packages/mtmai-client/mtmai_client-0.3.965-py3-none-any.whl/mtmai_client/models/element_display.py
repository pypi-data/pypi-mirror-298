from enum import Enum


class ElementDisplay(str, Enum):
    INLINE = "inline"
    PAGE = "page"
    SIDE = "side"

    def __str__(self) -> str:
        return str(self.value)
