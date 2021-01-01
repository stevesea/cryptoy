from cryptoy.nacl.box import BoxKeyPair


def test_keypair_gen():
    kp = BoxKeyPair.generate()

    asjson = kp.to_json()

    asdict = kp.to_dict()

    assert BoxKeyPair.from_json(asjson) == kp
    assert BoxKeyPair.from_dict(asdict) == kp


def test_keypair_load():
    asdict = {
        "public_key_base64": "0HmxBKFksC/sybT7Gqzsmnna4T/wEDVoI/hbC0GyW2c=",
        "secret_key_base64": "pQy+q7cw2YfS0RGfSF8IKqMrZ8/nmVf99pHAdxFJAsI=",
    }

    kp = BoxKeyPair.from_dict(asdict)
    assert kp.to_dict() == asdict
