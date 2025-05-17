from database.db_manager import get_connection
import random

class Client:
    def __init__(self, id=None, name=None, address=None, phone=None, 
                 contact_person=None, email=None):
        """
        Инициализация клиента. Если ID не указан, должен быть сгенерирован автоматически.
        
        Args:
            id (int, optional): Уникальный идентификатор клиента. Defaults to None.
            name (str): ФИО клиента.
            address (str): Адрес клиента.
            phone (str): Телефон клиента.
            contact_person (str): Контактное лицо.
            email (str, optional): Email клиента. Defaults to None.
        """
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        self.contact_person = contact_person
        self.email = email

    def save(self):
        """Сохраняет клиента в базу данных (создает новый или обновляет существующий)"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            if not self._exists_in_db():
                if self.id is None:
                    while True:
                        new_id = random.randint(100000, 999999)
                        cursor.execute("SELECT 1 FROM clients WHERE id = ?", (new_id,))
                        if cursor.fetchone() is None:
                            self.id = new_id
                            break
                
                cursor.execute("""
                    INSERT INTO clients (id, name, address, phone, contact_person, email)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (self.id, self.name, self.address, self.phone, self.contact_person, self.email))
            else:
                cursor.execute("""
                    UPDATE clients 
                    SET name = ?, address = ?, phone = ?, contact_person = ?, email = ?
                    WHERE id = ?
                """, (self.name, self.address, self.phone, self.contact_person, self.email, self.id))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _exists_in_db(self):
        """Проверяет, существует ли клиент в базе данных"""
        if self.id is None:
            return False
            
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM clients WHERE id = ?", (self.id,))
            return cursor.fetchone() is not None
        finally:
            conn.close()

    def delete(self):
        """Удаляет клиента из базы данных"""
        if self.id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute("SELECT 1 FROM orders WHERE client_id = ?", (self.id,))
                if cursor.fetchone():
                    raise ValueError("Нельзя удалить клиента с существующими заказами")
                
                cursor.execute("DELETE FROM clients WHERE id = ?", (self.id,))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                conn.close()

    def get_all_clients():
        """Возвращает список всех клиентов"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, address, phone, contact_person, email 
                FROM clients
                ORDER BY name
            """)
            
            clients = []
            for row in cursor.fetchall():
                client = Client(
                    id=row[0], name=row[1], address=row[2],
                    phone=row[3], contact_person=row[4], email=row[5]
                )
                clients.append(client)
            
            return clients
        finally:
            conn.close()

    @staticmethod
    def get_client_by_id(client_id):
        """Возвращает клиента по его ID"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, name, address, phone, contact_person, email 
                FROM clients 
                WHERE id = ?
            """, (client_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
                
            return Client(
                id=row[0], name=row[1], address=row[2],
                phone=row[3], contact_person=row[4], email=row[5]
            )
        finally:
            conn.close()

    def search_clients(search_term):
        """Поиск клиентов по имени, телефону или фамилии"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            search_pattern = f"%{search_term}%"
            cursor.execute("""
                SELECT id, name, address, phone, contact_person, email 
                FROM clients
                WHERE name LIKE ? OR phone LIKE ? OR contact_person LIKE ?
                ORDER BY name
            """, (search_pattern, search_pattern, search_pattern))
            
            clients = []
            for row in cursor.fetchall():
                client = Client(
                    id=row[0], name=row[1], address=row[2],
                    phone=row[3], contact_person=row[4], email=row[5]
                )
                clients.append(client)
            
            return clients
        finally:
            conn.close()


def get_all_clients():
    return Client.get_all_clients()

def get_client_by_id(client_id):
    return Client.get_client_by_id(client_id)

def search_clients(search_term):
    return Client.search_clients(search_term)