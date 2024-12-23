from datetime import datetime
from models import Client, Visit
from sqlalchemy.orm import Session


def add_client_from_console(db: Session):
    last_name = input("Введите фамилию клиента: ")
    first_name = input("Введите имя клиента: ")
    middle_name = input("Введите отчество клиента: ")
    birth_date_str = input("Введите дату рождения клиента (ГГГГ-ММ-ДД): ")
    try:
        datetime.strptime(birth_date_str, "%Y-%m-%d")
    except ValueError:
        print("Неверный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД.")
        return None

    new_client = Client(last_name=last_name, first_name=first_name, middle_name=middle_name, birth_date=birth_date_str)
    db.add(new_client)
    db.commit()
    print("Клиент успешно добавлен.")
    return new_client


def get_all_clients(db: Session):
    return db.query(Client).all()


def get_visits_by_client_id(db: Session, client_id: int):
    return db.query(Visit).filter(Visit.client_id == client_id).all()


def get_client_by_id(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()
