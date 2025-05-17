from models.delivery import DeliveryMethod, get_all_delivery_methods

def menu_delivery():
    while True:
        print("\n=== Управление доставкой ===")
        print("1. Список способов доставки")
        print("2. Добавить способ доставки")
        print("3. Удалить способ доставки")
        print("4. Изменить способ доставки")
        print("0. Назад")
        
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