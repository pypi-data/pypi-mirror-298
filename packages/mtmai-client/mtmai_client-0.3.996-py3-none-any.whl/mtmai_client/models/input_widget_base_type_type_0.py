from enum import Enum


class InputWidgetBaseTypeType0(str, Enum):
    ARRAY = "array"
    BOOLEAN = "boolean"
    NUMBER = "number"
    OBJECT = "object"
    STRING = "string"
    TAGS = "tags"

    def __str__(self) -> str:
        return str(self.value)
