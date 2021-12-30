from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Index, Numeric, String, Table, Text, text
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Client(Base):
    __tablename__ = 'Clients'
    __table_args__ = (
        Index('PupilsBtree', 'Surname', 'Patronymic', 'Name'),
    )

    Id = Column(BigInteger, primary_key=True, server_default=text("nextval('\"Pupils_Id_seq\"'::regclass)"))
    Name = Column(String(20), nullable=False)
    Patronymic = Column(String(20), nullable=False)
    Surname = Column(String(20), nullable=False, index=True)


class Seller(Base):
    __tablename__ = 'Sellers'

    id = Column(BigInteger, primary_key=True, unique=True, server_default=text("nextval('\"Teachers_id_seq\"'::regclass)"))
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)


class Price(Base):
    __tablename__ = 'Prices'

    id = Column(BigInteger, primary_key=True, unique=True, server_default=text("nextval('\"Marks_id_seq\"'::regclass)"))
    time = Column(DateTime, nullable=False)
    clientsid = Column(ForeignKey('Clients.Id'), nullable=False)
    sellersid = Column(ForeignKey('Sellers.id'), nullable=False)
    price = Column(Float, nullable=False)

    Client = relationship('Client')
    Seller = relationship('Seller')


class Product(Base):
    __tablename__ = 'Products'

    id = Column(BigInteger, primary_key=True, unique=True, server_default=text("nextval('\"Subjects_id_seq\"'::regclass)"))
    name = Column(String(20), nullable=False)
    pricesid = Column(ForeignKey('Prices.id'), nullable=False)

    Price = relationship('Price')


class ClientsProduct(Base):
    __tablename__ = 'ClientsProducts'

    id = Column(BigInteger, primary_key=True, unique=True, server_default=text("nextval('\"PupilsSubjects_id_seq\"'::regclass)"))
    clientsid = Column(ForeignKey('Clients.Id'), nullable=False)
    productsid = Column(ForeignKey('Products.id'), nullable=False)

    Client = relationship('Client')
    Product = relationship('Product')


class SellersProduct(Base):
    __tablename__ = 'SellersProducts'

    id = Column(BigInteger, primary_key=True, unique=True, server_default=text("nextval('\"TeachersSubjects_id_seq\"'::regclass)"))
    sellersid = Column(ForeignKey('Sellers.id'), nullable=False)
    productsid = Column(ForeignKey('Products.id'), nullable=False)

    Product = relationship('Product')
    Seller = relationship('Seller')
