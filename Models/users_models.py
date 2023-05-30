from datetime import datetime

from sqlalchemy import (
    MetaData, Table, Column, Integer, String, DateTime, Boolean, BigInteger
)

from Database.connection import Base, engine

metadata = MetaData()


class User(Base):
    __tablename__ = 'users'

    user_id = Column('user_id', Integer, primary_key=True)
    name = Column('name', String(50), nullable=False)
    document = Column('document', Integer, nullable=False)
    phone_number = Column('phone_number', String(13), nullable=False)
    email = Column('email', String(50), nullable=False)
    age = Column('age', Integer, nullable=False)
    username = Column('username', String(50), nullable=False)
    password = Column('password', String(500), nullable=False)
    created_at = Column(
        'created_at', DateTime, nullable=False, default=datetime.now()
    )

    def __str__(self) -> str:
        return self.name


class Permission(Base):
    __tablename__ = 'permissions'

    permission_id = Column('permission_id', Integer, primary_key=True)
    user = Column('user', String(50), nullable=False)
    permission = Column('permission', Integer)

    def __str__(self) -> str:
        return str(self.permission_id)


class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column('customer_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, nullable=False)
    name = Column('name', String(50), nullable=False)
    document = Column('document', Integer, nullable=False)
    phone_number = Column('phone_number', String(13), nullable=False)
    email = Column('email', String(50), nullable=False)
    age = Column('age', Integer, nullable=False)
    address = Column('address', String(50), nullable=False)
    city = Column('city', String(50), nullable=False)
    profession = Column('profession', String(50), nullable=False)
    selfie = Column('selfie', String(500), nullable=False)
    active = Column('active', Boolean, default=True)
    created_at = Column(
        'created_at', DateTime, nullable=False, default=datetime.now()
    )

    def __str__(self) -> str:
        return self.name


class SavingsAccounts(Base):
    __tablename__ = 'savings_accounts'

    account_id = Column('account_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, nullable=False)
    customer_id = Column('customer_id', String(50), nullable=False)
    account_number = Column('account_number', Integer, nullable=False)
    current_balance = Column('current_balance', Integer, nullable=False)
    activated_at = Column('activated_at', String(20), nullable=False)
    city = Column('city', String(50), nullable=False)
    country = Column('country', String(50), nullable=False)
    active = Column('active', Boolean, default=True)

    def __str__(self) -> str:
        return str(self.account_id)


class Transactions(Base):
    __tablename__ = 'transactions'

    transactions_id = Column('transactions_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, nullable=False)
    customer_id = Column('customer_id', Integer, nullable=False)
    account_number = Column('account_number', Integer, nullable=False)
    transaction_date = Column(
        'transaction_date', String(20), nullable=False
    )
    trade_name = Column('trade_name', String(50), nullable=False)
    transaction_value = Column('transaction_value', String(50), nullable=False)
    current_balance = Column('current_balance', Integer, nullable=False)
    ending_balance = Column(
        'ending_balance', Integer, nullable=False, default=0
    )
    trade_status = Column('trade_status', Integer, default=0)

    def __str__(self) -> str:
        return str(self.transactions_id)


class Credit(Base):
    __tablename__ = 'credits'

    credit_id = Column('credit_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, nullable=False)
    customer_id = Column('customer_id', Integer, nullable=False)
    credit_value = Column('credit_value', BigInteger, nullable=False)
    fee = Column('fee', Integer, nullable=False)
    months_term = Column('months_term', Integer, nullable=False)
    payment_date = Column('payment_date', Integer, nullable=False)
    dues_paid = Column('dues_paid', Integer, nullable=False)
    next_payment = Column('next_payment', String(20), nullable=False)
    last_payment = Column('last_payment', String(20), nullable=False)
    status_credit = Column(
        'status_credit', Boolean, nullable=True, default=1
    )
    current_balance = Column('current_balance', BigInteger, nullable=False)
    created_at = Column('created_at', nullable=False, default=datetime.now())

    def __str__(self) -> str:
        return str(self.credit_id)


class Installment(Base):
    __tablename__ = 'installments'

    installment_id = Column('installment_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, nullable=False)
    credit_id = Column('credit_id', Integer, nullable=False)
    installment_value = Column('installment_value', BigInteger, nullable=False)
    installment_date = Column('installment_date', String(20), nullable=False)

    def __str__(self) -> str:
        return str(self.installment_id)


users = Table(
    'users',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('name', String(50), nullable=False),
    Column('document', Integer, nullable=False),
    Column('phone_number', String(13), nullable=False),
    Column('email', String(50), nullable=False),
    Column('age', Integer, nullable=False),
    Column('username', String(50), nullable=False),
    Column('password', String(500), nullable=False),
    Column(
        'created_at', DateTime, nullable=False, default=datetime.now()
    )
)


users = Table(
    'permissions',
    metadata,
    Column('permission_id', Integer, primary_key=True),
    Column('user', String(50), nullable=False),
    Column('permission', Integer)
)


customers = Table(
    'customers',
    metadata,
    Column('customer_id', Integer, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('name', String(50), nullable=False),
    Column('document', Integer, nullable=False),
    Column('phone_number', String(13), nullable=False),
    Column('email', String(50), nullable=False),
    Column('age', Integer, nullable=False),
    Column('address', String(50), nullable=False),
    Column('city', String(50), nullable=False),
    Column('profession', String(50), nullable=False),
    Column('selfie', String(500), nullable=False),
    Column('active', Boolean, default=True),
    Column(
        'created_at', DateTime, nullable=False, default=datetime.now()
    )
)

savings_accounts = Table(
    'savings_accounts',
    metadata,
    Column('account_id', Integer, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('customer_id', Integer, nullable=False),
    Column('account_number', BigInteger, nullable=False),
    Column('current_balance', BigInteger, nullable=False),
    Column(
        'activated_at', String(20), nullable=False
    ),
    Column('city', String(50), nullable=False),
    Column('country', String(50), nullable=False),
    Column('active', Boolean, default=True),
)

transactions = Table(
    'transactions',
    metadata,
    Column('transactions_id', Integer, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('customer_id', Integer, nullable=False),
    Column('account_number', BigInteger, nullable=False),
    Column(
        'transaction_date', String(20), nullable=False
    ),
    Column('trade_name', String(50), nullable=False),
    Column('transaction_value', String(50), nullable=False),
    Column('current_balance', BigInteger, nullable=False),
    Column('ending_balance', BigInteger, nullable=False),
    Column('trade_status', Integer, default=0)
)

credits = Table(
    'credits',
    metadata,
    Column('credit_id', Integer, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('customer_id', Integer, nullable=False),
    Column('credit_value', BigInteger, nullable=False),
    Column('fee', Integer, nullable=False),
    Column('months_term', Integer, nullable=False),
    Column('payment_date', Integer, nullable=False),
    Column('dues_paid', Integer, nullable=False),
    Column('next_payment', String(20), nullable=False),
    Column('last_payment', String(20), nullable=False),
    Column('status_credit', Boolean, default=1),
    Column('current_balance', BigInteger, nullable=False),
    Column(
        'created_at', DateTime, nullable=False, default=datetime.now()
    ),
)

installments = Table(
    'installments',
    metadata,
    Column('installment_id', Integer, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('credit_id', Integer, nullable=False),
    Column('installment_value', BigInteger, nullable=False),
    Column('installment_date', String(20), nullable=False)
)


# metadata.drop_all(engine)
metadata.create_all(engine)
