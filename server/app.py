#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    body = [b.to_dict() for b in Bakery.query.all()]

    return make_response(body, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    return Bakery.query.filter_by(id=id).first().to_dict()

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    return [bg.to_dict() for bg in BakedGood.query.order_by(desc('price')).all()]

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    return BakedGood.query.order_by(desc('price')).first().to_dict()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
