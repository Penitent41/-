from database.db_manager import get_connection

class OrderItem:
    def __init__(self, id=None, order_id=None, product_id=None, quantity=None, item_price=None):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.item_price = item_price

    def save(self):
        """Сохраняет позицию заказа в базу данных"""
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, item_price) "
                "VALUES (?, ?, ?, ?)",
                (self.order_id, self.product_id, self.quantity, self.item_price)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE order_items SET order_id = ?, product_id = ?, quantity = ?, item_price = ? "
                "WHERE id = ?",
                (self.order_id, self.product_id, self.quantity, self.item_price, self.id)
            )
        
        conn.commit()
        conn.close()

    def delete(self):
        """Удаляет позицию заказа"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM order_items WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()

def get_items_by_order_id(order_id):
    """Возвращает все позиции для указанного заказа"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, order_id, product_id, quantity, item_price "
        "FROM order_items WHERE order_id = ?",
        (order_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    return [OrderItem(id=row[0], order_id=row[1], product_id=row[2], 
                     quantity=row[3], item_price=row[4]) for row in rows]