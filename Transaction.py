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

    def get(self, i):
        if i == "first_name": return self.__first_name
        if i == "last_name": return self.__last_name
        if i == "username": return self.__username
        if i == "email": return self.__email
        if i == "address": return self.__address
        if i == "address2": return self.__address2
        if i == "country": return self.__country
        if i == "postal": return self.__postal
        if i == "payment_method": return self.__payment_method
        if i == "cc_name": return self.__cc_name
        if i == "cc_number": return self.__cc_number
        if i == "cc_expiration": return self.__cc_expiration
        if i == "cc_cvv": return self.__cc_cvv

    def set(self, i, val):
        if i == "first_name":  self.__first_name = val
        if i == "last_name":  self.__last_name = val
        if i == "username":  self.__username = val
        if i == "email":  self.__email = val
        if i == "address":  self.__address = val
        if i == "address2":  self.__address2 = val
        if i == "country":  self.__country = val
        if i == "postal":  self.__postal = val
        if i == "payment_method": self.__payment_method = val
        if i == "cc_name":  self.__cc_name = val
        if i == "cc_number":  self.__cc_number = val
        if i == "cc_expiration":  self.__cc_expiration = val
        if i == "cc_cvv":  self.__cc_cvv = val



