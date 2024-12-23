import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import base, Client, Certificate
from cli import add_certificate_from_console, get_all_certificates, get_certificates_by_client_id
from datetime import datetime


@pytest.fixture(scope="function")
def db_engine():
    """Создает движок базы данных для тестов"""
    engine = create_engine("sqlite:///:memory:")  # Используем in-memory базу данных для тестов
    base.metadata.create_all(engine)
    yield engine
    base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Создает сессию базы данных для каждого теста"""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def sample_clients(db_session):
    """Создает несколько клиентов для тестов"""
    client1 = Client(last_name="Иванов", first_name="Иван", middle_name="Иванович", birth_date="1990-05-15")
    client2 = Client(last_name="Петров", first_name="Петр", middle_name="Петрович", birth_date="1985-10-20")
    db_session.add_all([client1, client2])
    db_session.commit()
    return client1, client2


def test_add_certificate(db_session, sample_clients):
    """Тест на добавление сертификата"""
    client1, client2 = sample_clients
    certificate = Certificate(
        purchase_date="2024-01-20",
        purchaser_id=client1.id,
        price=100.0,
        balance=100.0,
        given_date="2024-02-10",
        recipient_id=client2.id
    )
    db_session.add(certificate)
    db_session.commit()

    # Проверяем, что сертификат добавлен в базу данных
    assert db_session.query(Certificate).count() == 1
    added_certificate = db_session.query(Certificate).first()
    assert added_certificate.purchase_date == "2024-01-20"
    assert added_certificate.purchaser_id == client1.id
    assert added_certificate.price == 100.0
    assert added_certificate.balance == 100.0
    assert added_certificate.given_date == "2024-02-10"
    assert added_certificate.recipient_id == client2.id


def test_add_certificate_no_recipient(db_session, sample_clients):
    """Тест на добавление сертификата без получателя"""
    client1, _ = sample_clients
    certificate = Certificate(
        purchase_date="2024-01-20",
        purchaser_id=client1.id,
        price=100.0,
        balance=100.0,
    )
    db_session.add(certificate)
    db_session.commit()

    assert db_session.query(Certificate).count() == 1
    added_certificate = db_session.query(Certificate).first()
    assert added_certificate.recipient_id is None
    assert added_certificate.given_date is None


def test_get_all_certificates(db_session, sample_clients):
    """Тест на получение всех сертификатов"""
    client1, client2 = sample_clients
    certificate1 = Certificate(
        purchase_date="2024-01-20",
        purchaser_id=client1.id,
        price=100.0,
        balance=100.0,
        given_date="2024-02-10",
        recipient_id=client2.id
    )
    certificate2 = Certificate(
        purchase_date="2024-03-01",
        purchaser_id=client2.id,
        price=200.0,
        balance=200.0,
    )
    db_session.add_all([certificate1, certificate2])
    db_session.commit()

    certificates = get_all_certificates(db_session)

    assert len(certificates) == 2
    assert any(c.purchase_date == "2024-01-20" and c.purchaser_id == client1.id for c in certificates)
    assert any(c.purchase_date == "2024-03-01" and c.purchaser_id == client2.id for c in certificates)


def test_get_certificates_by_client_id(db_session, sample_clients):
    """Тест на получение сертификатов по ID клиента"""
    client1, client2 = sample_clients
    certificate1 = Certificate(
        purchase_date="2024-01-20",
        purchaser_id=client1.id,
        price=100.0,
        balance=100.0,
        given_date="2024-02-10",
        recipient_id=client2.id
    )
    certificate2 = Certificate(
        purchase_date="2024-03-01",
        purchaser_id=client2.id,
        price=200.0,
        balance=200.0,
    )
    certificate3 = Certificate(
        purchase_date="2024-04-01",
        purchaser_id=client1.id,
        price=50.0,
        balance=50.0,
        given_date="2024-05-01",
        recipient_id=client2.id
    )
    db_session.add_all([certificate1, certificate2, certificate3])
    db_session.commit()

    certificates_client1 = get_certificates_by_client_id(db_session, client1.id)
    certificates_client2 = get_certificates_by_client_id(db_session, client2.id)

    assert len(certificates_client1) == 2
    assert any(c.purchase_date == "2024-01-20" for c in certificates_client1)
    assert any(c.purchase_date == "2024-04-01" for c in certificates_client1)

    assert len(certificates_client2) == 3
    assert any(c.purchase_date == "2024-01-20" for c in certificates_client2)
    assert any(c.purchase_date == "2024-03-01" for c in certificates_client2)


def test_add_certificate_from_console(db_session, monkeypatch, sample_clients):
    client1, _ = sample_clients

    # Мокаем input для эмуляции ввода пользователя
    inputs = iter([
        "2024-06-01",  # purchase_date
        str(client1.id),  # purchaser_id
        "150.0",  # price
        "2024-07-01",  # given_date
        str(client1.id)  # recipient_id
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    new_certificate = add_certificate_from_console(db_session)
    assert new_certificate is not None
    assert new_certificate.purchase_date == "2024-06-01"
    assert new_certificate.price == 150.0
    assert new_certificate.balance == 150.0
    assert new_certificate.given_date == "2024-07-01"
    assert new_certificate.recipient_id == client1.id


def test_add_certificate_from_console_no_recipient(db_session, monkeypatch, sample_clients):
    client1, _ = sample_clients

    # Мокаем input для эмуляции ввода пользователя
    inputs = iter([
        "2024-06-01",  # purchase_date
        str(client1.id),  # purchaser_id
        "150.0",  # price
        None  # given_date
    ])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    new_certificate = add_certificate_from_console(db_session)
    assert new_certificate is not None
    assert new_certificate.purchase_date == "2024-06-01"
    assert new_certificate.price == 150.0
    assert new_certificate.balance == 150.0
    assert new_certificate.given_date is None
    assert new_certificate.recipient_id is None
