from utilities.database_utilities import JWT_SECRET_KEY
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from datetime import timedelta, datetime
from database import get_connection
from models import Users, Cards, Fees
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from singleton import UFE
import random
import pandas as pd

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

with Session(get_connection()) as session:
    session.begin()

@app.route('/login/<username>/<password>', methods=['POST'])
def login(username, password):
    
    users = pd.read_sql(sql=select(Users), con=get_connection())

    if ((users['username'] != username) | (users['hashed_password'] != password)).any():
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/create_card/<balance>', methods=['POST'])
@jwt_required()
def create_card(balance):
    card_number = str(random.randint(100000000000000, 999999999999999))
    session.add(Cards(card_number=card_number, balance=balance))
    session.commit()
    return jsonify({"card_number": card_number,
                    "balance": balance}), 201

@app.route('/pay/<card_number>', methods=['POST'])
@jwt_required()
def pay(card_number):
    cards = pd.read_sql(sql=select(Cards), con=get_connection())
    amount = int(random.randint(100, 999))

    if ((cards['card_number'] != card_number).all()):
        return jsonify({"error": "Card not found"}), 404

    fee = validate_ufe()
    total_fee = amount * fee
    total_amount = amount + total_fee

    
    intial_balance = float(cards.loc[cards['card_number'] == card_number, 'balance'].values[0])
    final_balance = round(float(intial_balance - total_amount), 1)
    stmt = (update(Cards).where(Cards.card_number == card_number).values(balance=final_balance))
    session.execute(stmt)
    session.commit()

    return jsonify({"card_number": card_number, "amount_paid": amount, "total_amount_deducted": total_amount, "fee": fee}), 200

@app.route('/get_balance/<card_number>', methods=['GET'])
@jwt_required()
def get_balance(card_number):
    cards = pd.read_sql(sql=select(Cards), con=get_connection())

    if ((cards['card_number'] != card_number).all()):
        return jsonify({"error": "Card not found"}), 404

    balance = cards.loc[cards['card_number'] == card_number, 'balance'].values[0]
    return jsonify({"card_number": card_number, "balance": balance}), 200

def validate_ufe():
    calc = UFE()
    fees = pd.read_sql(sql=select(Fees), con=get_connection())
    ufe = fees['fee'][0]
    ahora = datetime.now()
    
    if ahora.minute == 0:
        new_ufe = round(random.uniform(0, 2), 1)
        get_ufe = calc.calculate_ufe(ufe, new_ufe)
        stmt = (update(Fees).values(fee=float(get_ufe)))
        session.execute(stmt)
        session.commit()
        
        return get_ufe
    
    else:

        return ufe

if __name__ == '__main__':
    app.run(port=5001)