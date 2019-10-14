from fastecdsa import keys,curve

def generate_keys():
    priv_key, pub_key = keys.gen_keypair(curve.secp256k1)
    keys.export_key(priv_key,curve=curve.secp256k1,filepath='./priv_key.key')
    keys.export_key(pub_key,curve=curve.secp256k1,filepath='./pub_key.pub')

generate_keys()