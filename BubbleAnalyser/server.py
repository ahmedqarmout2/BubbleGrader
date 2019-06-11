#!flask/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/ping', methods=['GET'])
def ping():
    return jsonify({'ping': 'msg'})

if __name__ == '__main__':
    app.run()