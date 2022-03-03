class Transaction:
    def __init__(self, first_name, last_name, username, email, address, address2, country, postal, payment_method, cc_name, cc_number, cc_expiration, cc_cvv, ):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__username = username
        self.__email = email
        self.__address = address
        self.__address2 = address2
        self.__country = country
        self.__postal = postal
        self.__payment_method = payment_method
        self.__cc_name = cc_name
        self.__cc_number = cc_number
        self.__cc_expiration = cc_expiration
        self.__cc_cvv = cc_cvv
    def get_first_name(self):
        return self.__first_name
    def get_last_name(self):
        return self.__last_name
    def get_username(self):
        return self.__username
    def get_email(self):
        return self.__email
    def get_address(self):
        return self.__address
    def get_address2(self):
        return self.__address2
    def get_country(self):
        return self.__country
    def get_postal(self):
        return self.__postal
    def get_payment_method(self):
        return self.__payment_method
    def get_cc_name(self):
        return self.__cc_name
    def get_cc_number(self):
        return self.__cc_number
    def get_cc_expiration(self):
        return self.__cc_expiration
    def get_cc_cvv(self):
        return self.__cc_cvv

    def set_first_name(self,name):
        self.__first_name = name
        return self.__first_name
    def set_last_name(self,name):
        self.__last_name = name
        return self.__last_name
    def set_username(self,username):
        self.__username = username
        return self.__username
    def set_email(self,email):
        self.__email = email
        return self.__email
    def set_address(self,address):
        self.__address = address
        return self.__address
    def set_address2(self,address2):
        self.__address2 = address2
        return self.__address2
    def set_country(self,country):
        self.__country =country
        return self.__country
    def set_postal(self,postal):
        self.__postal=postal
        return self.__postal
    def set_payment_method(self,payment):
        self.__payment_method =payment
        return self.__payment_method
    def set_cc_name(self,name):
        self.__cc_name = name
        return self.__cc_name
    def set_cc_number(self,number):
        self.__cc_number = number
        return self.__cc_number
    def set_cc_expiration(self,expire):
        self.__cc_expiration = expire
        return self.__cc_expiration
    def set_cc_cvv(self,cvv):
        self.__cvv = cvv
        return self.__cc_cvv
