from models.product import Product, get_all_products, get_products_with_delivery
from models.client import get_all_clients, get_client_by_id, Client
from models.delivery import get_all_delivery_methods, DeliveryMethod
from models.order import Order, get_all_orders  

def show_main_menu():
    print("\n=== Система управления заказами ===")
    print("1. Управление товарами")
    print("2. Управление клиентами")
    print("3. Управление заказами")
    print("4. Управление способами доставки")
    print("0. Выход")
    return input("Выберите действие: ")

def menu_delivery():
    while True:
        print("\n=== Управление способами доставки ===")
        print("1. Показать все способы доставки")
        print("2. Добавить способ доставки")
        print("3. Удалить способ доставки")
        print("4. Изменить способ доставки")
        print("0. Назад в главное меню")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            methods = get_all_delivery_methods()
            print("\nСпособы доставки:")
            for m in methods:
                status = "Активен" if m.is_available else "Неактивен"
                print(f"{m.id}. {m.name} | {m.base_cost} руб. | {m.speed_days} дн. | {status}")
        
        elif choice == "2":
            print("\nДобавление способа доставки:")
            name = input("Название: ")
            cost = float(input("Базовая стоимость: "))
            days = int(input("Срок доставки (дней): "))
            
            method = DeliveryMethod(
                name=name,
                base_cost=cost,
                speed_days=days,
                is_available=True
            )
            method.save()
            print("✅ Способ доставки добавлен")
        
        elif choice == "3":
            method_id = int(input("ID способа доставки для удаления: "))
            method = DeliveryMethod(id=method_id)
            method.delete()
            print("✅ Способ доставки удален")
        
        elif choice == "4":
            method_id = int(input("ID способа доставки для изменения: "))
            method = DeliveryMethod.get_by_id(method_id)
            if method:
                print("\nОставьте поле пустым, чтобы не изменять")
                name = input(f"Название [{method.name}]: ") or method.name
                cost = input(f"Стоимость [{method.base_cost}]: ") or method.base_cost
                days = input(f"Срок [{method.speed_days}]: ") or method.speed_days
                status = input(f"Активен (да/нет) [{'да' if method.is_available else 'нет'}]: ")
                
                updated = DeliveryMethod(
                    id=method_id,
                    name=name,
                    base_cost=float(cost),
                    speed_days=int(days),
                    is_available=status.lower() == 'да' if status else method.is_available
                )
                updated.save()
                print("✅ Способ доставки обновлен")
        
        elif choice == "0":
            break

