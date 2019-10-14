from fastecdsa import keys,curve,ecdsa

priv_key, pub_key = keys.gen_keypair(curve.secp256k1)

parsed_d_1, parsed_Q_1 = keys.import_key('./priv_key.key')

parsed_d_2, parsed_Q_2 = keys.import_key('./pub_key.pub')

print(parsed_d_1)
print(parsed_Q_1)
print(parsed_d_2)
print(parsed_Q_2)

m = 'This is a message'

r, s = ecdsa.sign(m, parsed_d_1, curve=curve.secp256k1)

print(ecdsa.verify((r, s), m,parsed_Q_2, curve=curve.secp256k1))