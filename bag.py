from __future__ import annotations

from collections import Counter
from typing import Any, Generic, Iterable, List, Protocol, Set, TypeVar

"""
Implementation of a mutable bag of conserved objects.

We can imagine each bag object as a physical bag with physical objects inside it.

All operations (except initialization and duplication) should therefore conserve
the objects. Some operations, like sorting and dropping duplicates, should also
not change the contents if used repeatedly and consecutively, i.e., they are
idempotent. These are the primary properties we want to test for.

Example ---

Bag1: (1, 2, 2, 3)
Bag2: (1, 2)

Bag1 gives all to Bag2...
Bag1: ()
Bag2: (1, 2, 2, 2, 3)

"""


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
        """
        BEFORE
        Bag: (1, 2, 3)

        AFTER
        Bag:    (1, 2, 3)
        NewBag: (1, 2, 3)

        NOT CONSERVATIVE
        IDEMPOTENT self-evident
        """
        return Bag([x for x in self._v])

    def sort(self) -> None:
        """
        BEFORE
        Bag: (3, 1, 2)

        AFTER
        Bag: (1, 2, 3)

        CONSERVATIVE
        IDEMPOTENT on self
        """
        self._v.sort()

    def pop_duplicates(self) -> Bag[T]:
        """
        BEFORE
        self: (1, 2, 2, 3, 3, 3)

        AFTER
        self:    (1, 2, 3)
        output:  (2, 3, 3)

        CONSERVATIVE
        IDEMPOTENT on self
        """
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
        """
        BEFORE
        self:  (1, 2, 3)
        other: (2, 3, 4)

        AFTER
        self:  ()
        other: (1, 2, 3, 2, 3, 4)

        CONSERVATIVE
        IDEMPOTENT self evident
        """
        other._v = self._v + other._v
        self._v = []

    def count(self) -> Counter[T]:
        """
        Bag:    ("a", "b", "b")
        Output: {"a": 1, "b": 2}

        CONSERVATIVE
        IDEMPOTENT self evident
        """
        return Counter(self._v)
