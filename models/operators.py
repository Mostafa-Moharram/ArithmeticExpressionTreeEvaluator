from models.operator_base import OperatorBase


class OperatorPlus(OperatorBase):
    def evaluate(self) -> float:
        return self.expressions[0].evaluate() + self.expressions[1].evaluate()

class OperatorMinus(OperatorBase):
    def evaluate(self) -> float:
        return self.expressions[0].evaluate() - self.expressions[1].evaluate()

class OperatorMul(OperatorBase):
    def evaluate(self) -> float:
        return self.expressions[0].evaluate() * self.expressions[1].evaluate()

class OperatorDiv(OperatorBase):
    def evaluate(self) -> float:
        return self.expressions[0].evaluate() / self.expressions[1].evaluate()
