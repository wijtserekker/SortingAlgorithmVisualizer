from threading import Thread, Condition
from time import sleep
from tkinter import *

from list import List

list_size = 1120
default_width = 1200
default_height = 600
pad_x = 40
pad_y = 40
bar_spacing = 0
sleep_time = 0


class View:

    def __init__(self, master: 'Tk'):
        self.root = master
        self.canvas = Canvas(self.root, width=default_width, height=default_height)
        self.bars: '[]' = []
        self.comp_text = self.canvas.create_text(5, 5, text='Comparisons: 0', anchor=NW)
        self.mut_text = self.canvas.create_text(5, 20, text='Mutations: 0', anchor=NW)
        self.canvas.create_text(5, 35, text=('List size: ' + str(list_size)), anchor=NW)
        self.init_bars()

        self.root.bind('<space>', self.on_space)
        self.root.bind('<Up>', self.on_up)
        self.root.bind('<Down>', self.on_down)

        self.canvas.pack()
        self.root.update()

        self.done = Condition()
        self.busy = False

        self.unpause = Condition()
        self.pause = False

    def init_bars(self):
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

        if highlight_change:
            sleep(sleep_time)

        l_copy = l.copy()
        self.root.after_idle(self.draw_list, l_copy, highlight_change, changed_index1, changed_index2)

    def draw_list(self, l: List, highlight_change: bool, changed_index1, changed_index2):

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        graph_width = width - 2*pad_x
        graph_height = height - 2*pad_y
        bar_gap = graph_width / list_size * bar_spacing
        bar_width = (graph_width - (list_size - 1) * bar_gap) / list_size

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
                                   , pad_y + graph_height - (elem / list_size * graph_height)
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


# =====================================================
# =============== SORTING ALGORITHMS ==================
# =====================================================

def bubble_sort(l: List):
    changed = True
    while changed:
        changed = False
        for i in range(0, list_size - 1):
            if l[i] > l[i+1]:
                l.swap(i, i+1)
                changed = True


def insertion_sort(l: List):
    for i in range(1, list_size):
        j = i
        while j > 0 and l[j] < l[j-1]:
            l.swap(j, j-1)
            j -= 1


def selection_sort(l: List):
    for i in range(0, list_size):
        small_sub = i
        for j in range(i+1, list_size):
            if l[j] < l[small_sub]:
                small_sub = j
        l.swap(i, small_sub)


def quick_sort(l: List, lo=0, hi=list_size-1):
    if lo < hi:
        p = partition(l, lo, hi)
        quick_sort(l, lo, p - 1)
        quick_sort(l, p + 1, hi)


def partition(l, lo, hi):  # Quick sort helper function
    pivot = l[hi]
    i = lo - 1
    for j in range(lo, hi):
        if l[j] < pivot:
            i += 1
            l.swap(i, j)
    l.swap(i + 1, hi)
    return i + 1


def shell_sort(l: List):
    interval = 0
    while interval < list_size/3:
        interval = interval*3 + 1

    while interval > 0:
        for outer in range(interval, list_size):
            inner = outer
            while inner > interval - 1 and l[inner - interval] > l[inner]:
                l.swap(inner - interval, inner)
                inner = inner - interval
        interval = int((interval-1) / 3)

# =====================================================
# =====================================================
# =====================================================


def sort(l: List):
    sleep(1)

    shell_sort(l)

    l.high_lighted1 = -1
    l.high_lighted2 = -1
    l.view.update(l, True)


screen = Tk()
view = View(screen)
main_list = List(list_size, view)
view.update(main_list, False)
Thread(target=sort, args=(main_list,), daemon=True).start()
screen.mainloop()

