import unittest

from hypothesis import given
from hypothesis.strategies import characters, composite, integers, text

from cryptography import decode, encode, encode_broken, encode_broken_upper_z_only


@composite
def ascii_characters(draw) -> str:
    # https://en.wikipedia.org/wiki/Unicode_character_property
    return draw(
        characters(
            codec="ascii",
            categories=[
                "Lu",
                "Ll",
                "Nd",
                "Pc",
                "Pd",
                "Ps",
                "Pe",
                "Pi",
                "Pf",
                "Po",
                "Sm",
                "Sc",
                "Sk",
                "So",
                "Zs",
                # "Cc", excluded because we only want \n
            ],
            include_characters="\n",
        )
    )


@composite
def ascii_message(draw) -> str:
    return draw(text(ascii_characters()))


class test_cryptography(unittest.TestCase):
    @given(ascii_message(), integers(0, 26))
    def test_roundtrip_identity(self, s, n):
        """
        Working, of course. :)
        """
        self.assertEqual(decode(encode(s, rotate_by=n), rotate_by=n), s)

    @given(ascii_message(), integers(0, 26))
    def test_roundtrip_identity_broken(self, s, n):
        """
        Falsifying example: test_roundtrip_identity_broken(
            # The test always failed when commented parts were varied together.
            self=<cryptography_test.test_cryptography testMethod=test_roundtrip_identity_broken>,
            s='',  # or any other generated value
            n=0,  # or any other generated value
        )

        Note the test found the minimal example.
        """
        self.assertEqual(decode(encode_broken(s, rotate_by=n), rotate_by=n), s)

    @given(ascii_message(), integers(0, 26))
    def test_roundtrip_identity_broken_upper_z_only(self, s, n):
        """
        Falsifying example: test_roundtrip_identity_broken_upper_z_only(
            self=<cryptography_test.test_cryptography testMethod=test_roundtrip_identity_broken_upper_z_only>,
            s='S',
            n=7,
        )

        Note the test didn't quite find the minimal example, but got pretty
        close. It certainly found a broken case. chr(ord("S") + 7) is "Z", which
        gets duplicated.

        """
        self.assertEqual(
            decode(encode_broken_upper_z_only(s, rotate_by=n), rotate_by=n), s
        )
