from database import db, PreOrder, Supply, User
from modules.notifications import NotificationModule


class OrderModule:
    @staticmethod
    def create_preorder(user_id, sku, qty):
        user = User.query.get(user_id)
        qty = int(qty)

        # Считаем доступный товар В ПУТИ, который еще не забронирован
        total_in_transit = (
            db.session.query(db.func.sum(Supply.quantity))
            .filter_by(sku=sku, status="In Transit")
            .scalar() or 0
        )

        already_booked = (
            db.session.query(db.func.sum(PreOrder.quantity))
            .filter_by(sku=sku, status="Pending")
            .scalar() or 0
        )

        available = total_in_transit - already_booked

        if available >= qty:
            status = "Pending"
            msg = (
                f"Товар {sku} ({qty} шт.) забронирован. "
                "Он уже находится в пути на склад."
            )
        else:
            status = "Waitlist"
            msg = (
                f"Товар {sku} ({qty} шт.) добавлен в лист ожидания. "
                "Как только появится поставка, он будет забронирован автоматически."
            )

        new_order = PreOrder(user_id=user_id, sku=sku, quantity=qty, status=status)
        db.session.add(new_order)
        db.session.commit()

        NotificationModule.send_telegram_msg(user.telegram_id, msg)
        return True, msg
