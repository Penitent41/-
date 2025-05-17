from database.db_manager import get_connection

class DeliveryMethod:
    def __init__(self, id=None, name=None, description=None, 
                 base_cost=0.0, speed_days=1, is_available=True):
        self.id = id
        self.name = name
        self.description = description
        self.base_cost = base_cost
        self.speed_days = speed_days
        self.is_available = is_available

    def save(self):
        """Сохраняет способ доставки"""
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None:
            cursor.execute("""
                INSERT INTO delivery_methods 
                (name, description, base_cost, speed_days, is_available)
                VALUES (?, ?, ?, ?, ?)
            """, (self.name, self.description, self.base_cost,
                 self.speed_days, self.is_available))
            self.id = cursor.lastrowid
        else:
            cursor.execute("""
                UPDATE delivery_methods SET
                name = ?, description = ?, base_cost = ?,
                speed_days = ?, is_available = ?
                WHERE id = ?
            """, (self.name, self.description, self.base_cost,
                 self.speed_days, self.is_available, self.id))
        
        conn.commit()
        conn.close()

    def delete(self):
        """Удаляет способ доставки"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM delivery_methods WHERE id = ?", (self.id,))
            conn.commit()
            conn.close()

    def get_all():
        """Возвращает все способы доставки"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM delivery_methods")
        rows = cursor.fetchall()
        conn.close()
        return [DeliveryMethod(id=row[0], name=row[1], description=row[2],
                base_cost=row[3], speed_days=row[4], is_available=bool(row[5])) 
                for row in rows]

    def get_available():
        """Возвращает только доступные способы доставки"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM delivery_methods WHERE is_available = 1")
        rows = cursor.fetchall()
        conn.close()
        return [DeliveryMethod(id=row[0], name=row[1], description=row[2],
                base_cost=row[3], speed_days=row[4], is_available=True) 
                for row in rows]

    def get_by_id(method_id):
        """Возвращает способ доставки по ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM delivery_methods WHERE id = ?", (method_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return DeliveryMethod(id=row[0], name=row[1], description=row[2],
                                base_cost=row[3], speed_days=row[4], 
                                is_available=bool(row[5]))
        return None

def get_all_delivery_methods():
    return DeliveryMethod.get_all()

def get_available_delivery_methods():
    return DeliveryMethod.get_available()

def get_delivery_method_by_id(method_id):
    return DeliveryMethod.get_by_id(method_id)