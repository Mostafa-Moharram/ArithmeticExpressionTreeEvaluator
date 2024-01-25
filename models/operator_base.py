from models.expression import Expression


class OperatorBase(Expression):
    def __init__(self):
        self.expressions = []
