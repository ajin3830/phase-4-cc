from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
                        # many-many plural, join table
    serialize_rules = ('-restaurants.pizzas', '-restaurant_pizzas')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza')
    #association
    restaurants = association_proxy('restaurant_pizzas', 'restaurant')

    def __repr__(self):
        return f'<Pizza {self.name} />'

class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
                        # many-many plural, join table
    serialize_rules = ('-pizzas.restaurants', '-restaurant_pizzas')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    #relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', backref="restaurant")
    #association
    pizzas = association_proxy('restaurant_pizzas', 'pizza')

    def __repr__(self):
        return f'<Restaurant {self.name} />'

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'
                        # one-many
    serialize_rules = ('-pizza.restaurants', '-restaurant.pizzas')

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #relationship columns
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    @validates('price')
    def validate_price(self, key, price):
        if not price or not 1 <= price <= 30:
        # if price < 1 or price > 30:
            raise ValueError('must have a price between 1 and 30')
        return price

    def __repr__(self):
        return f'<RestaurantPizza {self.price} />'
 