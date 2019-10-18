from fastecdsa.keys import import_key
from fastecdsa import curve,ecdsa

m="This is a message"

priv_key , parsed_q = import_key('./priv_key.key')
parsed_d, pub_key = import_key('./pub_key.pub')

r, s = ecdsa.sign(m, priv_key, curve=curve.secp256k1)

print(r)
print(s)

valid = ecdsa.verify((r, s), m, pub_key, curve=curve.secp256k1)

print(valid)