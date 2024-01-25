from models.expression import Expression


class Variable(Expression):
    def __init__(self, name, variables: dict):
        self.__name = name
        self.__variables = variables

    def evaluate(self) -> float:
        return self.__variables[self.__name]
