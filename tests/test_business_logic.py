import pytest
from app import app, db
from database import User, Product, Supply, PreOrder
from modules.inventory import InventoryModule
from modules.orders import OrderModule

# Фикстура для создания реальной тестовой базы данных SQLite
@pytest.fixture(scope='module')
def test_db():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_warehouse.db'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        
        # Подготовка данных: создаем клиента и товар для тестирования
        test_user = User(username="test_client", password="123", role="client", telegram_id="00000")
        test_product = Product(sku="TEST_SKU", name="Тестовый товар")
        
        db.session.add(test_user)
        db.session.add(test_product)
        db.session.commit()
        
        yield db
        
        db.drop_all()

# ==========================================
# ИНТЕГРАЦИОННЫЕ ТЕСТЫ БИЗНЕС-ЛОГИКИ
# ==========================================

def test_1_create_preorder_waitlist(test_db):
    """Шаг 1: Создание заказа при отсутствии поставок (ожидается Waitlist)"""
    # Вызываем реальный метод из orders.py
    success, msg = OrderModule.create_preorder(user_id=1, sku="TEST_SKU", qty=2)
    
    # Проверка физической записи в БД
    order = PreOrder.query.first()
    assert order is not None
    assert order.status == "Waitlist" # Товара нет в пути, статус должен быть Waitlist[cite: 12]
    assert order.quantity == 2

def test_2_add_supply_updates_waitlist(test_db):
    """Шаг 2: Добавление поставки. Заказ должен сменить статус на Pending"""
    # Вызываем реальный метод из inventory.py[cite: 10]
    InventoryModule.add_supply(sku="TEST_SKU", qty=5, date="2026-06-01")
    
    # Проверяем саму поставку
    supply = Supply.query.first()
    assert supply.status == "In Transit"
    assert supply.quantity == 5
    
    # Проверяем, что заказ обновился благодаря методу _process_orders[cite: 10]
    order = PreOrder.query.first()
    assert order.status == "Pending"

def test_3_create_preorder_pending_immediately(test_db):
    """Шаг 3: Создание заказа, когда товар УЖЕ в пути (ожидается Pending сразу)"""
    # В пути 5 шт, 2 уже забронировано. Заказываем оставшиеся 3.
    success, msg = OrderModule.create_preorder(user_id=1, sku="TEST_SKU", qty=3)
    
    # В базе должно быть 2 заказа
    orders = PreOrder.query.order_by(PreOrder.id).all()
    assert len(orders) == 2
    assert orders[1].status == "Pending" # Хватило товара в пути, статус сразу Pending[cite: 12]
    assert orders[1].quantity == 3

def test_4_receive_supply_updates_to_ready(test_db):
    """Шаг 4: Приемка товара на склад. Все брони должны стать Ready"""
    supply = Supply.query.first()
    # Вызываем реальный метод приемки[cite: 10]
    InventoryModule.receive_supply(supply_id=supply.id)
    
    supply_updated = Supply.query.first()
    assert supply_updated.status == "Arrived" # Статус поставки изменился[cite: 10]
    
    # Все заказы должны поменять статус на Ready[cite: 10]
    orders = PreOrder.query.all()
    for order in orders:
        assert order.status == "Ready"