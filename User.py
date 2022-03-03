class User:
    count_id = 0

    def __init__(self, first_name, last_name, gender, membership, remarks):
        User.count_id += 1
        self.__user_id = User.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__membership = membership
        self.__gender = gender
        self.__remarks = remarks

    def get(self, i):
        if i == "user_id": return self.__user_id
        if i == "first_name": return self.__first_name
        if i == "last_name": return self.__last_name
        if i == "membership": return self.__membership
        if i == "gender": return self.__gender
        if i == "remarks": return self.__remarks

    def set(self, i, val):
        if i == "user_id": self.__user_id = val
        if i == "first_name": self.__first_name = val
        if i == "last_name": self.__last_name = val
        if i == "membership": self.__membership = val
        if i == "gender": self.__gender = val
        if i == "remarks": self.__remarks = val
          
