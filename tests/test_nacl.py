from cryptoy.nacl.box import BoxKeyPair


def test_keypair_gen():
    kp = BoxKeyPair.generate()

    asjson = kp.to_json()

    asdict = kp.to_dict()

    assert BoxKeyPair.from_json(asjson) == kp
    assert BoxKeyPair.from_dict(asdict) == kp
