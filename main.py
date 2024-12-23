from cli import (
    add_client_from_console,
    get_all_clients,
    get_visits_by_client_id,
    get_client_by_id
)
from database import get_db


def main():
    while True:
        print("\nМеню:")
        print("1. Добавить клиента")
        print("2. Вывести всех клиентов")
        print("3. Вывести посещения клиента")
        print("4. Выход")
        choice = input("Выберите действие: ")

        db = next(get_db())

        if choice == "1":
            add_client_from_console(db)
        elif choice == "2":
            all_clients = get_all_clients(db)
            if all_clients:
                print("\nВсе клиенты в базе:")
                for client in all_clients:
                    print(client)
            else:
                print("В базе нет клиентов")
        elif choice == "3":
            client_id_str = input("Введите id клиента для просмотра его посещений: ")
            try:
                client_id = int(client_id_str)
                client = get_client_by_id(db, client_id)
                if client:
                    print(f"\nПосещения клиента {client}:")
                    visits = get_visits_by_client_id(db, client_id)
                    if visits:
                        for visit in visits:
                            print(visit)
                    else:
                        print("У данного клиента нет посещений")
                else:
                    print("Клиент с таким id не найден")
            except ValueError:
                print("Неверный формат id клиента.")
        elif choice == "4":
            break
        else:
            print("Неверный выбор. Пожалуйста, повторите.")


if __name__ == "__main__":
    main()
