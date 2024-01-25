from models.expression import Expression

class Constant(Expression):
    def __init__(self, value: float):
        self.__value = value

    def evaluate(self) -> float:
        return self.__value
