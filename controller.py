from view import ExpressionView


class ExpressionController:
    def create_operator_view(self, view: ExpressionView, operator: str):
        view.create_circle_in_view(operator)

    def create_constant_view(self, view: ExpressionView, value: float):
        view.create_triangle_in_view(str(value))