import cryptoy.encodings as ce


def test_b2a():
    assert ce.b2a(b"test", "b64") == "dGVzdA=="
    assert ce.b2a(b"test") == "test"


def test_a2b():
    assert ce.a2b("dGVzdA==", "b64") == b"test"
    assert ce.a2b("dGVzdA==") == b"dGVzdA=="


def test_roundtrip():
    for enc in ce.encodings:
        val = b"test"
        encval = ce.b2a(val, enc)
        assert ce.a2b(encval, enc) == val
