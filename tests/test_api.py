import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            from database import db, User
            from modules.identity import IdentityModule
            db.create_all()
            if not User.query.filter_by(username="admin").first():
                admin = User(username="admin", password=IdentityModule.hash_password("admin123"), role="manager", telegram_id="")
                db.session.add(admin)
            if not User.query.filter_by(username="client").first():
                client_user = User(username="client", password=IdentityModule.hash_password("password123"), role="client", telegram_id="")
                db.session.add(client_user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_login_success(client):
    response = client.post("/login", data={"username": "admin", "password": "admin123"})
    assert response.status_code == 302
    with client.session_transaction() as sess:
        assert sess.get("role") == "manager"

def test_login_fail(client):
    response = client.post("/login", data={"username": "admin", "password": "wrong"})
    # ИСПРАВЛЕНО: убрали b'', используем as_text=True
    assert "Ошибка: Неверный логин или пароль" in response.get_data(as_text=True)

def test_admin_dashboard_requires_auth(client):
    response = client.get("/admin")
    assert response.status_code == 403

def test_add_supply_as_manager(client):
    client.post("/login", data={"username": "admin", "password": "admin123"})
    response = client.post("/add_supply", data={"sku": "IPHONE15", "qty": "10", "date": "01.07.2026"})
    assert response.status_code == 302
    with app.app_context():
        from database import Supply
        supply = Supply.query.filter_by(sku="IPHONE15").first()
        assert supply is not None
        assert supply.quantity == 10