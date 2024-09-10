from typing import List

"""
This file encapsulates an ASCII-based, case-agnostic cipher, defaulting to
Rot13. Non-letter characters are left unchanged.

Two broken methods are included that each contain an error, for demonstration
purposes with property-based testing.

For ROT13, the following encoding holds for both upper and lowercase ASCII
letters.

from: ABCDE FGHIJ KLMNO PQRST UVWXY Z
to:   NOPQR STUVW XYZAB CDEFG HIJKL M

Example ---

from: The quick brown fox jumps over the lazy dog.
to:   Gur dhvpx oebja sbk whzcf bire gur ynml qbt.

The primary property of interest is whether the round-trip always equals the input.
"""

ASCII_ALPHABET_SIZE = 26
ROT13 = 13

UPPER_A = 65
UPPER_Z = 90
LOWER_A = 97
LOWER_Z = 122


def encode(_s: str, /, *, rotate_by: int = ROT13) -> str:
    """
    Default is ROT13 Caesar cipher.
    """
    assert _isascii(_s)
    out: List[str] = []
    for c in _s:
        v = ord(c)
        new_v = _shift_letters(v, rotate_by)
        new_c = chr(new_v)
        out.append(new_c)
    return "".join(out)


def decode(_s: str, /, *, rotate_by: int = ROT13) -> str:
    """
    Decodes a message encoded with the same value of "rotate_by".
    """
    assert _isascii(_s)
    out: List[str] = []
    for c in _s:
        v = ord(c)
        new_v = _shift_letters(v, _encode_to_decode_shift_amount(rotate_by))
        new_c = chr(new_v)
        out.append(new_c)
    return "".join(out)


def encode_broken(_s: str, /, *, rotate_by: int = ROT13) -> str:
    return encode(_s, rotate_by=rotate_by) + " "


def encode_broken_upper_z_only(_s: str, /, *, rotate_by: int = ROT13) -> str:
    out = encode(_s, rotate_by=rotate_by)
    out = out.replace("Z", "ZZ")
    return out


def _encode_to_decode_shift_amount(_n: int, /) -> int:
    return (ASCII_ALPHABET_SIZE - _n) % ASCII_ALPHABET_SIZE


def _shift_letters(_c: int, _n: int, /) -> int:
    if UPPER_A <= _c <= UPPER_Z:  # upper
        v = _shift_ord(_c, _n, UPPER_A)
    elif LOWER_A <= _c <= LOWER_Z:  # lower
        v = _shift_ord(_c, _n, LOWER_A)
    else:
        v = _c
    return v


def _shift_ord(_c: int, _n: int, _first_ord: int, /) -> int:
    v = _c
    v = v - _first_ord
    v = (v + _n) % ASCII_ALPHABET_SIZE
    v = v + _first_ord
    return v


def _isascii(_s: str, /) -> bool:
    try:
        _s.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False
