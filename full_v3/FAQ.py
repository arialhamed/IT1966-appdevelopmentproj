class FAQ:
    count_id = 0

    def __init__(self, question, username):
        FAQ.count_id += 1
        self.__question_id = FAQ.count_id
        self.__question = question
        self.__answer = ""
        self.__username = username

    def get_id(self): return self.__question_id

    def get_question(self): return self.__question

    def set_question(self, val): self.__question = val

    def get_answer(self): return self.__answer

    def set_answer(self, val): self.__answer = val

    def get_username(self): return self.__username

    def set_username(self, val): self.__username = val
