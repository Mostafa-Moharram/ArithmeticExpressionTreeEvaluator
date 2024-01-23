import functools
from tkinter import Button, Canvas, Entry, Event, Frame, Label, StringVar, Tk, messagebox, ttk

class ExpressionView:
    def __init__(self, controller):
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
    
    def create_controls(self, operators: list[str] | tuple[str]):
        controls_frame = Frame(self.__window)

        controls_heading_label = Label(controls_frame, text='Controls', justify='center', font=(None, 20))
        controls_heading_label.pack(fill='x', pady=(20, 20))

        self.__add_operators_in_view(controls_frame, operators)
        self.__add_constant_in_view(controls_frame)

        controls_frame.grid(row=0, column=1, sticky='nesw')
    
    def __add_operators_in_view(self, controls_frame: Frame, operators: list[str] | tuple[str]):
        operators_frame = Frame(controls_frame)

        operator_button = Button(operators_frame, text='Create operator')
        operator_button.pack(side='left', expand=True)

        operators_comboBox = ttk.Combobox(operators_frame, state='readonly')
        operators_comboBox['values'] = operators
        operators_comboBox.pack(side='left', expand=True)
        operators_comboBox.current(0)

        operator_button.bind('<Button-1>',
                            lambda _: self.__controller.create_operator_view(self, operators_comboBox.get()))

        operators_frame.pack(fill='x')
    
    @staticmethod
    def __handle_float_input(value_str: str):
        try:
            value = float(value_str)
            return value
        except:
            messagebox.showerror('Invalid Input', 'Input has to be floating point number.')
            return None
    
    def __handle_constant_input(self, value_str: str):
        value = ExpressionView.__handle_float_input(value_str)
        if value is None:
            return
        self.__controller.create_constant_view(self, value)

    def __add_constant_in_view(self, controls_frame: Frame):
        constant_frame = Frame(controls_frame)

        constant_input_value = StringVar()
        constant_button = Button(constant_frame,
                                 text='Create constant',
                                 command=lambda:
                             self.__handle_constant_input(constant_input_value.get()))
        constant_button.pack(side='left', expand=True)

        value_entry = Entry(constant_frame, textvariable=constant_input_value)
        value_entry.pack(side='left', expand=True)

        constant_frame.pack(fill='x')

    def __create_canvas(self):
        self.__canvas = Canvas(self.__window, bg='grey')
        self.__canvas.grid(row=0, column=0, sticky='nesw')
    
    def __handle_move_event(self, event: Event, trigger: int, trigger_text: int, dx: int, dy: int):
        self.__canvas.moveto(trigger, event.x - 35, event.y - 35)
        coords = self.__canvas.coords(trigger)
        self.__canvas.coords(trigger_text, coords[0] + dx, coords[1] + dy)

    def mainloop(self):
        self.__window.mainloop()

    # Show it
    def create_circle_in_view(self, text: str):
        item = self.__canvas.create_oval(0, 0, 60, 60, fill='white')
        item_text = self.__canvas.create_text(30, 30, text=text, font=(None, 18))
        self.__canvas.tag_bind(item, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=30, dy=30))
        self.__canvas.tag_bind(item_text, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=30, dy=30))
    
    def create_rectangle_in_view(self, text: str):
        item = self.__canvas.create_rectangle(0, 0, 70, 70, fill='white')
        item_text = self.__canvas.create_text(35, 35, text=text)
        self.__canvas.tag_bind(item, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=35, dy=35))
        self.__canvas.tag_bind(item_text, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=35, dy=35))

    def create_triangle_in_view(self, text: str):
        item = self.__canvas.create_polygon([35, 0, 0, 70, 70, 70], fill='white')
        item_text = self.__canvas.create_text(35, 50, text=text)
        self.__canvas.tag_bind(item, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=0, dy=50))
        self.__canvas.tag_bind(item_text, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=0, dy=50))