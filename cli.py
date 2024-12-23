from datetime import datetime
from models import Client, Visit, Certificate
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


def add_certificate_from_console(db: Session):
    purchase_date_str = input("Введите дату приобретения сертификата (ГГГГ-ММ-ДД): ")
    try:
        datetime.strptime(purchase_date_str, "%Y-%m-%d")
    except ValueError:
        print("Неверный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД.")
        return None

    purchaser_id_str = input("Введите ID клиента, который приобрел сертификат: ")
    try:
        purchaser_id = int(purchaser_id_str)
        purchaser = db.query(Client).filter(Client.id == purchaser_id).first()
        if not purchaser:
            print("Клиент с таким id не найден")
            return None
    except ValueError:
        print("Неверный формат ID клиента.")
        return None

    price_str = input("Введите стоимость сертификата: ")
    try:
        price = float(price_str)
    except ValueError:
        print("Неверный формат стоимости сертификата")
        return None

    balance = price

    given_date = input("Введите дату вручения сертификата (ГГГГ-ММ-ДД, или оставьте пустым, если еще не вручен): ")
    recipient_id = None
    recipient = None
    if given_date:
        try:
            datetime.strptime(given_date, "%Y-%m-%d")
            recipient_id_str = input("Введите ID клиента, которому вручен сертификат: ")
            try:
                recipient_id = int(recipient_id_str)
                recipient = db.query(Client).filter(Client.id == recipient_id).first()
                if not recipient:
                    print("Клиент с таким id не найден")
                    return None
            except ValueError:
                print("Неверный формат id клиента-получателя")
                return None
        except ValueError:
            print("Неверный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД.")
            return None

    new_certificate = Certificate(purchase_date=purchase_date_str, purchaser_id=purchaser_id, price=price,
                                  balance=balance, given_date=given_date, recipient_id=recipient_id)
    db.add(new_certificate)
    db.commit()
    print("Сертификат успешно добавлен.")
    return new_certificate


def get_all_clients(db: Session):
    return db.query(Client).all()


def get_visits_by_client_id(db: Session, client_id: int):
    return db.query(Visit).filter(Visit.client_id == client_id).all()


def get_all_certificates(db: Session):
    return db.query(Certificate).all()


def get_certificates_by_client_id(db: Session, client_id: int):
    return db.query(Certificate).filter(
        (Certificate.purchaser_id == client_id) | (Certificate.recipient_id == client_id)).all()


def get_client_by_id(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()
