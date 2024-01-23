from controller import ExpressionController
from view import ExpressionView

controller = ExpressionController()
view = ExpressionView(controller, ('+', '*', '-', '/'))

view.mainloop()
