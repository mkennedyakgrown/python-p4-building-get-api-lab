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
    bakeries = Bakery.query.all()
    body = [bakery_to_dict(b) for b in bakeries]

    return make_response(body, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    return bakery_to_dict(bakery)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(desc('price')).all()
    return [baked_good_to_dict(bg) for bg in baked_goods]

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    return baked_good_to_dict(BakedGood.query.order_by(desc('price')).first())

def bakery_to_dict(b):
    return {
        "baked_goods": [{
            "bakery_id": bg.bakery_id,
            "created_at": bg.created_at,
            "id": bg.id,
            "name": bg.name,
            "price": bg.price,
            "updated_at": bg.updated_at
        } for bg in b.baked_goods],
        "created_at": b.created_at,
        "id": b.id,
        "name": b.name,
        "updated_at": b.updated_at
    }

def baked_good_to_dict(bg):
    bg_dict = {
        "bakery_id": bg.bakery_id,
        "created_at": bg.created_at,
        "id": bg.id,
        "name": bg.name,
        "price": bg.price,
        "updated_at": bg.updated_at
    }
    if bg.bakery:
        bg_dict["bakery"] = {
            "created_at": bg.bakery.created_at,
            "id": bg.bakery.id,
            "name": bg.bakery.name,
            "updated_at": bg.bakery.updated_at
        }
    return bg_dict

if __name__ == '__main__':
    app.run(port=5555, debug=True)
