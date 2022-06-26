import random
from typing import Optional


def roll_d6(
        dm: int = 0, min_: Optional[int] = None, max_: Optional[int] = None, r: Optional[random.Random] = None
) -> int:
    return cap((r or random).randint(1, 6) + dm, min_, max_)


def roll_2d6(
    dm: int = 0, min_: Optional[int] = None, max_: Optional[int] = None, r: Optional[random.Random] = None
) -> int:
    r = r or random
    return cap(r.randint(1, 6) + r.randint(1, 6) + dm, min_, max_)


def cap(value: int, min_: Optional[int] = None, max_: Optional[int] = None) -> int:
    if min_ is not None:
        value = max(min_, value)
    if max_ is not None:
        value = min(max_, value)
    return value


def e_hex(value: int) -> str:
    if value <= 9:
        return str(value)
    return chr(ord('A') + value - 0xA)


def subsector_code(index: int) -> str:
    return chr(ord('A') + index)


def to_coords(x: int, y: int) -> str:
    return f"{x:02}{y:02}"
