class Review:
    count_id = 0

    def __init__(self, ratings, product_name, email, comments):
        Review.count_id += 1
        self.__review_id = Review.count_id
        self.__ratings = ratings
        self.__product_name = product_name
        self.__email = email
        self.__comments = comments

    def get_review_id(self):
        return self.__review_id
    def get_ratings(self):
        return self.__ratings
    def get_product_name(self):
        return self.__product_name
    def get_email(self):
        return self.__email
    def get_comments(self):
        return self.__comments

    def set_review_id(self,review_id):
        self.__review_id = review_id
    def set_ratings(self,ratings):
        self.__ratings = ratings
    def set_product_name(self, product_name):
        self.__product_name = product_name
    def set_email(self,email):
        self.__email = email
    def set_comments(self,comments):
        self.__comments = comments
