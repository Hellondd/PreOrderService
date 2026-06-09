import pytest
import sys
import os

# Добавляем корень проекта в sys.path, чтобы импортировать app и modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from database import db, User, Product, Supply, PreOrder
from modules.inventory import InventoryModule
from modules.orders import OrderModule

# Фикстура для тестовой БД (создаётся отдельно, не мешает основной)
@pytest.fixture(scope="module")
def test_client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_warehouse.db"
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.create_all()
        # Создаём тестового пользователя и товар, если их нет
        if not User.query.filter_by(username="test_client").first():
            test_user = User(
                username="test_client",
                password=IdentityModule.hash_password("123"),
                role="client",
                telegram_id="12345"
            )
            db.session.add(test_user)
        if not Product.query.filter_by(sku="TEST_SKU").first():
            test_product = Product(sku="TEST_SKU", name="Тестовый товар")
            db.session.add(test_product)
        db.session.commit()
        yield app.test_client()
        db.drop_all()

# Импортируем IdentityModule после того, как путь настроен
from modules.identity import IdentityModule

def test_1_create_preorder_waitlist(test_client):
    """Создание заказа при отсутствии поставок -> статус Waitlist"""
    with app.app_context():
        user = User.query.filter_by(username="test_client").first()
        success, msg = OrderModule.create_preorder(user.id, "TEST_SKU", 2)
        assert success is True
        order = PreOrder.query.filter_by(user_id=user.id).first()
        assert order is not None
        assert order.status == "Waitlist"
        assert order.quantity == 2

def test_2_add_supply_updates_waitlist(test_client):
    """Добавление поставки переводит заказ из Waitlist в Pending"""
    with app.app_context():
        InventoryModule.add_supply("TEST_SKU", 5, "2026-06-01")
        supply = Supply.query.filter_by(sku="TEST_SKU").first()
        assert supply.status == "In Transit"
        order = PreOrder.query.filter_by(sku="TEST_SKU").first()
        assert order.status == "Pending"

def test_3_create_preorder_pending_immediately(test_client):
    """Если товар уже в пути и есть свободный остаток, заказ создаётся со статусом Pending"""
    with app.app_context():
        user = User.query.filter_by(username="test_client").first()
        success, msg = OrderModule.create_preorder(user.id, "TEST_SKU", 3)
        assert success is True
        orders = PreOrder.query.filter_by(sku="TEST_SKU").order_by(PreOrder.id).all()
        # Всего должно быть 2 заказа: первый на 2 шт, второй на 3 шт
        assert len(orders) == 2
        assert orders[1].status == "Pending"

def test_4_receive_supply_updates_to_ready(test_client):
    """Приёмка товара на склад переводит заказы в статус Ready"""
    with app.app_context():
        supply = Supply.query.filter_by(sku="TEST_SKU").first()
        InventoryModule.receive_supply(supply.id)
        supply_updated = Supply.query.get(supply.id)
        assert supply_updated.status == "Arrived"
        orders = PreOrder.query.filter_by(sku="TEST_SKU").all()
        for order in orders:
            assert order.status == "Ready"