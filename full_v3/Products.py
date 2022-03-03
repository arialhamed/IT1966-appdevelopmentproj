from uuid import uuid4


class Products:
    def __init__(self , item_name,Price,description,stock):
        self.__product_id = str(uuid4())
        self.__image = None
        self.__item_name = item_name
        self.__Stock = stock
        self.__description = description
        self.__Price = Price
        self.__qty = 0

    def get_products_id(self):
        return self.__product_id

    def get_name(self):
        return self.__item_name

    def get_image(self):
        return self.__image

    def get_stock(self):
        return self.__Stock

    def get_price(self):
        return self.__Price

    def get_description(self):
        return self.__description

    def get_qty(self):
        return self.__qty

    def get_total(self):
        total = self.__qty*self.__Price
        return total

    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_name(self, item_name):
        self.__item_name = item_name

    def set_image(self, image):
        self.__image = image

    def set_stock(self, stock):
        self.__Stock = stock

    def set_price(self, Price):
        self.__Price = Price

    def set_qty(self, qty):
        self.__qty = qty

    def set_description(self, description):
        self.__description = description

    def set_total(self, qty):
        total = qty*self.__Price
        return total

    def add_qty(self,qty):
        self.__qty += qty
        return self.__qty
