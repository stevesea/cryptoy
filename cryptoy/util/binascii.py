from base64 import (
    a85decode,
    a85encode,
    b16decode,
    b16encode,
    b32decode,
    b32encode,
    b85decode,
    b85encode,
    standard_b64decode,
    standard_b64encode,
    urlsafe_b64decode,
    urlsafe_b64encode,
)
from typing import Callable, Dict

encodings: Dict[str, Callable] = {
    "a85": a85encode,
    "b16": b16encode,
    "b32": b32encode,
    "b64": standard_b64encode,
    "b64url": urlsafe_b64encode,
    "b85": b85encode,
}


def my_b16decode(s: str) -> bytes:
    """b16decode, but allow lowercase alphabet"""
    return b16decode(s, casefold=True)


def my_b32decode(s: str) -> bytes:
    """b32decode, but allow lowercase alphabet"""
    return b32decode(s, casefold=True)


decodings: Dict[str, Callable] = {
    "a85": a85decode,
    "b16": my_b16decode,
    "b32": my_b32decode,
    "b64": standard_b64decode,
    "b64url": urlsafe_b64decode,
    "b85": b85decode,
}


def b2a(data: bytes, encoding: str = None) -> str:
    """convert binary data to printable characters using given encoding.

    >>> b2a(b"test","b64")
    'dGVzdA=='

    If no encoding supplied, bytes are decoded as UTF-8.
    >>> b2a(b"test")
    'test'
    """
    if encoding is None:
        return data.decode("utf-8")
    else:
        return encodings[encoding](data).decode("utf-8")


def a2b(s: str, encoding: str = None) -> bytes:
    """convert the given encoded string to bytes.

    >>> a2b("dGVzdA==", "b64")
    b'test'
    >>> a2b("dGVzdA==")
    b'dGVzdA=='
    """
    if encoding is None:
        return s.encode("utf-8")
    else:
        return decodings[encoding](s)
