from time import time
import hashlib
import json
from flask import Flask,request,jsonify
from fastecdsa import keys, curve

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

    def new_transaction(self, sender, recipient, amount):
        ts = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        }
        self.current_transactions.append(ts)
        return self.last_block["index"] + 1
    
    def proof_of_work(self,index,time,previous_hash):
        proof = 0
        while True:
            header = f'{index}{time}{previous_hash}{proof}'
            header_hash = self.hash(header.encode())
            if(header_hash[:4] == "0000"):
                return proof,header_hash
            proof+=1

    def add_block(self,previous_hash):
        timestamp = time()
        index = len(self.chain) +1

        proof,block_hash = self.proof_of_work(index,timestamp,previous_hash)

        block = {
            "index": index,
            "timestamp": timestamp,
            "transactions": self.current_transactions,
            "proof": proof,
            "block_hash": block_hash,
            "previous_hash": previous_hash
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    

app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine',methods=['GET'])
def mine():
    previous_hash = blockchain.last_block["block_hash"]

    blockchain.new_transaction(sender='0',recipient='1',amount=20)

    block = blockchain.add_block(previous_hash)

    response = {
        "message": "Block is created",
        "index": block['index'],
        "transactions": block['transactions'],
        "proof": block['proof'],
        "block_hash": block['block_hash'],
        "previous_hash" : block['previous_hash']
    }

    return jsonify(response),200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return 'Missing Values', 400
    
    sender = values['sender']
    recipient = values['recipient']
    amount = values['amount']
    index = blockchain.new_transaction(sender,
                        recipient,amount)
    
    response = {
        'message': f'Block #{index}'
        }
    return jsonify(response), 201

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('-p','--port',default=5000,type=int,help='port num')

    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0',port=port,debug=True)