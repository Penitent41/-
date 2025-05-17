from database.db_manager import get_connection
import random

class IDGenerator:
    _used_ids = set()

    def generate_id(cls):
        """Генерирует уникальный 6-значный ID для продукта"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM products")
            db_ids = {row[0] for row in cursor.fetchall()}
            
            while True:
                new_id = random.randint(100000, 999999)  # 6-значный ID
                if new_id not in db_ids and new_id not in cls._used_ids:
                    cls._used_ids.add(new_id)
                    return new_id
        finally:
            conn.close()

class Product:
    def __init__(self, id=None, name=None, description=None, price=None, 
                 has_delivery=False, stock=0, delivery_options=None):
        """
        Инициализация товара. Если ID не указан, генерируется автоматически.
        
        Args:
            id (int, optional): Уникальный идентификатор товара. Defaults to None.
            name (str): Название товара.
            description (str): Описание товара.
            price (float): Цена товара.
            has_delivery (bool): Возможность доставки. Defaults to False.
            stock (int): Количество на складе. Defaults to 0.
            delivery_options (list, optional): Способы доставки. Defaults to None.
        """
        self.id = id if id is not None else IDGenerator.generate_id()
        self.name = name
        self.description = description
        self.price = price
        self.has_delivery = has_delivery
        self.stock = stock
        self.delivery_options = delivery_options or []

    def save(self):
        """Сохраняет товар в базу данных (создает новый или обновляет существующий)"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            if not self._exists_in_db():
                cursor.execute("""
                    INSERT INTO products (id, name, description, price, has_delivery, stock)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (self.id, self.name, self.description, self.price, self.has_delivery, self.stock))
                
                if self.has_delivery and self.delivery_options:
                    for method_id, additional_cost in self.delivery_options:
                        cursor.execute("""
                            INSERT INTO product_delivery_options (product_id, delivery_method_id, additional_cost)
                            VALUES (?, ?, ?)
                        """, (self.id, method_id, additional_cost))
            else:
                cursor.execute("""
                    UPDATE products 
                    SET name = ?, description = ?, price = ?, has_delivery = ?, stock = ?
                    WHERE id = ?
                """, (self.name, self.description, self.price, self.has_delivery, self.stock, self.id))
                
                cursor.execute("DELETE FROM product_delivery_options WHERE product_id = ?", (self.id,))
                if self.has_delivery and self.delivery_options:
                    for method_id, additional_cost in self.delivery_options:
                        cursor.execute("""
                            INSERT INTO product_delivery_options (product_id, delivery_method_id, additional_cost)
                            VALUES (?, ?, ?)
                        """, (self.id, method_id, additional_cost))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _exists_in_db(self):
        """Проверяет, существует ли товар в базе данных"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM products WHERE id = ?", (self.id,))
            return cursor.fetchone() is not None
        finally:
            conn.close()

    def delete(self):
        """Удаляет товар из базы данных"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute("DELETE FROM product_delivery_options WHERE product_id = ?", (self.id,))
                cursor.execute("DELETE FROM products WHERE id = ?", (self.id,))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                conn.close()
            # Удаляем ID из кэша генератора
            if self.id in IDGenerator._used_ids:
                IDGenerator._used_ids.remove(self.id)

    def get_available_delivery_methods(self):
        """Возвращает доступные способы доставки для этого товара"""
        if not self.has_delivery:
            return []
            
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT dm.id, dm.name, dm.base_cost, dm.speed_days, pdo.additional_cost
                FROM delivery_methods dm
                JOIN product_delivery_options pdo ON dm.id = pdo.delivery_method_id
                WHERE pdo.product_id = ? AND dm.is_available = 1
            """, (self.id,))
            return cursor.fetchall()
        finally:
            conn.close()

    def get_all_products():
        """Возвращает список всех товаров"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, description, price, has_delivery, stock 
                FROM products
                ORDER BY name
            """)
            
            products = []
            for row in cursor.fetchall():
                product = Product(
                    id=row[0], name=row[1], description=row[2], 
                    price=row[3], has_delivery=bool(row[4]), stock=row[5]
                )
                
                if product.has_delivery:
                    cursor.execute("""
                        SELECT delivery_method_id, additional_cost
                        FROM product_delivery_options
                        WHERE product_id = ?
                    """, (product.id,))
                    product.delivery_options = cursor.fetchall()
                
                products.append(product)
            
            return products
        finally:
            conn.close()

    def get_product_by_id(product_id):
        """Возвращает товар по его ID"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, description, price, has_delivery, stock 
                FROM products 
                WHERE id = ?
            """, (product_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
                
            product = Product(
                id=row[0], name=row[1], description=row[2], 
                price=row[3], has_delivery=bool(row[4]), stock=row[5]
            )
            
            if product.has_delivery:
                cursor.execute("""
                    SELECT delivery_method_id, additional_cost
                    FROM product_delivery_options
                    WHERE product_id = ?
                """, (product.id,))
                product.delivery_options = cursor.fetchall()
            
            return product
        finally:
            conn.close()

    def get_products_with_delivery():
        """Возвращает товары с доступной доставкой"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, description, price, stock 
                FROM products 
                WHERE has_delivery = 1
                ORDER BY name
            """)
            
            products = []
            for row in cursor.fetchall():
                product = Product(
                    id=row[0], name=row[1], description=row[2], 
                    price=row[3], has_delivery=True, stock=row[4]
                )
                
                cursor.execute("""
                    SELECT delivery_method_id, additional_cost
                    FROM product_delivery_options
                    WHERE product_id = ?
                """, (product.id,))
                product.delivery_options = cursor.fetchall()
                
                products.append(product)
            
            return products
        finally:
            conn.close()

def get_all_products():
    return Product.get_all_products()

def get_products_with_delivery():
    return Product.get_products_with_delivery()

def get_product_by_id(product_id):
    return Product.get_product_by_id(product_id)