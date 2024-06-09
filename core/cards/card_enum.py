from enum import Enum


class SuitEnum(str, Enum):
    D: str = "♦"
    H: str = "♥"
    C: str = "♣"
    S: str = "♠"

    @classmethod
    def length(cls) -> int:
        return len(cls.__annotations__)

    @classmethod
    def enum_set(cls) -> list[str]:
        return [x[0] for x in cls.__annotations__]


class HigherRankEnum(int, Enum):
    J: int = 11
    Q: int = 12
    K: int = 13
    A: int = 14

    @classmethod
    def name_by_value(cls, value: int) -> str | int:
        for member in cls:
            if member.value == value:
                return member.name
        return value

    @classmethod
    def length(cls) -> int:
        return len(cls.__annotations__)

    @classmethod
    def highest(cls) -> int:
        return max(cls._member_map_.values()).value

    @classmethod
    def lowest(cls) -> int:
        return min(cls._member_map_.values()).value
