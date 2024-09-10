from __future__ import annotations

import random
from collections import Counter
from typing import Any, Generic, Iterable, List, Protocol, Set, TypeVar


class BagItem(Protocol):
    def __lt__(self, other: Any, /) -> bool: ...

    def __hash__(self) -> int: ...


T = TypeVar("T", bound=BagItem)


class Bag(Generic[T]):
    def __init__(self, _v: Iterable[T], /) -> None:
        self._v: List[T] = list(_v)

    def __str__(self) -> str:
        out: List[str] = []
        for item in self._v:
            out.append(str(item))
        return f"({",".join(out)})"

    def __repr__(self) -> str:
        return f"{__class__.__name__}{self.__str__()}"

    def __len__(self) -> int:
        return len(self._v)

    def __eq__(self, other: Bag[T]) -> bool:
        return self.count() == other.count()

    def duplicate(self) -> Bag[T]:
        return Bag([x for x in self._v])

    def sort(self) -> None:
        self._v.sort()

    def pop_duplicates(self) -> Bag[T]:
        mine: Set[T] = set()
        others: List[T] = []
        for item in self._v:
            if item in mine:
                others.append(item)
            else:
                mine.add(item)

        self._v = list(mine)
        return Bag(others)

    def give_all_to(self, other: Bag[T]) -> None:
        other._v = self._v + other._v
        self._v = []

    def count(self) -> Counter[T]:
        return Counter(self._v)
