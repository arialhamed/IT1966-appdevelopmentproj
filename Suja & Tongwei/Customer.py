# Customer ...
class Customer:
    count_id = 0

# Initiator
    def __init__(self, firstname, lastname, username, email, gender, birth, password, phone_number, address, postal, payment_method, card_number, expiry, security_code):
        Customer.count_id += 1
        self.__customer_id = Customer.count_id
        self.__firstName = firstname
        self.__lastName = lastname
        self.__username = username
        self.__email = email
        self.__gender = gender
        self.__birth = birth
        self.__password = password
        self.__phone_number = phone_number
        self.__address = address
        self.__postal = postal
        self.__payment_method = payment_method
        self.__card_number = card_number
        self.__expiry = expiry
        self.__security_code = security_code

# Accessor Method
    def get_customer_id(self):
        return self.__customer_id

    def get_firstName(self):
        return self.__firstName

    def get_lastName(self):
        return self.__lastName

    def get_username(self):
        return self.__username

    def get_email(self):
        return self.__email

    def get_gender(self):
        return self.__gender

    def get_birth(self):
        return self.__birth

    def get_password(self):
        return self.__password

    def get_phone_number(self):
        return self.__phone_number

    def get_address(self):
        return self.__address

    def get_postal(self):
        return self.__postal

    def get_payment_method(self):
        return self.__payment_method

    def get_card_number(self):
        return self.__card_number

    def get_expiry(self):
        return self.__expiry

    def get_security_code(self):
        return self.__security_code

# Mutator Method
    def set_customer_id(self, customer_id):
        self.__customer_id = customer_id

    def set_firstName(self, firstName):
        self.__firstName = firstName

    def set_lastName(self, lastName):
        self.__lastName = lastName

    def set_username(self, username):
        self.__username = username

    def set_email(self, email):
        self.__email = email

    def set_gender(self, gender):
        self.__gender = gender

    def set_birth(self, birth):
        self.__birth = birth

    def set_password(self, password):
        self.__password = password

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_address(self, address):
        self.__address = address

    def set_postal(self, postal):
        self.__postal = postal

    def set_payment_method(self, payment_method):
        self.__payment_method = payment_method

    def set_card_number(self, card_number):
        self.__card_number = card_number

    def set_expiry(self, expiry):
        self.__expiry = expiry

    def set_security_code(self, security_code):
        self.__security_code = security_code
