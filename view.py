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
        self.__model_id_map = dict()
        self.__pointer_to = dict()
        self.__pointee_by = dict()
        self.__active_item = None
        self.__potential_parents = set()

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

    def __update_pointer_pointee_lines(self, pointer_coords, pointee_coords, line1, line2):
        middle_coords = ((pointer_coords[0] + pointee_coords[0]) // 2,
                         (pointer_coords[1] + pointee_coords[1]) // 2)
        self.__canvas.coords(line1,
                             pointer_coords[0], pointer_coords[1],
                             middle_coords[0], middle_coords[1])
        self.__canvas.coords(line2,
                             middle_coords[0], middle_coords[1],
                             pointee_coords[0], pointee_coords[1])

    def __update_pointer_to_pointees(self, pointer):
        if pointer not in self.__pointer_to.keys():
            return
        pointer_coords = ExpressionView.__get_center(self.__canvas.coords(pointer))
        for pointee, line1, line2 in self.__pointer_to[pointer]:
            pointee_coords = ExpressionView.__get_center(self.__canvas.coords(pointee))
            self.__update_pointer_pointee_lines(pointer_coords, pointee_coords,
                                                line1, line2)

    def __update_pointee_by_pointers(self, pointee):
        if pointee not in self.__pointee_by.keys():
            return
        pointee_coords = ExpressionView.__get_center(self.__canvas.coords(pointee))
        for pointer, line1, line2 in self.__pointee_by[pointee]:
            pointer_coords = ExpressionView.__get_center(self.__canvas.coords(pointer))
            self.__update_pointer_pointee_lines(pointer_coords, pointee_coords,
                                                line1, line2)

    def __handle_move_event(self, event: Event, trigger: int, trigger_text: int, dx: int, dy: int):
        self.__canvas.moveto(trigger, event.x - 35, event.y - 35)
        coords = self.__canvas.coords(trigger)
        self.__canvas.coords(trigger_text, coords[0] + dx, coords[1] + dy)
        self.__update_pointer_to_pointees(trigger)
        self.__update_pointee_by_pointers(trigger)

    def __activate_arrow_drawing(self, item: int):
        self.__canvas.itemconfigure(item, outline='black')
        self.__active_item = item

    def __deactivate_arrow_drawing(self):
        self.__canvas.itemconfigure(self.__active_item, outline='white')
        self.__active_item = None

    @staticmethod
    def __get_center(coords) -> tuple[int]:
        if len(coords) == 4:
            return ((coords[0] + coords[2]) // 2, (coords[1] + coords[3]) // 2)
        return (coords[0], coords[1] + 50)

    def __handle_mouse_right_click(self, item: int):
        if self.__active_item is None:
            if item in self.__potential_parents:
                self.__activate_arrow_drawing(item)
            return
        if self.__active_item == item:
            self.__deactivate_arrow_drawing()
            return
        pointer = self.__active_item
        pointee = item
        self.__deactivate_arrow_drawing()
        self.__controller.set_parent_of(self,
            self.__view_id_map[pointer],
            self.__view_id_map[pointee])

    def __create_circle_in_view(self, text: str):
        item = self.__canvas.create_oval(0, 0, 60, 60, fill='white', width=1, outline='white')
        item_text = self.__canvas.create_text(30, 30, text=text, font=(None, 18))
        self.__canvas.tag_bind(item, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=30, dy=30))
        self.__canvas.tag_bind(item_text, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=30, dy=30))
        self.__canvas.tag_bind(item, '<Button-3>', lambda _: self.__handle_mouse_right_click(item))
        return item

    def __create_rectangle_in_view(self, text: str):
        item = self.__canvas.create_rectangle(0, 0, 70, 70, fill='white', width=1, outline='white')
        item_text = self.__canvas.create_text(35, 35, text=text)
        self.__canvas.tag_bind(item, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=35, dy=35))
        self.__canvas.tag_bind(item_text, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=35, dy=35))
        self.__canvas.tag_bind(item, '<Button-3>', lambda _: self.__handle_mouse_right_click(item))
        return item

    def __create_triangle_in_view(self, text: str):
        item = self.__canvas.create_polygon([35, 0, 0, 70, 70, 70], fill='white', width=1, outline='white')
        item_text = self.__canvas.create_text(35, 50, text=text)
        self.__canvas.tag_bind(item, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=0, dy=50))
        self.__canvas.tag_bind(item_text, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=0, dy=50))
        self.__canvas.tag_bind(item, '<Button-3>', lambda _: self.__handle_mouse_right_click(item))
        return item

    def mainloop(self):
        self.__window.mainloop()

    def show_error(self, title: str, text: str):
        messagebox.showerror(title, text)

    def show_info(self, title: str, text: str):
        messagebox.showinfo(title, text)

    def add_variable(self, name: str, id: int):
        view_id = self.__create_rectangle_in_view(name)
        self.__view_id_map[view_id] = id
        self.__model_id_map[id] = view_id

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
        self.__view_id_map[view_id] = id
        self.__model_id_map[id] = view_id

    def add_operator(self, text: str, id: int):
        view_id = self.__create_circle_in_view(text)
        self.__potential_parents.add(view_id)
        self.__view_id_map[view_id] = id
        self.__model_id_map[id] = view_id

    def form_parenting_connection(self, parent_id: int, child_id: int) -> None:
        pointer = self.__model_id_map[parent_id]
        pointee = self.__model_id_map[child_id]
        pointer_coord = ExpressionView.__get_center(
            self.__canvas.coords(pointer))
        pointee_coord = ExpressionView.__get_center(
            self.__canvas.coords(pointee))
        mid = ((pointee_coord[0] + pointer_coord[0]) // 2,
               (pointee_coord[1] + pointer_coord[1]) // 2)
        line1 = self.__canvas.create_line(
            pointer_coord[0], pointer_coord[1],
            mid[0], mid[1],
            arrow='last', fill='black', width='2')
        line2 = self.__canvas.create_line(
            mid[0], mid[1],
            pointee_coord[0], pointee_coord[1],
            fill='black', width='2')
        self.__canvas.lower(line1)
        self.__canvas.lower(line2)
        self.__pointer_to.setdefault(pointer, []).append((pointee, line1, line2))
        self.__pointee_by.setdefault(pointee, []).append((pointer, line1, line2))
