from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255)) # Увеличено для хранения хэша
    role = db.Column(db.String(20))
    telegram_id = db.Column(db.String(50), nullable=True)

class Product(db.Model):
    sku = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100))

class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    arrival_date = db.Column(db.String(20))
    sku = db.Column(db.String(50), db.ForeignKey('product.sku'))
    quantity = db.Column(db.Integer)
    status = db.Column(db.String(20), default="In Transit")

class PreOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sku = db.Column(db.String(50), db.ForeignKey('product.sku'))
    quantity = db.Column(db.Integer)
    status = db.Column(db.String(20))