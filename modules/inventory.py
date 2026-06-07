from database import db, Supply, PreOrder, User
from modules.notifications import NotificationModule


class InventoryModule:
    @staticmethod
    def _process_orders(sku, available_qty, current_status, new_status, msg_template):
        """Вспомогательный метод для обновления статусов и рассылки"""
        orders = (
            PreOrder.query.filter_by(sku=sku, status=current_status)
            .order_by(PreOrder.id)
            .all()
        )
        for order in orders:
            if available_qty >= order.quantity:
                order.status = new_status
                available_qty -= order.quantity

                user = User.query.get(order.user_id)
                msg = msg_template.format(sku=sku, qty=order.quantity)
                NotificationModule.send_telegram_msg(user.telegram_id, msg)
        return available_qty

    @staticmethod
    def add_supply(sku, qty, date):
        new_supply = Supply(sku=sku, quantity=qty, arrival_date=date)
        db.session.add(new_supply)

        msg_tmpl = "Отличные новости! Ваш предзаказ на {sku} ({qty} шт.) переведен в статус 'В пути'."
        InventoryModule._process_orders(sku, qty, "Waitlist", "Pending", msg_tmpl)
        db.session.commit()

    @staticmethod
    def receive_supply(supply_id):
        supply = Supply.query.get(supply_id)
        if supply:
            supply.status = "Arrived"
            msg_tmpl = "Ваш заказ на {sku} прибыл на склад и готов к выдаче!"
            InventoryModule._process_orders(
                supply.sku, supply.quantity, "Pending", "Ready", msg_tmpl
            )
            db.session.commit()
