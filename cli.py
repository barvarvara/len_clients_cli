from datetime import datetime
from models import Client, Visit, Certificate
from sqlalchemy.orm import Session

DATE_FORMAT = "%Y-%m-%d"


def _validate_date_format(date_str):
    """Проверяет формат даты."""
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        return False


def _get_client_by_id(db: Session, client_id: int):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        print(f"Клиент с ID {client_id} не найден.")
        return None
    return client


def add_client_from_console(db: Session):
    last_name = input("Введите фамилию клиента: ")
    first_name = input("Введите имя клиента: ")
    middle_name = input("Введите отчество клиента: ")
    birth_date_str = input(f"Введите дату рождения клиента ({DATE_FORMAT}): ")

    if not _validate_date_format(birth_date_str):
        print(f"Неверный формат даты. Пожалуйста, введите дату в формате {DATE_FORMAT}.")
        return None

    new_client = Client(last_name=last_name, first_name=first_name, middle_name=middle_name, birth_date=birth_date_str)
    db.add(new_client)
    db.commit()
    print("Клиент успешно добавлен.")
    return new_client


def add_certificate_from_console(db: Session):
    purchase_date_str = input(f"Введите дату приобретения сертификата ({DATE_FORMAT}): ")
    if not _validate_date_format(purchase_date_str):
        print(f"Неверный формат даты. Пожалуйста, введите дату в формате {DATE_FORMAT}.")
        return None

    purchaser_id_str = input("Введите ID клиента, который приобрел сертификат: ")
    try:
        purchaser_id = int(purchaser_id_str)
        purchaser = _get_client_by_id(db, purchaser_id)
        if not purchaser:
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

    given_date_str = input(
        f"Введите дату вручения сертификата ({DATE_FORMAT}, или оставьте пустым, если еще не вручен): ")
    recipient_id = None
    if given_date_str:
        if not _validate_date_format(given_date_str):
            print(f"Неверный формат даты. Пожалуйста, введите дату в формате {DATE_FORMAT}.")
            return None
        recipient_id_str = input("Введите ID клиента, которому вручен сертификат: ")
        try:
            recipient_id = int(recipient_id_str)
            recipient = _get_client_by_id(db, recipient_id)
            if not recipient:
                return None
        except ValueError:
            print("Неверный формат id клиента-получателя")
            return None
    new_certificate = Certificate(
        purchase_date=purchase_date_str,
        purchaser_id=purchaser_id,
        price=price,
        balance=balance,
        given_date=given_date_str,
        recipient_id=recipient_id
    )
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
    return _get_client_by_id(db, client_id)
