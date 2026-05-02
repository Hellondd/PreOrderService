from database import db, Supply, PreOrder, User
from modules.notifications import NotificationModule

class InventoryModule:
    @staticmethod
    def add_supply(sku, qty, date):
        new_supply = Supply(sku=sku, quantity=qty, arrival_date=date)
        db.session.add(new_supply)
        db.session.commit()
        
        # Триггер: Ищем заказы в листе ожидания и переводим их в Pending (В пути)
        waitlist_orders = PreOrder.query.filter_by(sku=sku, status="Waitlist").order_by(PreOrder.id).all()
        available_qty = qty
        
        for order in waitlist_orders:
            if available_qty >= order.quantity:
                order.status = "Pending"
                available_qty -= order.quantity
                
                user = User.query.get(order.user_id)
                NotificationModule.send_telegram_msg(
                    user.telegram_id, 
                    f"Отличные новости! Ваш предзаказ на {sku} ({order.quantity} шт.) переведен в статус 'В пути'."
                )
        db.session.commit()

    @staticmethod
    def receive_supply(supply_id):
        supply = Supply.query.get(supply_id)
        if supply:
            supply.status = "Arrived"
            # Триггер: Переводим заказы из Pending в Ready
            pending_orders = PreOrder.query.filter_by(sku=supply.sku, status="Pending").order_by(PreOrder.id).all()
            stock = supply.quantity
            
            for order in pending_orders:
                if stock >= order.quantity:
                    order.status = "Ready"
                    stock -= order.quantity
                    
                    user = User.query.get(order.user_id)
                    NotificationModule.send_telegram_msg(
                        user.telegram_id, 
                        f"Ваш заказ на {supply.sku} прибыл на склад и готов к выдаче!"
                    )
            db.session.commit()