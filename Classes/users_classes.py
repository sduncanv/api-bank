from pydantic import BaseModel, EmailStr, Field, validator


class RegisterUser(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    document: str
    phone_number: str
    email: EmailStr
    age: int
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=8)

    @validator('name')
    def name_caracters(cls, name):
        if not name.replace(" ", "").isalpha():
            raise ValueError('The name must contain only letters.')

        if name.lower() == 'true' or name.lower() == 'false':
            raise ValueError('Enter a valid name, not a boolean value')

        return name

    @validator('document')
    def document_length(cls, document):
        if len(document) < 5:
            raise ValueError('Enter a valid document, add more characters')

        if ' ' in document:
            raise ValueError('The document must not contain spaces.')

        if not document.replace(" ", "").isnumeric():
            raise ValueError('The document must be numeric.')

        return document

    @validator('phone_number')
    def phone_number_length(cls, phone_number):
        if len(phone_number) != 13:
            raise ValueError('The phone number must have 13 characters.')

        if ' ' in phone_number:
            raise ValueError('The phone_number must not contain spaces.')

        if not phone_number[1:].replace(" ", "").isnumeric():
            raise ValueError('The phone_number must be numeric.')

        return phone_number

    @validator('username')
    def username_caracters(cls, username):
        if not len(username) in range(5, 51):
            raise ValueError('The username must have 5 to 50 characters')

        if ' ' in username:
            raise ValueError('The username must not contain spaces.')

        if not username.replace(" ", "").isalnum():
            raise ValueError('The username must be alphanumeric.')

        return username

    @validator('password')
    def password_length(cls, password):
        if len(password) < 8:
            raise ValueError('Password must be 8 or more characters.')

        if ' ' in password:
            raise ValueError('The password must not contain spaces.')

        return password


class UpdateUser(BaseModel):
    user_id: int
    name: str = Field(min_length=2, max_length=50)
    phone_number: str
    email: EmailStr
    age: int

    @validator('name')
    def name_caracters(cls, name):
        if not name.replace(" ", "").isalpha():
            raise ValueError('The name must contain only letters.')

        if name.lower() == 'true' or name.lower() == 'false':
            raise ValueError('Enter a valid name, not a boolean value')

        return name

    @validator('phone_number')
    def phone_number_length(cls, phone_number):
        if len(phone_number) != 13:
            raise ValueError('The phone number must have 13 characters.')

        if ' ' in phone_number:
            raise ValueError('The phone_number must not contain spaces.')

        if not phone_number[1:].replace(" ", "").isnumeric():
            raise ValueError('The phone_number must be numeric.')

        return phone_number


class LoginTokens(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    password: str = Field(min_length=8)

    @validator('username')
    def username_caracters(cls, username):
        if not len(username) in range(5, 51):
            raise ValueError('The username must have 5 to 50 characters')

        if ' ' in username:
            raise ValueError('The username must not contain spaces.')

        if not username.replace(" ", "").isalnum():
            raise ValueError('The username must be alphanumeric.')

        return username

    @validator('password')
    def password_length(cls, password):
        if len(password) < 8:
            raise ValueError('Password must be 8 or more characters.')

        if ' ' in password:
            raise ValueError('The password must not contain spaces.')

        return password


class AssignPermissions(BaseModel):
    user: str
    permission: list


class RegisterCustomer(BaseModel):
    name: str
    document: str
    phone_number: str
    email: EmailStr
    age: int
    address: str = Field(min_length=5)
    city: str = Field(min_length=3)
    profession: str = Field(min_length=5)
    selfie: str

    @validator('name')
    def name_caracters(cls, name):
        if not name.replace(" ", "").isalpha():
            raise ValueError('The name must contain only letters.')

        if name.lower() == 'true' or name.lower() == 'false':
            raise ValueError('Enter a valid name, not a boolean value')

        return name

    @validator('document')
    def document_length(cls, document):
        if len(document) < 5:
            raise ValueError('Enter a valid document, add more characters')

        if ' ' in document:
            raise ValueError('The document must not contain spaces.')

        if not document.replace(" ", "").isnumeric():
            raise ValueError('The document must be numeric.')

        return document

    @validator('phone_number')
    def phone_number_length(cls, phone_number):
        if len(phone_number) != 13:
            raise ValueError('The phone number must have 13 characters.')

        if ' ' in phone_number:
            raise ValueError('The phone_number must not contain spaces.')

        if not phone_number[1:].replace(" ", "").isnumeric():
            raise ValueError('The phone_number must be numeric.')

        return phone_number

    @validator('city')
    def city_caracters(cls, city):
        if not city.replace(" ", "").isalpha():
            raise ValueError('The city must contain only letters.')

        if city.lower() == 'true' or city.lower() == 'false':
            raise ValueError('Enter a valid city, not a boolean value')

        return city


class DeleteCustomer(BaseModel):
    customer_id = int


class SavingsAccountUpdate(BaseModel):
    account_id: int
    current_balance: str
    city: str = Field(min_length=3)
    country: str = Field(min_length=3)
    active: int


class SavingsAccountCreate(BaseModel):
    customer_id: int
    account_number: str
    current_balance: str
    activated_at: str
    city: str = Field(min_length=3)
    country: str = Field(min_length=3)

    @validator('account_number')
    def account_number_length(cls, account_number):
        if len(account_number) < 12:
            raise ValueError('Enter a valid account_number, must be 12.')

        if ' ' in account_number:
            raise ValueError('The account_number must not contain spaces.')

        if not account_number.replace(" ", "").isnumeric():
            raise ValueError('The account_number must be numeric.')

        return account_number

    @validator('current_balance')
    def current_balance_length(cls, current_balance):
        if len(current_balance) < 1:
            raise ValueError('Enter a valid current_balance.')

        if ' ' in current_balance:
            raise ValueError('The current_balance must not contain spaces.')

        if not current_balance.replace(" ", "").isnumeric():
            raise ValueError('The current_balance must be numeric.')

        return current_balance

    @validator('city')
    def city_caracters(cls, city):
        if not city.replace(" ", "").isalpha():
            raise ValueError('The city must contain only letters.')

        if city.lower() == 'true' or city.lower() == 'false':
            raise ValueError('Enter a valid city, not a boolean value')

        return city

    @validator('country')
    def country_caracters(cls, country):
        if not country.replace(" ", "").isalpha():
            raise ValueError('The country must contain only letters.')

        if country.lower() == 'true' or country.lower() == 'false':
            raise ValueError('Enter a valid country, not a boolean value')

        return country


class TransactionCreate(BaseModel):
    customer_id: int
    account_number: str
    transaction_date: str
    trade_name: str = Field(min_length=4)
    transaction_value: int
    trade_status: int

    @validator('account_number')
    def account_number_length(cls, account_number):
        if len(account_number) < 10:
            raise ValueError('Enter a valid account_number.')

        if ' ' in account_number:
            raise ValueError('The account_number must not contain spaces.')

        if not account_number.replace(" ", "").isnumeric():
            raise ValueError('The account_number must be numeric.')

        return account_number

    @validator('trade_status')
    def trade_status_length(cls, trade_status):
        if trade_status not in range(0, 3):
            raise ValueError('Choose a valid state')

        return trade_status


class CreateCredits(BaseModel):
    customer_id: int
    credit_value: int
    fee: int
    months_term: int
    payment_date: int


class CreateInstallments(BaseModel):
    credit_id: int
    installments_value: int
    installments_date: str


class VerifyId(BaseModel):
    id = int


class VerifyUsername(BaseModel):
    username = str
