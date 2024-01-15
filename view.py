import functools
from tkinter import Canvas, Event, Frame, Label, Tk

class ExpressionView:
    def __init__(self):
        self.__window = Tk()
        self.__window.title('Expression Tree Parser')
        self.__window.geometry('1000x700')
        self.__window.columnconfigure(0, weight=8, uniform='a')
        self.__window.columnconfigure(1, weight=2, uniform='a')
        self.__window.rowconfigure(0, weight=1, uniform='a')
        self.__create_controls()
        self.__create_canvas()
    
    def __create_controls(self):
        controls_frame = Frame(self.__window)
        controls_frame.grid(row=0, column=1, sticky='nesw')

        controls_heading_label = Label(controls_frame, text='Controls', justify='center', font=25)
        controls_heading_label.pack(fill='x', pady=(20, 0))
    
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
        item = self.__canvas.create_oval(0, 0, 70, 70, fill='white')
        item_text = self.__canvas.create_text(35, 35, text=text)
        self.__canvas.tag_bind(item, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=35, dy=35))
        self.__canvas.tag_bind(item_text, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=35, dy=35))
    
    def create_rectangle_in_view(self, text: str):
        item = self.__canvas.create_rectangle(0, 0, 70, 70, fill='white')
        item_text = self.__canvas.create_text(35, 35, text=text)
        self.__canvas.tag_bind(item, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=35, dy=35))
        self.__canvas.tag_bind(item_text, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=35, dy=35))

    def create_triangle_in_view(self, text: str):
        item = self.__canvas.create_polygon([35, 0, 0, 70, 70, 70], fill='white')
        item_text = self.__canvas.create_text(35, 35, text=text)
        self.__canvas.tag_bind(item, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=0, dy=50))
        self.__canvas.tag_bind(item_text, '<B1-Motion>', functools.partial(self.__handle_move_event, trigger=item, trigger_text=item_text, dx=0, dy=50))