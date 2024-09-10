import unittest

from hypothesis import given
from hypothesis.strategies import composite, integers

from vector import Vector2, dot


@composite
def vector2s(draw) -> Vector2:
    return Vector2(draw(integers()), draw(integers()))


class test_Vector2(unittest.TestCase):
    @given(vector2s(), vector2s())
    def test_additive_vector_commutativity(self, P, Q):
        self.assertEqual(P + Q, Q + P)

    @given(vector2s(), vector2s(), vector2s())
    def test_additive_vector_associativity(self, P, Q, R):
        self.assertEqual((P + Q) + R, P + (Q + R))

    @given(vector2s())
    def test_additive_vector_identity(self, P):
        self.assertEqual(P + Vector2.zero(), P)

    @given(vector2s())
    def test_additive_vector_invertability(self, P):
        self.assertEqual(P + (-P), Vector2.zero())

    @given(vector2s(), vector2s(), integers())
    def test_additive_vector_distributivity(self, P, Q, s):
        self.assertEqual(s * (P + Q), (s * P) + (s * Q))

    @given(vector2s(), integers(), integers())
    def test_additive_scalar_distributivity(self, P, s, t):
        self.assertEqual((s + t) * P, (s * P) + (t * P))

    @given(vector2s(), integers(), integers())
    def test_additive_scalar_associativity(self, P, s, t):
        self.assertEqual(s * (t * P), (s * t) * P)

    @given(vector2s())
    def test_multiplicative_scalar_identity(self, P):
        self.assertEqual(1 * P, P)

    @given(vector2s())
    def test_rotation_half_cycle(self, P):
        self.assertEqual(P.rot90cw().rot90cw(), -P)

    @given(vector2s())
    def test_rotation_full_cycle(self, P):
        self.assertEqual(P.rot90cw().rot90cw().rot90cw().rot90cw(), P)


class test_dot(unittest.TestCase):
    @given(vector2s(), vector2s())
    def test_vector_commutativity(self, P, Q):
        self.assertEqual(dot(P, Q), dot(Q, P))

    @given(vector2s(), vector2s(), vector2s())
    def test_vector_distributivity(self, P, Q, R):
        self.assertEqual(dot(P, (Q + R)), dot(P, Q) + dot(P, R))

    @given(vector2s(), vector2s(), integers())
    def test_scalar_commutativity(self, P, Q, s):
        self.assertEqual(s * dot(P, Q), dot(s * P, Q))

    @given(vector2s())
    def test_identity(self, P):
        self.assertEqual(dot(P, Vector2.zero()), 0)

    @given(vector2s())
    def test_perpendicular_nullity(self, P):
        self.assertEqual(dot(P, P.rot90cw()), 0)
