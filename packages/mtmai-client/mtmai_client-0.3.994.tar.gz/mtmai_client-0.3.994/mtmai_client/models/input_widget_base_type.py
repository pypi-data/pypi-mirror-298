from enum import Enum


class InputWidgetBaseType(str, Enum):
    ARRAY = "array"
    BOOLEAN = "boolean"
    NUMBER = "number"
    OBJECT = "object"
    STRING = "string"
    TAGS = "tags"

    def __str__(self) -> str:
        return str(self.value)
