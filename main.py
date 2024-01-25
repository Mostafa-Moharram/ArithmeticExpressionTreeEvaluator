from controller import ExpressionController
from view import ExpressionView
from model import ExpressionModel

model = ExpressionModel()
controller = ExpressionController(model)
view = ExpressionView(controller, ('+', '*', '-', '/'))

view.mainloop()
