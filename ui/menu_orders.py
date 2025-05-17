from models.order import Order, get_all_orders, get_order_by_id
from models.client import get_all_clients
from models.order_item import OrderItem, get_items_by_order_id
from models.product import get_all_products, get_product_by_id
from models.delivery import get_all_delivery_methods
from datetime import datetime

def manage_order_items(order_id):
    while True:
        print("\n=== Позиции заказа ===")
        items = get_items_by_order_id(order_id)
        if not items:
            print("Нет позиций.")
        else:
            for item in items:
                product = get_product_by_id(item.product_id)
                print(f"{item.id}. {product.name} | Кол-во: {item.quantity} | Цена: {item.item_price} руб.")
        
        print("1. Добавить позицию")
        print("2. Удалить позицию")
        print("3. Изменить позицию")
        print("0. Назад к заказу")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            products = get_all_products()
            print("Доступные товары:")
            for p in products:
                print(f"{p.id}. {p.name} - {p.price} руб.")
            
            product_id = int(input("Введите ID товара: "))
            quantity = int(input("Введите количество: "))
            product = get_product_by_id(product_id)
            
            if product.has_delivery:
                print("Доступные способы доставки:")
                methods = get_all_delivery_methods()
                for m in methods:
                    print(f"{m.id}. {m.name} ({m.base_cost} руб.)")
            
            item = OrderItem(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity,
                item_price=product.price
            )
            item.save()
            print("✅ Позиция добавлена.")
        
        elif choice == "2":
            item_id = int(input("Введите ID позиции: "))
            item = OrderItem(id=item_id)
            item.delete()
            print("✅ Позиция удалена.")
        
        elif choice == "3":
            item_id = int(input("Введите ID позиции: "))
            quantity = int(input("Новое количество: "))
            item = next((i for i in items if i.id == item_id), None)
            if item:
                item.quantity = quantity
                item.save()
                print("✅ Позиция обновлена.")
            else:
                print("❌ Позиция не найдена.")
        
        elif choice == "0":
            break
        
        else:
            print("❌ Неверный ввод")

def menu_orders():
    while True:
        print("\n=== Заказы ===")
        print("1. Показать все заказы")
        print("2. Добавить заказ")
        print("3. Удалить заказ")
        print("4. Управление позициями")
        print("0. Назад в главное меню")
        choice = input("Выберите действие: ")
        
        if choice == "1":
            orders = get_all_orders()
            print("\nСписок заказов:")
            for o in orders:
                client = next((c for c in get_all_clients() if c.id == o.client_id), None)
                print(f"{o.id}. {client.name if client else 'N/A'} | Дата: {o.order_date} | Сумма: {o.total_amount} руб. | Статус: {o.status}")
        
        elif choice == "2":
            print("Доступные клиенты:")
            clients = get_all_clients()
            for c in clients:
                print(f"{c.id}. {c.name}")
            
            client_id = int(input("Введите ID клиента: "))
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            order = Order(
                client_id=client_id,
                order_date=order_date,
                total_amount=0,
                status="новый"
            )
            order.save()
            
            print("✅ Заказ создан. Добавьте позиции:")
            manage_order_items(order.id)
            
            items = get_items_by_order_id(order.id)
            if items:
                order.total_amount = sum(item.quantity * item.item_price for item in items)
                
                delivery_products = any(get_product_by_id(item.product_id).has_delivery for item in items)
                if delivery_products:
                    methods = get_all_delivery_methods()
                    print("\nВыберите способ доставки:")
                    for m in methods:
                        print(f"{m.id}. {m.name} ({m.base_cost} руб.)")
                    
                    method_id = int(input("Введите ID способа доставки: "))
                    method = next((m for m in methods if m.id == method_id), None)
                    if method:
                        order.delivery_method_id = method_id
                        order.delivery_cost = method.base_cost
                        order.total_amount += method.base_cost
            
            order.save()
            print(f"✅ Заказ #{order.id} оформлен. Сумма: {order.total_amount} руб.")
        
        elif choice == "3":
            order_id = int(input("Введите ID заказа: "))
            order = Order(id=order_id)
            order.delete()
            print("✅ Заказ удален.")
        
        elif choice == "4":
            order_id = int(input("Введите ID заказа: "))
            if get_order_by_id(order_id):
                manage_order_items(order_id)
            else:
                print("❌ Заказ не найден")
        
        elif choice == "0":
            break
        
        else:
            print("❌ Неверный ввод")