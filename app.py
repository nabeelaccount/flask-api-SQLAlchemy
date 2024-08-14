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
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String, unique=True, nullable=False, default=str(uuid.uuid4()))
    amount = db.Column(db.Numeric, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def json(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'amount': str(self.amount),
            'timestamp': self.timestamp.isoformat()
        }

# Creating table for the 'transactions' table
with app.app_context():
    db.create_all()


# Post data
@app.route("/api/transaction", methods=['POST'])
def create_transaction():
    data = request.get_json()

    # Generate a unique transaction_id if not provided
    transaction_id = data.get("transactionId") or str(uuid.uuid4())
    amount = data["amount"]
    timestamp = data.get("timestamp") or datetime.utcnow().isoformat()

    # Convert timestamp to a datetime object
    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

    # Create a new Transaction object and add it to the session
    transaction = Transaction(transaction_id=transaction_id, amount=amount, timestamp=timestamp)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"id": transaction.id, "message": f"Transaction {transaction.transaction_id} created at {timestamp}."}), 201

@app.route("/api/all", methods=['POST'])
def get_transaction():
    data = request.get_json()

    transactions = Transaction.query.all()
    return jsonify([transaction.json() for transaction in transactions]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)