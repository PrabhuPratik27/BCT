from fastecdsa import keys,curve,ecdsa
import os.path
import requests

m="This is a message"

def generate_keys():
    priv_key = keys.gen_private_key(curve.secp256k1)
    pub_key = keys.get_public_key(priv_key,curve.secp256k1)
    keys.export_key(priv_key,curve=curve.secp256k1,filepath='./priv_key.key')
    keys.export_key(pub_key,curve=curve.secp256k1,filepath='./pub_key.pub')

def mine():
    priv_key, q = keys.import_key('./priv_key.key')
    r, s = ecdsa.sign(m, priv_key, curve=curve.secp256k1)

    files={'pub_key': open('./pub_key.pub','rb')}
    values={'r': r, 's': s}

    r = requests.post('http://localhost:5000/mine', files=files, data=values)
    print(r.text)

def transaction():
    priv_key, q = keys.import_key('./priv_key.key')
    r, s = ecdsa.sign(m, priv_key, curve=curve.secp256k1)

    print("Enter the file to public key of recipient")
    file = input()

    print("Enter the amount to send")
    amount = int(input())

    files = {'sender': open('./pub_key.pub','rb'), 'recipient': open(file + '/pub_key.pub','rb')}
    values={'r': r, 's': s, 'amount': amount}

    r = requests.post('http://localhost:5000/transactions/new', files=files, data=values)
    print(r.text)

def balance():
    files={'pub_key': open('./pub_key.pub','rb')}

    r = requests.post('http://localhost:5000/balance', files=files)
    print(r.text)

if (not os.path.exists('./pub_key.pub')):
    if (not os.path.exists('./priv_key.key')):
        generate_keys()
print("Keys hai abhi kaam hoga")
while (True):
    print("1 for mining")
    print("2 for transactions")
    print("3 for balance")
    print("4 to exit")
    k = int(input())
    if (k==1):
        mine()
    elif (k==2):
        transaction()
    elif (k==3):
        balance()
    elif (k==4):
        exit()
    else:
        print("Bhai number to sahi daal")
            
