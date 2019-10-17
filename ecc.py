from fastecdsa import keys, curve

"""The reason there are two ways to generate a keypair is that generating the public key requires
a point multiplication, which can be expensive. That means sometimes you may want to delay
generating the public key until it is actually needed."""

# generate a keypair (i.e. both keys) for curve P256
priv_key_1, pub_key_1 = keys.gen_keypair(curve.P256)

# generate a private key for curve P256
priv_key_2 = keys.gen_private_key(curve.P256)

# get the public key corresponding to the private key we just generated
pub_key_2 = keys.get_public_key(priv_key_2, curve.P256)

print(priv_key_1)
print(priv_key_2)

priv_key_3 = keys.gen_private_key(curve.P256)

print(priv_key_3)