def menu_products():
    while True:
        print("\n=== Управление товарами ===")
        print("1. Показать все товары")
        print("2. Добавить товар")
        print("3. Удалить товар")
        print("4. Изменить товар")
        print("5. Товары с доставкой")
        print("0. Назад в главное меню")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            products = get_all_products()
            print("\nСписок товаров:")
            for p in products:
                delivery_status = "✅" if p.has_delivery else "❌"
                print(f"{p.id}. {p.name} | Цена: {p.price} руб. | "
                      f"В наличии: {p.stock} | Доставка: {delivery_status} | "
                      f"Описание: {p.description[:30]}...")
        
        elif choice == "2":
            print("\n=== Добавление нового товара ===")
            name = input("Название товара: ")
            description = input("Описание товара: ")
            price = float(input("Цена: "))
            stock = int(input("Количество на складе: "))
            has_delivery = input("Доступна доставка? (да/нет): ").lower() == 'да'
            
            product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock,
                has_delivery=has_delivery
            )
            product.save()
            
            if has_delivery:
                print("\nДоступные способы доставки:")
                methods = get_all_delivery_methods()
                for m in methods:
                    print(f"{m.id}. {m.name} ({m.base_cost} руб., {m.speed_days} дней)")
                
                while True:
                    method_id = input("Добавить способ доставки (ID или 0 для завершения): ")
                    if method_id == '0':
                        break
                    try:
                        additional_cost = float(input("Дополнительная стоимость для этого товара: "))
                        product.delivery_options.append((int(method_id), additional_cost))
                        product.save()
                    except:
                        print("❌ Ошибка ввода!")
            
            print("✅ Товар добавлен.")
        
        elif choice == "3":
            product_id = input("Введите ID товара для удаления: ")
            product = Product(id=int(product_id))
            product.delete()
            print("✅ Товар удалён.")
        
        elif choice == "4":
            product_id = int(input("Введите ID товара для редактирования: "))
            current_product = next((p for p in get_all_products() if p.id == product_id), None)
            
            if not current_product:
                print("❌ Товар не найден!")
                continue
                
            print("\nОставьте поле пустым, чтобы не изменять значение")
            name = input(f"Новое название [{current_product.name}]: ")
            description = input(f"Новое описание [{current_product.description}]: ")
            price = input(f"Новая цена [{current_product.price}]: ")
            stock = input(f"Новое количество [{current_product.stock}]: ")
            has_delivery = input(f"Доставка [{'да' if current_product.has_delivery else 'нет'}]: ")
            
            product = Product(
                id=product_id,
                name=name if name else current_product.name,
                description=description if description else current_product.description,
                price=float(price) if price else current_product.price,
                stock=int(stock) if stock else current_product.stock,
                has_delivery=has_delivery.lower() == 'да' if has_delivery else current_product.has_delivery
            )
            
            if product.has_delivery:
                print("\nТекущие способы доставки:")
                for m_id, cost in current_product.delivery_options:
                    method = next(m for m in get_all_delivery_methods() if m.id == m_id)
                    print(f"{method.id}. {method.name} (+{cost} руб.)")
                
                print("\n1. Добавить способ доставки")
                print("2. Удалить способ доставки")
                print("3. Продолжить без изменений")
                delivery_choice = input("Выберите действие: ")
                
                if delivery_choice == "1":
                    methods = get_all_delivery_methods()
                    available_methods = [m for m in methods if m.id not in [x[0] for x in current_product.delivery_options]]
                    
                    for m in available_methods:
                        print(f"{m.id}. {m.name} ({m.base_cost} руб.)")
                    
                    method_id = input("Выберите ID способа доставки: ")
                    additional_cost = float(input("Дополнительная стоимость: "))
                    product.delivery_options = current_product.delivery_options + [(int(method_id), additional_cost)]
                
                elif delivery_choice == "2":
                    method_id = input("Введите ID способа доставки для удаления: ")
                    product.delivery_options = [x for x in current_product.delivery_options if x[0] != int(method_id)]
                else:
                    product.delivery_options = current_product.delivery_options
            
            product.save()
            print("✅ Товар обновлён.")
        
        elif choice == "5":
            products = get_products_with_delivery()
            print("\nТовары с доставкой:")
            for p in products:
                print(f"\n{p.id}. {p.name} ({p.price} руб.)")
                print("Доступные способы доставки:")
                for m in p.get_available_delivery_methods():
                    total_cost = m[2] + m[4]  # base_cost + additional_cost
                    print(f"  - {m[1]}: {total_cost} руб. ({m[3]} дней)")
        
        elif choice == "0":
            break
        
        else:
            print("❌ Неверный ввод!")

def menu_clients():
    while True:
        print("\n=== Управление клиентами ===")
        print("1. Показать всех клиентов")
        print("2. Добавить клиента")
        print("3. Удалить клиента")
        print("4. Изменить клиента")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            clients = get_all_clients()
            print("\nСписок клиентов:")
            for client in clients:
                print(f"ID:{client.id} | Имя:{client.name} | Фамилия:{client.contact_person} | Телефон:{client.phone} | Aдрес:{client.address}")
        
        elif choice == "2":
            print("\nДобавление нового клиента:")
            name = input("Имя: ")
            contact = input("Фамилия: ")
            phone = input("Телефон: ")
            address = input("Адрес: ")
            email = input("Email (необязательно): ")
            
            client = Client(
                name=name,
                contact_person=contact,
                phone=phone,
                address=address,
                email=email
            )
            client.save()
            print("✅ Клиент добавлен")
        
        elif choice == "3":
            client_id = int(input("Введите ID клиента для удаления: "))
            client = Client(id=client_id)
            client.delete()
            print("✅ Клиент удален")
        
        elif choice == "4":
            client_id = int(input("Введите ID клиента для изменения: "))
            client = get_client_by_id(client_id)
            if client:
                print("\nОставьте поле пустым, чтобы не изменять")
                name = input(f"Имя [{client.name}]: ") or client.name
                contact = input(f"Фамилия [{client.contact_person}]: ") or client.contact_person
                phone = input(f"Телефон [{client.phone}]: ") or client.phone
                address = input(f"Адрес [{client.address}]: ") or client.address
                
                updated = Client(
                    id=client_id,
                    name=name,
                    contact_person=contact,
                    phone=phone,
                    address=address,
                    email=client.email
                )
                updated.save()
                print("✅ Клиент обновлен")
        
        elif choice == "0":
            break

