from cli import (
    add_client_from_console,
    get_all_clients,
    get_visits_by_client_id,
    add_certificate_from_console,
    get_all_certificates,
    get_certificates_by_client_id,
    get_client_by_id
)
from database import get_db

MENU_OPTIONS = {
    "1": "Добавить клиента",
    "2": "Вывести всех клиентов",
    "3": "Вывести посещения клиента",
    "4": "Добавить сертификат",
    "5": "Вывести все сертификаты",
    "6": "Вывести сертификаты клиента",
    "7": "Выход",
}


def _display_menu():
    """Отображает меню пользователю."""
    print("\nМеню:")
    for key, value in MENU_OPTIONS.items():
        print(f"{key}. {value}")
    return input("Выберите действие: ")


def main():
    while True:
        choice = _display_menu()

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
            add_certificate_from_console(db)
        elif choice == "5":
            all_certificates = get_all_certificates(db)
            if all_certificates:
                print("\nВсе сертификаты в базе:")
                for certificate in all_certificates:
                    print(certificate)
            else:
                print("В базе нет сертификатов")
        elif choice == "6":
            client_id_str = input("Введите ID клиента для просмотра его сертификатов: ")
            try:
                client_id = int(client_id_str)
                client = get_client_by_id(db, client_id)
                if client:
                    print(f"\nСертификаты клиента {client}:")
                    certificates = get_certificates_by_client_id(db, client_id)
                    if certificates:
                        for certificate in certificates:
                            print(certificate)
                    else:
                        print("У данного клиента нет сертификатов")
                else:
                    print("Клиент с таким ID не найден")
            except ValueError:
                print("Неверный формат id клиента.")
        elif choice == "7":
            break
        else:
            print("Неверный выбор. Пожалуйста, повторите.")


if __name__ == "__main__":
    main()
