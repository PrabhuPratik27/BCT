from fastecdsa.keys import import_key
from fastecdsa import curve,ecdsa
from flask import Flask,request,jsonify

m="This is a message"

app = Flask(__name__)

@app.route('/check',methods=['POST'])
def check():
    r = int(request.form.get("r"))
    s = int(request.form.get("s"))
    print(r,s)

    parsed_d, pub_key = import_key('./pub_key.pub')

    valid = ecdsa.verify((r, s), m, pub_key, curve=curve.secp256k1)
    
    response = {
        'message': valid
    }
    return jsonify(response), 201

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('-p','--port',default=5000,type=int,help='port num')

    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0',port=port,debug=True)