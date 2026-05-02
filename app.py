from flask import Flask, render_template, request, redirect
from database import db, User, Product, Supply, PreOrder
from modules.inventory import InventoryModule
from modules.orders import OrderModule

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
db.init_app(app)

# Инициализация БД и первичных данных
with app.app_context():
    db.create_all()
    if not User.query.first():
        db.session.add(User(username="Ivan_Client", role="client"))
        db.session.add(User(username="Manager_Alex", role="manager"))
        db.session.add(Product(sku="IPHONE15", name="Apple iPhone 15"))
        db.session.commit()

@app.route('/')
def index():
    return render_template('index.html', 
                           supplies=Supply.query.all(), 
                           orders=PreOrder.query.all(),
                           products=Product.query.all())

@app.route('/add_supply', methods=['POST'])
def add_supply():
    InventoryModule.add_supply(request.form['sku'], int(request.form['qty']), request.form['date'])
    return redirect('/')

@app.route('/make_order', methods=['POST'])
def make_order():
    OrderModule.create_preorder(1, request.form['sku'], request.form['qty']) # ID=1 это Ivan_Client
    return redirect('/')

@app.route('/receive/<int:id>')
def receive(id):
    InventoryModule.receive_supply(id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)