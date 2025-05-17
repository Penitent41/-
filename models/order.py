from database.db_manager import get_connection
from datetime import datetime

class Order:
    def __init__(self, id=None, client_id=None, order_date=None, total_amount=0.0, status='new', delivery_id=None):
        self.id = id
        self.client_id = client_id
        self.order_date = order_date or datetime.now().isoformat()
        self.total_amount = total_amount
        self.status = status
        self.delivery_id = delivery_id

    def save(self):
        """Добавляет новый заказ или обновляет существующий"""
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO orders (client_id, order_date, total_amount, status, delivery_id) VALUES (?, ?, ?, ?, ?)",
                (self.client_id, self.order_date, self.total_amount, self.status, self.delivery_id)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE orders SET client_id = ?, order_date = ?, total_amount = ?, status = ?, delivery_id = ? WHERE id = ?",
                (self.client_id, self.order_date, self.total_amount, self.status, self.delivery_id, self.id)
            )
        conn.commit()
        conn.close()

    def delete(self):
        """Удаляет заказ"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM order_items WHERE order_id = ?", (self.id,))
            cursor.execute("DELETE FROM orders WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()

def get_all_orders():
    """Возвращает список всех заказов"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.client_id, o.order_date, o.total_amount, o.status, o.delivery_id,
               c.name as client_name, d.method as delivery_method
        FROM orders o
        LEFT JOIN clients c ON o.client_id = c.id
        LEFT JOIN deliveries d ON o.delivery_id = d.id
    """)
    rows = cursor.fetchall()
    conn.close()
    return [Order(id=row[0], client_id=row[1], order_date=row[2], 
                 total_amount=row[3], status=row[4], delivery_id=row[5]) for row in rows]

def get_order_by_id(order_id):
    """Возвращает заказ по ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.client_id, o.order_date, o.total_amount, o.status, o.delivery_id,
               c.name as client_name, d.method as delivery_method
        FROM orders o
        LEFT JOIN clients c ON o.client_id = c.id
        LEFT JOIN deliveries d ON o.delivery_id = d.id
        WHERE o.id = ?
    """, (order_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Order(id=row[0], client_id=row[1], order_date=row[2], 
                    total_amount=row[3], status=row[4], delivery_id=row[5])
    return None