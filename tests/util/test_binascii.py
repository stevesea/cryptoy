from cryptoy.util import binascii


def test_roundtrip():
    for enc in binascii.encodings:
        val = b"test"
        encval = binascii.b2a(val, enc)
        assert binascii.a2b(encval, enc) == val
