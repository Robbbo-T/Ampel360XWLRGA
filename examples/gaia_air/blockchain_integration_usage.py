import json
import hashlib
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # Optional: store flagged issues or alerts in a separate list
        self.alerts = []

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new block and add it to the chain.
        """
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
        """
        Creates a new transaction to go into the next mined block.
        Metadata can store additional information, such as:
        - Type of fuel additive
        - Corrosion readings or sensor data
        - Observed risk levels
        """
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
        """
        Hashes a block using SHA-256.
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        Returns the last block in the chain.
        """
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work:
        - Find a number p' such that hash(p || p') contains leading 4 zeros.
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeros?
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def analyze_data(self):
        """
        Example analytics function to detect correlations.
        This could be replaced by more sophisticated machine learning models
        or advanced statistical analysis.
        """
        flagged = []
        # Here, we simulate detection of correlation:
        # For instance, check metadata where 'fuel_additive' is associated
        # with 'high_corrosion' or any other critical parameter.
        for tx in self.current_transactions:
            metadata = tx.get('metadata', {})
            if metadata.get('fuel_additive') == 'ADDITIVE_X' and metadata.get('risk_level') == 'HIGH':
                flagged.append(tx)

        # If flagged, we might store them in a separate structure for alerts
        if flagged:
            self.alerts.extend(flagged)
        return flagged

app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    """
    Mines a new block, awarding 1 coin (or token) to the miner node.
    """
    last_block = blockchain.last_block
    last_proof = last_block['proof']

    # Proof of Work algorithm
    proof = blockchain.proof_of_work(last_proof)

    # The miner is awarded 1 coin (sender is "0" to denote new coin)
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    # Forge the new Block by adding it to the chain
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
    """
    Creates a new transaction and adds it to the list of current transactions.
    Expects JSON data in the form: 
    {
        "sender": "...",
        "recipient": "...",
        "amount": ...,
        "metadata": { "fuel_additive": "...", "risk_level": "..." }
    }
    """
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']

    if not values or not all(k in values for k in required):
        return 'Missing values', 400

    # Optional metadata can contain additional analytics fields
    metadata = values.get('metadata', {})

    index = blockchain.new_transaction(
        sender=values['sender'],
        recipient=values['recipient'],
        amount=values['amount'],
        metadata=metadata
    )

    # Run a quick analysis right after storing the transaction
    flagged_instances = blockchain.analyze_data()

    # If flagged instances found, we can respond or proceed with an alert system
    if flagged_instances:
        message = (f'Transaction added to Block {index}. '
                   f'ALERT: Correlation detected in metadata! Possible risk flagged.')
    else:
        message = f'Transaction will be added to Block {index}.'

    response = {'message': message}
    return jsonify(response), 201

@app.route('/sync', methods=['POST'])
def sync_data():
    """
    Endpoint for automated data module synchronization.
    External modules can POST periodic or event-driven updates here.
    Example JSON:
    {
        "module_id": "SensorModule01",
        "updates": [
            { "fuel_additive": "ADDITIVE_X", "risk_level": "HIGH" },
            { "fuel_additive": "ADDITIVE_Y", "risk_level": "LOW" }
        ]
    }
    """
    values = request.get_json()
    if not values or 'updates' not in values:
        return 'Invalid sync data', 400

    module_id = values.get('module_id', 'UnknownModule')
    updates = values['updates']

    # We can bundle these updates into transactions
    for update in updates:
        # The metadata might contain sensor or operational data
        metadata = {
            'fuel_additive': update.get('fuel_additive'),
            'risk_level': update.get('risk_level'),
            'module_id': module_id
        }
        blockchain.new_transaction(
            sender=module_id,
            recipient="AnalyticsEngine",
            amount=0,  # Not a monetary transaction, just a data log
            metadata=metadata
        )
    
    # Analyze immediately after synchronization
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
    """
    Returns the entire blockchain, including alerts if desired.
    """
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        'alerts': blockchain.alerts  # Optional: exposing flagged alerts
    }
    return jsonify(response), 200

if __name__ == '__main__':
    # In production, you might use a more robust server (e.g., Gunicorn) 
    # and handle SSL, load balancing, etc.
    app.run(host='0.0.0.0', port=5000)
