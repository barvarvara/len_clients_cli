from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship

base = declarative_base()


class Client(base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    birth_date = Column(String)  # Строка т.к. вводим в формате ГГГГ-ММ-ДД

    visits = relationship("Visit", back_populates="client")
    certificates_purchased = relationship("Certificate", back_populates="purchaser",
                                          foreign_keys="[Certificate.purchaser_id]")
    certificates_received = relationship("Certificate", back_populates="recipient",
                                         foreign_keys="[Certificate.recipient_id]")

    def __str__(self):
        return f"ФИО: {self.last_name} {self.first_name} {self.middle_name}, Дата рождения: {self.birth_date}"


class Visit(base):
    __tablename__ = 'visits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'))
    visit_date = Column(String)  # Строка т.к. вводим в формате ГГГГ-ММ-ДД
    description = Column(String)

    client = relationship("Client", back_populates="visits")

    def __str__(self):
        return f"Дата посещения: {self.visit_date}, Описание: {self.description}"
