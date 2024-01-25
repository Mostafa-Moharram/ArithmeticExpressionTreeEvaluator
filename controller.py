import math
from model import ExpressionModel
from validators import try_parse_float, validate_variable_name
from view import ExpressionView

class ExpressionController:
    def __init__(self, model: ExpressionModel) -> None:
        self.__model = model

    def create_operator(self, view: ExpressionView, operator: str):
        try:
            model_id = self.__model.create_operator(operator)
            view.add_operator(operator, model_id)
        except ValueError as ve:
            view.show_error('Invalid input', ve.args[0])

    def create_constant(self, view: ExpressionView, value_str: str):
        result = try_parse_float(value_str)
        if result[0]:
            model_id = self.__model.create_constant(result[1])
            view.add_constant(str(result[1]), model_id)
        else:
            view.show_error('Invalid Input', result[1])

    def create_variable(self, view: ExpressionView, name: str):
        validation_result = validate_variable_name(name)
        if validation_result[0]:
            model_id = self.__model.create_variable(name)
            view.add_variable(name, model_id)
        else:
            view.show_error('Invaid Input', validation_result[1])

    def set_parent_of(self, view: ExpressionView, parent_id: int, child_id: int) -> None:
        validation_result = self.__model.can_be_parent_of(parent_id, child_id)
        if not validation_result[0]:
            view.show_error('Invalid Connection', validation_result[1])
            return
        try:
            self.__model.set_parent_of(parent_id, child_id)
            view.form_parenting_connection(parent_id, child_id)
        except Exception as e:
            view.show_error('Unknown error', e.args[0])

    def evaluate_expression(self, view: ExpressionView, variable_keyvalue: dict):
        for name in self.__model.variables:
            if name not in variable_keyvalue:
                view.show_error('Invalid Input', f'Variable `{name}` value not specified')
                return
            result = try_parse_float(variable_keyvalue[name])
            if not result[0] or not math.isfinite(result[1]):
                view.show_error('Invalid Input', f'Variable `{name}` value is not a finite numeric value.')
                return
            self.__model.set_variable_value(name, result[1])
        try:
            result = self.__model.evaluate()
            view.show_info('Expression Evaluated', f'The expression evaluated to `{result}`.')
        except Exception as e:
            view.show_error('Evaluation Error', e.args[0])

