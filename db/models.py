from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, DateTime, Float

from db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    chat_id = Column(Integer, nullable=False, unique=True)
    phone_number = Column(String(255), unique=True)
    role_id = Column(Integer, ForeignKey('roles.id'))


class User1C(Base):
    __tablename__ = "users_1c"

    id = Column(Integer, primary_key=True)
    ref_1c = Column(String(36), nullable=False)
    description = Column(String(255), nullable=False)
    discount_card_number = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class FiscalCheck(Base):
    __tablename__ = "fiscal_checks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    date_time = Column(DateTime)
    amount = Column(Float, nullable=False)
    fn = Column(Integer, nullable=False)
    fp = Column(Integer, nullable=False)
    doc_number = Column(Integer, nullable=False)
    n = Column(Integer, nullable=False)
