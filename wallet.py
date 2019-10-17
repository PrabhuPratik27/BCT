from fastecdsa import keys,curve

def generate_keys():
    filepath=input()
    priv_key = keys.gen_private_key(curve.secp256k1)
    pub_key = keys.get_public_key(priv_key,curve.secp256k1)
    keys.export_key(priv_key,curve=curve.secp256k1,filepath=filepath+'/priv_key.key')
    keys.export_key(pub_key,curve=curve.secp256k1,filepath=filepath+'/pub_key.pub')

generate_keys()