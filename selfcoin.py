from time import time
import hashlib
import json
from flask import Flask,request,jsonify
from fastecdsa.keys import import_key
from fastecdsa import curve,ecdsa
from fastecdsa.point import Point
from werkzeug.utils import secure_filename
import os

SENDER_UPLOAD_FOLDER = './uploads/sender'
RECIPIENT_UPLOAD_FOLDER = './uploads/recipient'
m="This is a message"

class Blockchain:

    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.utxo = {}
        self.add_block("0")
    
    @staticmethod
    def hash(block_string):
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount,r,s):
        ts = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "r": r,
            "s": s
        }
        self.current_transactions.append(ts)
        return self.last_block["index"] + 1

    def balance(self,pub_key):
        if (pub_key in self.utxo.keys()):
            return self.utxo[pub_key]
        else:
            return 0
    
    def proof_of_work(self,index,time,previous_hash):
        proof = 0
        while True:
            header = f'{index}{time}{previous_hash}{proof}'
            header_hash = self.hash(header.encode())
            if(header_hash[:4] == "0000"):
                return proof,header_hash
            proof+=1

    def verify_transactions(self):
        verified_transactions = []

        for transaction in self.current_transactions:
            r=transaction["r"]
            s=transaction["s"]
            pub_key = transaction["sender"]
            pub_key_receiver = transaction["recipient"]
            amount = transaction["amount"]

            if(pub_key == Point.IDENTITY_ELEMENT ):
                verified_transactions.append(transaction)
                if(pub_key_receiver.x in self.utxo.keys()):
                    self.utxo[pub_key_receiver.x] += amount
                else:
                    self.utxo[pub_key_receiver.x] = amount
            else:
                valid = ecdsa.verify((r, s), m, pub_key, curve=curve.secp256k1)
                if(valid):
                    verified_transactions.append(transaction)
                    if(pub_key_receiver.x in self.utxo.keys()):
                        self.utxo[pub_key_receiver.x] += amount
                        self.utxo[pub_key.x] -= amount
                    else:
                        self.utxo[pub_key_receiver.x] = amount
                        self.utxo[pub_key.x] -= amount

        return verified_transactions


    def add_block(self,previous_hash):
        timestamp = time()
        index = len(self.chain) +1

        verified_transactions = self.verify_transactions()

        proof,block_hash = self.proof_of_work(index,timestamp,previous_hash)

        block = {
            "index": index,
            "timestamp": timestamp,
            "transactions": verified_transactions,
            "proof": proof,
            "block_hash": block_hash,
            "previous_hash": previous_hash
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    

app = Flask(__name__)
app.config['SENDER_UPLOAD_FOLDER'] = SENDER_UPLOAD_FOLDER
app.config['RECIPIENT_UPLOAD_FOLDER']  = RECIPIENT_UPLOAD_FOLDER

blockchain = Blockchain()

@app.route('/mine',methods=['POST'])
def mine():
    if 'pub_key' not in request.files:
        return 'Missing Values', 400

    if 'r' not in request.form:
        return 'Missing Values', 400

    if 's' not in request.form:
        return 'Missing Values', 400

    pub_key = request.files['pub_key']
    filename = secure_filename(pub_key.filename)
    pub_key.save(os.path.join(app.config['SENDER_UPLOAD_FOLDER'], filename))

    parsed_d_miner, pub_key_miner = import_key('./uploads/sender/' + filename)
    os.system('rm -rf ./uploads/sender/' + filename)

    r = int(request.form.get("r"))
    s = int(request.form.get("s"))

    previous_hash = blockchain.last_block["block_hash"]

    blockchain.new_transaction(sender=Point.IDENTITY_ELEMENT ,recipient=pub_key_miner,amount=100,r=r,s=s)

    block = blockchain.add_block(previous_hash)

    response = {
        "message": "Block is created",
        "index": block['index'],
        "proof": block['proof'],
        "block_hash": block['block_hash'],
        "previous_hash" : block['previous_hash']
    }

    return jsonify(response),200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    if 'amount' not in request.form:
        return 'Missing Values', 400

    if 'r' not in request.form:
        return 'Missing Values', 400

    if 's' not in request.form:
        return 'Missing Values', 400

    if 'sender' not in request.files:
        return 'Missing Values', 400

    if 'recipient' not in request.files:
        return 'Missing Values', 400

    amount = int(request.form.get("amount"))
    print(amount)

    r = int(request.form.get("r"))
    s = int(request.form.get("s"))

    sender = request.files['sender']
    recipient = request.files['recipient']

    filename_sender = secure_filename(sender.filename)
    sender.save(os.path.join(app.config['SENDER_UPLOAD_FOLDER'], filename_sender))

    filename_recipient = secure_filename(recipient.filename)
    recipient.save(os.path.join(app.config['RECIPIENT_UPLOAD_FOLDER'], filename_recipient))

    parsed_d_sender, pub_key_sender = import_key('./uploads/sender/' + filename_sender)
    parsed_d_recipient, pub_key_recipient = import_key('./uploads/recipient/' + filename_recipient)


    os.system('rm -rf ./uploads/sender/' + filename_sender)
    os.system('rm -rf ./uploads/recipient/' + filename_recipient)

    balance = blockchain.balance(pub_key_sender.x)

    if (balance < amount):
        return 'Nikal Lavde Pehli Fursat Mein Nikal', 400

    index = blockchain.new_transaction(pub_key_sender,pub_key_recipient,amount,r,s)
    
    response = {
        'message': f'Block #{index}'
        }
    # response = {
    #     'message': "done"
    # }
    return jsonify(response), 201

@app.route('/balance',methods=['POST'])
def balance():
    if 'pub_key' not in request.files:
        return 'Missing Values', 400

    pub_key = request.files['pub_key']
    filename = secure_filename(pub_key.filename)
    pub_key.save(os.path.join(app.config['SENDER_UPLOAD_FOLDER'], filename))

    parsed_d_miner, pub_key_miner = import_key('./uploads/sender/' + filename)
    os.system('rm -rf ./uploads/sender/' + filename)
    
    balance = blockchain.balance(pub_key_miner.x)

    response = {
        "balance": balance
    }

    return jsonify(response), 201

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('-p','--port',default=5000,type=int,help='port num')

    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0',port=port,debug=True)