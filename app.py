from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import datetime
import uuid

app = Flask(__name__)
# Connect to the database using SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# Define the Transaction model
class Transaction(db.Model):
    __tablename__ = 'transactions'

    """
    nullable= you must provide a value when entering a paramater
    unique= must be unique across all other parameters
    default= default value in case one is not provided
    """
    # Auto increment id
    id = db.Column(db.Integer, primary_key=True)
    # Stores the Unique ID and defaults to uuid.uuid4 if one doesn't exist
    transaction_id = db.Column(db.String, unique=True, nullable=False, default=str(uuid.uuid4()))
    # Stores amount. Numeric
    amount = db.Column(db.Numeric, nullable=False)
    # Stores date-time and defaults to current time if not specified.
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def json(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'amount': str(self.amount),
            'timestamp': self.timestamp.isoformat()
        }

# Creating table for the 'transactions' table if it doesn't exist
with app.app_context():
    db.create_all()


# Post data
@app.route("/api/transaction", methods=['POST'])
def create_transaction():
    # Takes incoming JSON
    data = request.get_json()

    # Generate a unique transaction_id if not provided
    transaction_id = data.get("transactionId") or str(uuid.uuid4())
    amount = data["amount"]
    timestamp = data.get("timestamp") or datetime.utcnow().isoformat()

    # Convert timestamp to a datetime within Z
    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

    # Create a new Transaction object and adds and commits it to the database
    transaction = Transaction(transaction_id=transaction_id, amount=amount, timestamp=timestamp)
    db.session.add(transaction)
    db.session.commit()

    # Returns the following message in case of success
    return jsonify({"id": transaction.id, "message": f"Transaction {transaction.transaction_id} created at {timestamp}."}), 201

# Getll all transaction objects
@app.route("/api/all", methods=['POST'])
def get_transaction():
    data = request.get_json()

    # Queries database for all the transactions table records from Transaction object
    transactions = Transaction.query.all()
    # Returns each transaction record in json formate
    return jsonify([transaction.json() for transaction in transactions]), 200

if __name__ == '__main__':
    # Opens to all IP at port 5000
    app.run(host='0.0.0.0', port=5000)