def menu_orders():
    while True:
        print("\n=== Управление заказами ===")
        print("1. Показать все заказы")
        print("2. Создать заказ")
        print("3. Просмотреть заказ")
        print("4. Изменить статус заказа")
        print("0. Назад в главное меню")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            orders = get_all_orders()
            print("\nСписок заказов:")
            for o in orders:
                print(f"{o.id}. {o.order_date} | Клиент: {o.client_name} | "
                      f"Сумма: {o.total_amount} руб. | Статус: {o.status}")
        
        elif choice == "2":
            print("\n=== Создание нового заказа ===")
            
            print("\nДоступные клиенты:")
            clients = get_all_clients()
            for c in clients:
                print(f"{c.id}. {c.name} ({c.contact_person}, {c.phone})")
            
            client_id = int(input("Выберите ID клиента: "))
            
            order = Order(client_id=client_id)
            
            while True:
                print("\nДоступные товары:")
                products = get_all_products()
                for p in products:
                    print(f"{p.id}. {p.name} ({p.price} руб., {p.stock} шт.)")
                
                product_id = input("Выберите ID товара (или 0 для завершения): ")
                if product_id == '0':
                    break
                
                quantity = int(input("Количество: "))
                product = next(p for p in products if p.id == int(product_id))
                
                if quantity > product.stock:
                    print("❌ Недостаточно товара на складе!")
                    continue
                
                order.add_item(product.id, quantity, product.price)
            
            delivery_products = [p for p in products if p.has_delivery and any(item['product_id'] == p.id for item in order.items)]
            
            if delivery_products:
                print("\nТовары в заказе с доставкой:")
                for p in delivery_products:
                    print(f"- {p.name}")
                
                use_delivery = input("Оформить доставку? (да/нет): ").lower() == 'да'
                
                if use_delivery:
                    print("\nДоступные способы доставки:")
                    methods = get_all_delivery_methods()
                    for m in methods:
                        print(f"{m.id}. {m.name} ({m.base_cost} руб., {m.speed_days} дней)")
                    
                    method_id = int(input("Выберите ID способа доставки: "))
                    order.delivery_method_id = method_id
                    order.delivery_cost = next(m.base_cost for m in methods if m.id == method_id)
            
            order.save()
            print(f"✅ Заказ #{order.id} создан. Общая сумма: {order.total_amount} руб.")
        
        elif choice == "3":
            order_id = int(input("Введите ID заказа: "))
            order = Order.get_by_id(order_id)
            
            if not order:
                print("❌ Заказ не найден!")
                continue
            
            print(f"\n=== Заказ #{order.id} ===")
            print(f"Дата: {order.order_date}")
            print(f"Клиент: {order.client_name} ({order.contact_person})")
            print(f"Телефон: {order.client_phone}")
            print(f"Статус: {order.status}")
            
            print("\nТовары:")
            for item in order.items:
                print(f"- {item['product_name']}: {item['quantity']} x {item['unit_price']} руб.")
            
            if order.delivery_method_id:
                print(f"\nДоставка: {order.delivery_method_name}")
                print(f"Стоимость доставки: {order.delivery_cost} руб.")
                print(f"Предполагаемая дата доставки: {order.estimated_delivery_date}")
            
            print(f"\nОбщая сумма: {order.total_amount} руб.")
        
        elif choice == "4":
            order_id = int(input("Введите ID заказа: "))
            order = Order.get_by_id(order_id)
            
            if not order:
                print("❌ Заказ не найден!")
                continue
            
            print(f"\nТекущий статус: {order.status}")
            print("Доступные статусы:")
            print("1. В обработке")
            print("2. Отправлен")
            print("3. Доставлен")
            print("4. Отменен")
            
            status_choice = input("Выберите новый статус: ")
            
            if status_choice == "1":
                order.status = "processing"
            elif status_choice == "2":
                order.status = "shipped"
            elif status_choice == "3":
                order.status = "delivered"
            elif status_choice == "4":
                order.status = "cancelled"
            else:
                print("❌ Неверный выбор!")
                continue
            
            order.save()
            print("✅ Статус заказа обновлен.")
        
        elif choice == "0":
            break
        
        else:
            print("❌ Неверный ввод!")

if __name__ == "__main__":
    while True:
        action = show_main_menu()
        
        if action == "1":
            menu_products()
        elif action == "2":
            menu_clients()
        elif action == "3":
            menu_orders()
        elif action == "4":
            pass
        elif action == "0":
            print("Выход из системы.")
            break
        else:
            print("❌ Неверный ввод!")
