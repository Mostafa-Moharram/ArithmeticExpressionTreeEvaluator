import math
from models.constant import Constant
from models.expression import Expression
from models.operator_base import OperatorBase
from models.operators import OperatorDiv, OperatorMinus, OperatorMul, OperatorPlus
from models.variable import Variable


class ExpressionModel:
    def __init__(self) -> None:
        self.__expressions = []
        self.__has_parent = []
        self.__expressions_with_no_parent_count = 0
        self.__variables = dict()

    def __add_expression(self, e: Expression):
        index = len(self.__expressions)
        self.__expressions.append(e)
        self.__has_parent.append(False)
        self.__expressions_with_no_parent_count += 1
        return index

    def create_operator(self, operator_str: str) -> int:
        if operator_str == '+':
            return self.__add_expression(OperatorPlus())
        if operator_str == '-':
            return self.__add_expression(OperatorMinus())
        if operator_str == '*':
            return self.__add_expression(OperatorMul())
        if operator_str == '/':
            return self.__add_expression(OperatorDiv())
        raise ValueError('Unknown operator.')

    def create_constant(self, value: float) -> int:
        if math.isfinite(value):
            return self.__add_expression(Constant(value))
        raise ValueError('Input is either infinity or NaN.')

    def create_variable(self, name: str) -> int:
        self.__variables[name] = None
        return self.__add_expression(Variable(name, self.__variables))

    def can_be_parent_of(self, parent_id: int, child_id: int) -> bool:
        if parent_id < 0 or len(self.__expressions) <= parent_id:
            return False
        if child_id < 0 or len(self.__expressions) <= child_id:
            return False
        if not isinstance(parent_id, OperatorBase):
            return False
        parent: OperatorBase = self.__expressions[parent_id]
        return len(parent.expressions) < 2

    def set_parent_of(self, parent_id: int, child_id: int):
        if parent_id < 0 or len(self.__expressions) <= parent_id:
            raise IndexError('{parent_id} is out of bounds.')
        if child_id < 0 or len(self.__expressions) <= child_id:
            raise IndexError('{child_id} is out of bounds.')
        if not isinstance(parent_id, OperatorBase):
            raise ValueError('{parent_id} is not of type Operator')
        parent: OperatorBase = self.__expressions[parent_id]
        if len(parent.expressions) > 1:
            raise MemoryError('Operator {parent_id} has too many operands.')
        parent.expressions.append(self.__expressions[child_id])
        if not self.__has_parent[child_id]:
            self.__expressions_with_no_parent_count -= 1
            self.__has_parent[child_id] = True

    @property
    def variables(self) -> set:
        return set(self.__variables.keys())

    def evaluate(self, variables: dict) -> float:
        if len(self.__expressions) == 0:
            return 0
        if self.__expressions_with_no_parent_count != 1:
            raise ValueError('Input expression is not a tree.')
        index = -1
        for p in self.__has_parent:
            index += 1
            if not p:
                break
        for key in self.__variables.keys():
            if key not in variables:
                raise ValueError('Variable {key} is not specified.')
            value = variables[key]
            if not math.isfinite(value):
                raise ValueError('Variable {key} value is infinity or NaN.')
            self.__variables[key] = value
        return self.__expressions[index].evaluate()
