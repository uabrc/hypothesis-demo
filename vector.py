from __future__ import annotations

"""
An implementation of a pure integer vector. Contains only the binary operations
necessary to meet the arithmetic operation properties of a vector, i.e., vector
addition, scalar multiplication, negation.

Also has a method to rotate clockwise 90 degrees for convenience in producing
perpendicular vectors.

The dot product is also available.

Properties of interest are primarily arithmetic: commutativity, associativity,
distributivity, identity.
"""


class Vector2:
    def __init__(self, _x: int, _y: int, /) -> None:
        self._x = _x
        self._y = _y

    def __str__(self) -> str:
        return f"({self._x},{self._y})"

    def __repr__(self) -> str:
        return f"Vector2({self.__str__()})"

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self._x + other._x, self._y + other._y)

    def __radd__(self, other: Vector2) -> Vector2:
        return other + self

    def __mul__(self, scalar: int) -> Vector2:
        return Vector2(scalar * self._x, scalar * self._y)

    def __rmul__(self, scalar: int) -> Vector2:
        return Vector2(self._x * scalar, self._y * scalar)

    def __neg__(self) -> Vector2:
        return Vector2(-self._x, -self._y)

    def __eq__(self, other: Vector2) -> bool:
        return (self._x == other._x) and (self._y == other._y)

    def rot90cw(self) -> Vector2:
        return Vector2(self._y, -self._x)

    @classmethod
    def zero(cls) -> Vector2:
        return cls(0, 0)


def dot(lhs: Vector2, rhs: Vector2) -> int:
    return (lhs._x * rhs._x) + (lhs._y * rhs._y)
