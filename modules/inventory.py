from database import db, Supply, PreOrder

class InventoryModule:
    @staticmethod
    def add_supply(sku, qty, date):
        new_supply = Supply(sku=sku, quantity=qty, arrival_date=date)
        db.session.add(new_supply)
        db.session.commit()

    @staticmethod
    def receive_supply(supply_id):
        supply = Supply.query.get(supply_id)
        if supply:
            supply.status = "Arrived"
            # Логика распределения: ищем предзаказы на этот SKU
            pending_orders = PreOrder.query.filter_by(sku=supply.sku, status="Pending").all()
            stock = supply.quantity
            for order in pending_orders:
                if stock >= order.quantity:
                    order.status = "Ready"
                    stock -= order.quantity
            db.session.commit()