from uuid import uuid4
class Products:
    def __init__(self, name, price, description, quantity):
        self.__products_id = str(uuid4())
        self.__image = None
        self.__name = name
        self.__price = price
        self.__description = description
        self.__quantity = quantity


    def get_products_id(self):
        return self.__products_id

    def get_image(self):
        return self.__image

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_description(self):
        return self.__description

    def get_quantity(self):
        return self.__quantity

    def set_products_id(self, products_id):
        self.__products_id = products_id

    def set_image(self, image):
        self.__image = image

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_description(self, description):
        self.__description = description

    def set_quantity(self, quantity):
        self.__quantity = quantity
