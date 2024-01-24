from validators import try_parse_float, validate_variable_name
from view import ExpressionView

class ExpressionController:
    def create_operator(self, view: ExpressionView, operator: str):
        view.add_operator(operator, 0) # TODO

    def create_constant(self, view: ExpressionView, value_str: str):
        result = try_parse_float(value_str)
        if result[0]:
            view.add_constant(str(result[1]), 0) # TODO
        else:
            view.show_error('Invalid Input', result[1])

    def create_variable(self, view: ExpressionView, name: str):
        validation_result = validate_variable_name(name)
        if validation_result[0]:
            view.add_variable(name, 0) # TODO
        else:
            view.show_error('Invaid Input', validation_result[1])

    def evaluate_expression(self, view: ExpressionView, variable_keyvalue: list[tuple]):
        print(variable_keyvalue)