from view import ExpressionView


class ExpressionController:
    def create_operator_view(self, view: ExpressionView, operator: str):
        view.create_circle_in_view(operator)

    def create_constant_view(self, view: ExpressionView, value: float):
        view.create_triangle_in_view(str(value))
    
    def create_variable_view(self, view: ExpressionView, name: str):
        view.create_rectangle_in_view(name)

    def evaluate_expression_view(self, view: ExpressionView, variable_keyvalue: list[tuple]):
        print(variable_keyvalue)