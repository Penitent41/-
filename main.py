from database.db_manager import initialize_db
from ui.menu import show_main_menu, menu_products, menu_clients, menu_orders, menu_delivery

def main():
    initialize_db()
    while True:
        user_choice = show_main_menu()
        if user_choice == "1":
            menu_products()
        elif user_choice == "2":
            menu_clients()
        elif user_choice == "3":
            menu_orders()
        elif user_choice == "4":
            menu_delivery()
        elif user_choice == "0":
            print("Выход из программы. До свидания!")
            break
        else:
            print("❌ Неверный ввод.")

if __name__ == "__main__":
    main()