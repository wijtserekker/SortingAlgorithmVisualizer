from threading import Condition
from time import sleep
from tkinter import *

from list import List

default_width = 1200
default_height = 600
pad_x = 40
pad_y = 40
bar_spacing = 0
sleep_time = 0


class SortView:

    def __init__(self, master: Tk, list_size: int):
        self.root = master
        self.canvas = Canvas(self.root, width=default_width, height=default_height)
        self.bars: '[]' = []
        self.comp_text = self.canvas.create_text(5, 5, text='Comparisons: 0', anchor=NW)
        self.mut_text = self.canvas.create_text(5, 20, text='Mutations: 0', anchor=NW)
        self.canvas.create_text(5, 35, text=('List size: ' + str(list_size)), anchor=NW)
        self.init_bars(list_size)

        self.root.bind('<space>', self.on_space)
        self.root.bind('<Up>', self.on_up)
        self.root.bind('<Down>', self.on_down)

        self.canvas.pack()
        self.root.update()

        self.done = Condition()
        self.busy = False

        self.unpause = Condition()
        self.pause = False

    def init_bars(self, list_size: int):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        graph_width = width - 2*pad_x
        graph_height = height - 2*pad_y
        bar_gap = graph_width / list_size * bar_spacing
        bar_width = (graph_width - (list_size - 1) * bar_gap) / list_size
        for i in range(0, list_size):
            self.bars.append(self.canvas.create_rectangle(pad_x + i * (bar_width + bar_gap)
                                                          , pad_y + graph_height
                                                          , pad_x + i * (bar_width + bar_gap) + bar_width
                                                          , pad_y + graph_height, fill='black', width=0))

    def update(self, l: List, highlight_change: bool, changed_index1=None, changed_index2=None):
        self.wait_for_done_drawing()
        self.wait_for_unpause()

        if highlight_change and sleep_time > 0:
            sleep(sleep_time)

        l_copy = l.copy()
        self.root.after_idle(self.draw_list, l_copy, highlight_change, changed_index1, changed_index2)

    def draw_list(self, l: List, highlight_change: bool, changed_index1, changed_index2):

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        graph_width = width - 2*pad_x
        graph_height = height - 2*pad_y
        bar_gap = graph_width / len(l) * bar_spacing
        bar_width = (graph_width - (len(l) - 1) * bar_gap) / len(l)

        self.canvas.itemconfigure(self.comp_text, text=('Comparisons: ' + str(l.comparisons)))
        self.canvas.itemconfigure(self.mut_text, text=('Mutations: ' + str(l.mutations)))

        if graph_width <= 0 or graph_height <= 0:
            return

        if None not in [changed_index1, changed_index2]:
            changed_elems = [changed_index1, changed_index2]
        else:
            changed_elems = range(0, len(l.array))

        for i in changed_elems:
            elem = l.array[i].x

            if highlight_change:
                # Change select color
                if elem in [l.high_lighted1, l.high_lighted2]:
                    self.canvas.itemconfig(self.bars[i], fill='red')
                else:
                    self.canvas.itemconfig(self.bars[i], fill='black')
            else:
                # Adjust height
                self.canvas.coords(self.bars[i], pad_x + i * (bar_width + bar_gap)
                                   , pad_y + graph_height - (elem / len(l) * graph_height)
                                   , pad_x + i * (bar_width + bar_gap) + bar_width
                                   , pad_y + graph_height)
        self.canvas.pack()
        self.root.update()

        self.done.acquire()
        self.busy = False
        self.done.notify()
        self.done.release()

    def wait_for_done_drawing(self):
        self.done.acquire()
        while self.busy:
            self.done.wait()
        self.busy = True
        self.done.release()

    def wait_for_unpause(self):
        self.unpause.acquire()
        while self.pause:
            self.unpause.wait()
        self.unpause.release()

    def on_space(self, event):
        self.unpause.acquire()
        self.pause = not self.pause
        if not self.pause:
            self.unpause.notify()
        self.unpause.release()

    def on_up(self, event):
        global sleep_time
        sleep_time = max(0, sleep_time - 0.005)

    def on_down(self, event):
        global sleep_time
        sleep_time = sleep_time + 0.005


