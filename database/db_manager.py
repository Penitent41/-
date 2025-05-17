import sqlite3
import random
from config import DB_NAME

class IDGenerator:
    _used_ids = set()

    def generate_id(cls):
        while True:
            new_id = random.randint(1000, 9999)  # 4-значные ID
            if new_id not in cls._used_ids:
                cls._used_ids.add(new_id)
                return new_id

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS used_ids (
        id INTEGER PRIMARY KEY,
        entity_type TEXT NOT NULL
    )
    ''')

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            contact_person TEXT NOT NULL,
            email TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS delivery_methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            base_cost REAL NOT NULL,
            speed_days INTEGER NOT NULL,
            is_available BOOLEAN NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            has_delivery BOOLEAN NOT NULL,
            stock INTEGER NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_delivery_options (
            product_id INTEGER NOT NULL,
            delivery_method_id INTEGER NOT NULL,
            additional_cost REAL DEFAULT 0,
            PRIMARY KEY (product_id, delivery_method_id),
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (delivery_method_id) REFERENCES delivery_methods(id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_deliveries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            delivery_method_id INTEGER NOT NULL,
            delivery_cost REAL NOT NULL,
            estimated_delivery_date TEXT,
            actual_delivery_date TEXT,
            tracking_number TEXT,
            address TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (delivery_method_id) REFERENCES delivery_methods(id)
        )
        ''')

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()