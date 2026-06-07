import os
from flask import Flask, render_template, request, redirect, session, url_for, flash
from dotenv import load_dotenv
from database import db, User, Product, Supply, PreOrder
from modules.inventory import InventoryModule
from modules.orders import OrderModule
from modules.identity import IdentityModule


load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///warehouse.db"
app.secret_key = os.getenv("SECRET_KEY", "fallback_default_key_if_env_missing")
db.init_app(app)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="client").first():
        hashed_pw = IdentityModule.hash_password("password123")
        db.session.add(
            User(username="client", password=hashed_pw, role="client", telegram_id="")
        )
    if not User.query.filter_by(username="admin").first():
        hashed_pw = IdentityModule.hash_password("admin123")
        db.session.add(
            User(username="admin", password=hashed_pw, role="manager", telegram_id="")
        )
    if not Product.query.first():
        db.session.add(Product(sku="IPHONE15", name="Apple iPhone 15"))
        db.session.add(Product(sku="MACBOOK", name="MacBook Pro M3"))
    db.session.commit()


@app.route("/")
def index():
    if "user_id" in session:
        if session["role"] == "manager":
            return redirect(url_for("admin_dashboard"))
        return redirect(url_for("client_dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]  # Извлечение пароля из формы

        user = IdentityModule.authenticate(username, password)
        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            return redirect(url_for("index"))
        else:
            flash("Ошибка: Неверный логин или пароль.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "manager":
        return "Доступ запрещен. Требуются права менеджера.", 403
    supplies = Supply.query.all()
    orders = PreOrder.query.all()
    products = Product.query.all()
    return render_template(
        "admin.html", supplies=supplies, orders=orders, products=products
    )


@app.route("/add_supply", methods=["POST"])
def add_supply():
    if session.get("role") == "manager":
        InventoryModule.add_supply(
            request.form["sku"], int(request.form["qty"]), request.form["date"]
        )
    return redirect(url_for("admin_dashboard"))


@app.route("/receive/<int:id>")
def receive(id):
    if session.get("role") == "manager":
        InventoryModule.receive_supply(id)
    return redirect(url_for("admin_dashboard"))


@app.route("/client")
def client_dashboard():
    if session.get("role") != "client":
        return "Доступ запрещен. Вы не являетесь клиентом.", 403

    user = User.query.get(session["user_id"])  # Получаем текущего юзера
    my_orders = PreOrder.query.filter_by(user_id=session["user_id"]).all()
    products = Product.query.all()
    return render_template(
        "client.html", orders=my_orders, products=products, user=user
    )


@app.route("/update_tg", methods=["POST"])
def update_tg():
    if session.get("role") == "client":
        user = User.query.get(session["user_id"])
        user.telegram_id = request.form["tg_id"]
        db.session.commit()
        flash("Telegram ID успешно сохранен.")
    return redirect(url_for("client_dashboard"))


@app.route("/make_order", methods=["POST"])
def make_order():
    if session.get("role") == "client":
        success, msg = OrderModule.create_preorder(
            session["user_id"], request.form["sku"], request.form["qty"]
        )
        flash(msg)

    return redirect(url_for('client_dashboard'))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    return redirect(url_for("client_dashboard"))

