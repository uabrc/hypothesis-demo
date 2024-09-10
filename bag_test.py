import unittest

from hypothesis import given
from hypothesis.strategies import composite, integers, lists

from bag import Bag


@composite
def integer_bags(draw) -> Bag[int]:
    return Bag(draw(lists(integers())))


class test_Bag(unittest.TestCase):
    @given(integer_bags())
    def test_duplicate_equality(self, b0):
        self.assertEqual(b0, b0.duplicate())

    @given(integer_bags())
    def test_sort_equality(self, b0):
        original = b0.duplicate()
        b0.sort()
        self.assertEqual(b0, original)

    @given(integer_bags())
    def test_sort_idempotency(self, b0):
        b0.sort()
        b1 = b0.duplicate()
        b1.sort()
        self.assertEqual(b0, b1)

    @given(integer_bags())
    def test_pop_duplicates_conservancy(self, b0):
        original_b0_count = b0.count()
        duplicates = b0.pop_duplicates()
        self.assertEqual(b0.count() + duplicates.count(), original_b0_count)

    @given(integer_bags())
    def test_pop_duplicates_idempotency(self, b0):
        b0.pop_duplicates()
        b1 = b0.duplicate()
        b1.pop_duplicates()
        self.assertEqual(b0, b1)

    @given(integer_bags(), integer_bags())
    def test_give_all_to_conservancy(self, b0, b1):
        original_b0_count = b0.count()
        original_b1_count = b1.count()
        b0.give_all_to(b1)
        self.assertEqual(b0.count() + b1.count(), original_b0_count + original_b1_count)

    @given(integer_bags())
    def test_give_all_nullity(self, b0):
        b1 = b0.duplicate()
        b0.give_all_to(b1)
        self.assertEqual(len(b0.count()), 0)
