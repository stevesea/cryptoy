"""utility classes for reading/writing libsodium keypairs"""

from dataclasses import dataclass
from typing import Type, TypeVar

from dataclasses_json import dataclass_json
from nacl.public import PrivateKey

from cryptoy.encodings import a2b, b2a

T = TypeVar("T", bound="EncryptingKeyPair")


@dataclass_json
@dataclass
class EncryptingKeyPair:
    """libsodium Curve25519 Keypair."""

    public_key_base64: str
    secret_key_base64: str

    @classmethod
    def generate(cls: Type[T]) -> T:
        """generate a new libsodium Curve25519 Keypair.

        >>> kp = EncryptingKeyPair.generate()
        >>> asjson = kp.to_json()
        >>> kp2 = EncryptingKeyPair.from_json(asjson)
        >>> kp == kp2
        True
        """
        kp = PrivateKey.generate()

        return cls(
            public_key_base64=b2a(bytes(kp.public_key), "b64"),
            secret_key_base64=b2a(bytes(kp), "b64"),
        )

    @classmethod
    def from_secret_key_base64(cls: Type[T], secret_key_base64: str) -> T:
        """generate a new libsodium Curve25519 Keypair.

        >>> kp = EncryptingKeyPair.from_secret_key_base64("pQy+q7cw2YfS0RGfSF8IKqMrZ8/nmVf99pHAdxFJAsI=")
        >>> kp.public_key_base64
        '0HmxBKFksC/sybT7Gqzsmnna4T/wEDVoI/hbC0GyW2c='
        >>> kp.to_dict()
        {'public_key_base64': '0HmxBKFksC/sybT7Gqzsmnna4T/wEDVoI/hbC0GyW2c=', 'secret_key_base64': 'pQy+q7cw2YfS0RGfSF8IKqMrZ8/nmVf99pHAdxFJAsI='}
        >>> kp.to_json()
        '{"public_key_base64": "0HmxBKFksC/sybT7Gqzsmnna4T/wEDVoI/hbC0GyW2c=", "secret_key_base64": "pQy+q7cw2YfS0RGfSF8IKqMrZ8/nmVf99pHAdxFJAsI="}'
        """
        kp = PrivateKey(a2b(secret_key_base64, "b64"))
        return cls(
            public_key_base64=b2a(bytes(kp.public_key), "b64"),
            secret_key_base64=b2a(bytes(kp), "b64"),
        )
