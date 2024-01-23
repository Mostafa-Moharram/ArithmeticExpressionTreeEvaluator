from controller import ExpressionController
from view import ExpressionView

controller = ExpressionController()
view = ExpressionView(controller)

view.create_controls(('+', '*', '-', '/'))

view.create_rectangle_in_view('Rectangle')
view.create_rectangle_in_view('Rectangle')

view.mainloop()
