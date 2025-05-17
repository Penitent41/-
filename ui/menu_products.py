from models.product import Product, get_all_products, get_product_by_id
from models.delivery import get_all_delivery_methods

def menu_products():
    while True:
        print("\n=== Управление товарами ===")
        print("1. Показать все товары")
        print("2. Добавить товар")
        print("3. Удалить товар")
        print("4. Изменить товар")
        print("5. Настроить доставку для товара")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            products = get_all_products()
            print("\nСписок товаров:")
            for p in products:
                delivery_status = "✅" if p.has_delivery else "❌"
                print(f"{p.id}. {p.name} | {p.price} руб. | Наличие: {p.stock} | Доставка: {delivery_status}")
        
        elif choice == "2":
            print("\nДобавление нового товара:")
            name = input("Название: ")
            description = input("Описание: ")
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
            print("✅ Товар добавлен")
        
        elif choice == "3":
            product_id = int(input("ID товара для удаления: "))
            product = Product(id=product_id)
            product.delete()
            print("✅ Товар удален")
        
        elif choice == "4":
            product_id = int(input("ID товара для изменения: "))
            product = get_product_by_id(product_id)
            if product:
                print("\nОставьте поле пустым, чтобы не изменять")
                name = input(f"Название [{product.name}]: ") or product.name
                price = input(f"Цена [{product.price}]: ") or product.price
                stock = input(f"Количество [{product.stock}]: ") or product.stock
                
                updated = Product(
                    id=product_id,
                    name=name,
                    price=float(price),
                    stock=int(stock),
                    has_delivery=product.has_delivery
                )
                updated.save()
                print("✅ Товар обновлен")
        
        elif choice == "5":
            product_id = int(input("ID товара для настройки доставки: "))
            product = get_product_by_id(product_id)
            if product:
                print("\nДоступные способы доставки:")
                methods = get_all_delivery_methods()
                for m in methods:
                    print(f"{m.id}. {m.name} ({m.base_cost} руб.)")
        
        
        elif choice == "0":
            break