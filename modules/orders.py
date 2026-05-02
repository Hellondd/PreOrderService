from database import db, PreOrder, Supply

class OrderModule:
    @staticmethod
    def create_preorder(user_id, sku, qty):
        # Считаем доступный остаток в пути
        total_in_transit = db.session.query(db.func.sum(Supply.quantity)).filter_by(sku=sku, status="In Transit").scalar() or 0
        already_booked = db.session.query(db.func.sum(PreOrder.quantity)).filter_by(sku=sku, status="Pending").scalar() or 0
        
        if (total_in_transit - already_booked) >= int(qty):
            new_order = PreOrder(user_id=user_id, sku=sku, quantity=qty)
            db.session.add(new_order)
            db.session.commit()
            return True, "Бронь оформлена"
        return False, "Недостаточно товара в пути"