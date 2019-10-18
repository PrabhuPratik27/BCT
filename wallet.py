from fastecdsa import keys,curve
import os.path

def generate_keys():
    priv_key = keys.gen_private_key(curve.secp256k1)
    pub_key = keys.get_public_key(priv_key,curve.secp256k1)
    keys.export_key(priv_key,curve=curve.secp256k1,filepath='./priv_key.key')
    keys.export_key(pub_key,curve=curve.secp256k1,filepath='./pub_key.pub')

if (not os.path.exists('./pub_key.pub')):
    if (not os.path.exists('./priv_key.key')):
        generate_keys()
else:
    print("Keys hai abhi kaam hoga")