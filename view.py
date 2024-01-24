import functools
from tkinter import Button, Canvas, Entry, Event, Frame, Label, StringVar, Tk, messagebox, ttk

class ExpressionView:
    def __init__(self, controller, operators: list[str] | tuple[str]):
        self.__controller = controller
        self.__window = Tk()
        self.__window.title('Expression Tree Parser')
        self.__window.geometry('%dx%d'%(
            self.__window.winfo_screenwidth(),
            self.__window.winfo_screenheight()))
        self.__window.columnconfigure(0, weight=8, uniform='a')
        self.__window.columnconfigure(1, weight=2, uniform='a')
        self.__window.rowconfigure(0, weight=1, uniform='a')
        self.__window.resizable(width=False, height=False)
        self.__window.state('zoomed')
        self.__create_canvas()
        self.__create_controls(operators)
        self.__variable_name_values = dict()
        self.__view_id_map = dict()
    
    def __create_controls(self, operators: list[str] | tuple[str]):
        controls_frame = Frame(self.__window)

        controls_heading_label = Label(controls_frame, text='Controls', justify='center', font=(None, 20))
        controls_heading_label.pack(fill='x', pady=(20, 20))

        self.__add_operators_in_view(controls_frame, operators)
        self.__add_constant_in_view(controls_frame)
        self.__add_variables_in_view(controls_frame)

        evaluate_button = Button(controls_frame, text='Evaluate',
                                 command=self.__evaluate_expression)
        evaluate_button.pack(anchor='s', side='bottom')
        controls_frame.grid(row=0, column=1, sticky='nesw')
    
    def __evaluate_expression(self):
        variable_keyvalue = {n: v.get() for n, v in self.__variable_name_values.items()}
        self.__controller.evaluate_expression(self, variable_keyvalue)

    def __add_operators_in_view(self, controls_frame: Frame, operators: list[str] | tuple[str]):
        operators_frame = Frame(controls_frame)

        operator_button = Button(operators_frame, text='Create operator')
        operator_button.pack(side='left')

        operators_comboBox = ttk.Combobox(operators_frame, state='readonly')
        operators_comboBox['values'] = operators
        operators_comboBox.pack(side='right')
        operators_comboBox.current(0)

        operator_button.bind('<Button-1>',
                            lambda _: self.__controller.create_operator(self, operators_comboBox.get()))

        operators_frame.pack(fill='x', side='top', pady=(0, 5))

    def __add_variables_in_view(self, controls_frame: Frame):
        self.__variables_frame = Frame(controls_frame)

        variable_controls_frame = Frame(self.__variables_frame)

        variable_name = StringVar()
        variable_button = Button(variable_controls_frame, text='Add variable',
                                 command=lambda:
                                    self.__controller.create_variable(self, variable_name.get()))
        variable_name_entry = Entry(variable_controls_frame,
                                    textvariable=variable_name)
        
        variable_button.pack(side='left')
        variable_name_entry.pack(side='right')
        variable_controls_frame.pack(side='top', fill='x')
        self.__variables_frame.pack(fill='x', side='top')

    def __add_constant_in_view(self, controls_frame: Frame):
        constant_frame = Frame(controls_frame)

        constant_input_value = StringVar()
        constant_button = Button(constant_frame,
                                 text='Create constant',
                                 command=lambda:
                                 self.__controller.create_constant(self,
                                    constant_input_value.get()))
        constant_button.pack(side='left')

        value_entry = Entry(constant_frame, textvariable=constant_input_value)
        value_entry.pack(side='right')

        constant_frame.pack(fill='x', side='top', pady=(0, 5))

    def __create_canvas(self):
        self.__canvas = Canvas(self.__window, bg='lightgray')
        self.__canvas.grid(row=0, column=0, sticky='nesw')
    
    def __handle_move_event(self, event: Event, trigger: int, trigger_text: int, dx: int, dy: int):
        self.__canvas.moveto(trigger, event.x - 35, event.y - 35)
        coords = self.__canvas.coords(trigger)
        self.__canvas.coords(trigger_text, coords[0] + dx, coords[1] + dy)
    
    def __create_circle_in_view(self, text: str):
        item = self.__canvas.create_oval(0, 0, 60, 60, fill='white')
        item_text = self.__canvas.create_text(30, 30, text=text, font=(None, 18))
        self.__canvas.tag_bind(item, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=30, dy=30))
        self.__canvas.tag_bind(item_text, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=30, dy=30))
        return item
    
    def __create_rectangle_in_view(self, text: str):
        item = self.__canvas.create_rectangle(0, 0, 70, 70, fill='white')
        item_text = self.__canvas.create_text(35, 35, text=text)
        self.__canvas.tag_bind(item, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=35, dy=35))
        self.__canvas.tag_bind(item_text, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=35, dy=35))
        return item

    def __create_triangle_in_view(self, text: str):
        item = self.__canvas.create_polygon([35, 0, 0, 70, 70, 70], fill='white')
        item_text = self.__canvas.create_text(35, 50, text=text)
        self.__canvas.tag_bind(item, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=0, dy=50))
        self.__canvas.tag_bind(item_text, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=0, dy=50))
        return item

    def mainloop(self):
        self.__window.mainloop()

    def show_error(self, title: str, text: str):
        messagebox.showerror(title, text)

    def add_variable(self, name: str, id: int):
        view_id = self.__create_rectangle_in_view(name)
        # TODO: Bind model_id with view_id

        if name in self.__variable_name_values.keys():
            return

        variable_name_var = StringVar()
        
        self.__variable_name_values[name] = variable_name_var

        variable_frame = Frame(self.__variables_frame)
        
        variable_name_text = Label(variable_frame, text=name)
        variable_name_input = Entry(variable_frame, textvariable=variable_name_var)
        
        variable_name_text.pack(side='left')
        variable_name_input.pack(side='right')
        variable_frame.pack(side='top', anchor='w', fill='x')

    def add_constant(self, text: str, id: int):
        view_id = self.__create_triangle_in_view(text)
        # TODO: Bind model_id with view_id

    def add_operator(self, text: str, id: int):
        view_id = self.__create_circle_in_view(text)
        # TODO: Bind model_id with view_id

