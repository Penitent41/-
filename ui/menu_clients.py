from models.client import Client, get_all_clients, get_client_by_id

def menu_clients():
    while True:
        print("\n=== Управление клиентами ===")
        print("1. Список клиентов")
        print("2. Добавить клиента")
        print("3. Удалить клиента")
        print("4. Изменить клиента")
        print("0. Назад")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            clients = get_all_clients()
            print("\nСписок клиентов:")
            for c in clients:
                print(f"{c.id}. {c.name} | {c.contact_person} | {c.phone} | {c.address}")
        
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
            client_id = int(input("ID клиента для удаления: "))
            client = Client(id=client_id)
            client.delete()
            print("✅ Клиент удален")
        
        elif choice == "4":
            client_id = int(input("ID клиента для изменения: "))
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