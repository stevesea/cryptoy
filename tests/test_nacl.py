from cryptoy.nacl import EncryptingKeyPair


def test_keypair_gen():
    kp = EncryptingKeyPair.generate()

    asjson = kp.to_json()

    asdict = kp.to_dict()

    assert EncryptingKeyPair.from_json(asjson) == kp
    assert EncryptingKeyPair.from_dict(asdict) == kp
