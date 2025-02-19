#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# GET /restaurants
@app.route('/restaurants', methods=['GET'])
def restaurants():
    restaurants = Restaurant.query.all()
    return make_response([restaurant.to_dict() for restaurant in restaurants], 200)
    
# GET DELETE /restaurants/:id
@app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if not restaurant:
        return make_response({"error": "Restaurant not found"}, 404)
    elif request.method == 'GET':
        return make_response(restaurant.to_dict(), 200)
    elif request.method == 'DELETE':
        db.session.delete(restaurant)
        db.session.commit()
        return make_response('', 200)

# GET /pizzas
@app.route('/pizzas', methods=['GET'])
def pizza():
    pizzas = Pizza.query.all()
    return make_response([pizza.to_dict() for pizza in pizzas], 200)

# POST /restaurant_pizzas
@app.route('/restaurant_pizzas', methods=['POST'])
def restaurant_pizzas():
    try:
        new_rp = RestaurantPizza(
            price=request.get_json(force=True)['price'],
            pizza_id=request.get_json(force=True)['pizza_id'],
            restaurant_id=request.get_json(force=True)['restaurant_id']
        )
        db.session.add(new_rp)
        db.session.commit()

        # pizza = Pizza.query.filter_by(id=new_rp.pizza_id).first()
        return make_response(new_rp.to_dict(rules=('-created_at', '-updated_at')), 201)
    
    except ValueError:
        return make_response({'error': 'Invalid input'}, 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
