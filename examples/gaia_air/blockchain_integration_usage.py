import json
import hashlib
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
import numpy as np

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.alerts = []

        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount, metadata=None):
        transaction_data = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        }
        if metadata:
            transaction_data['metadata'] = metadata

        self.current_transactions.append(transaction_data)
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def analyze_data(self):
        flagged = []
        for tx in self.current_transactions:
            metadata = tx.get('metadata', {})
            if metadata.get('fuel_additive') == 'ADDITIVE_X' and metadata.get('risk_level') == 'HIGH':
                flagged.append(tx)

        if flagged:
            self.alerts.extend(flagged)
        return flagged

    def optimize_fuel_usage(self, sensor_data):
        # Placeholder for AI-driven fuel management logic
        optimized_fuel_usage = np.mean(sensor_data) * 0.95  # Example: reduce fuel usage by 5%
        return optimized_fuel_usage

    def ai_driven_scheduling(self, tasks):
        # Placeholder for AI-driven scheduling logic
        scheduled_tasks = sorted(tasks, key=lambda x: x['deadline'])
        return scheduled_tasks

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']

    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']

    if not values or not all(k in values for k in required):
        return 'Missing values', 400

    metadata = values.get('metadata', {})

    index = blockchain.new_transaction(
        sender=values['sender'],
        recipient=values['recipient'],
        amount=values['amount'],
        metadata=metadata
    )

    flagged_instances = blockchain.analyze_data()

    if flagged_instances:
        message = (f'Transaction added to Block {index}. '
                   f'ALERT: Correlation detected in metadata! Possible risk flagged.')
    else:
        message = f'Transaction will be added to Block {index}.'

    response = {'message': message}
    return jsonify(response), 201

@app.route('/sync', methods=['POST'])
def sync_data():
    values = request.get_json()
    if not values or 'updates' not in values:
        return 'Invalid sync data', 400

    module_id = values.get('module_id', 'UnknownModule')
    updates = values['updates']

    for update in updates:
        metadata = {
            'fuel_additive': update.get('fuel_additive'),
            'risk_level': update.get('risk_level'),
            'module_id': module_id
        }
        blockchain.new_transaction(
            sender=module_id,
            recipient="AnalyticsEngine",
            amount=0,
            metadata=metadata
        )
    
    flagged_instances = blockchain.analyze_data()
    if flagged_instances:
        message = (f'Data synchronized from {module_id}. '
                   f'Alerts generated for {len(flagged_instances)} issues.')
    else:
        message = f'Data synchronized from {module_id}. No issues flagged.'

    response = {'message': message}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        'alerts': blockchain.alerts
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
