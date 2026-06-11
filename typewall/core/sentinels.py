from typing import Any


class _Sentinel:
    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return self.name


MISSING: Any = _Sentinel("MISSING")
INVALID: Any = _Sentinel("INVALID")
