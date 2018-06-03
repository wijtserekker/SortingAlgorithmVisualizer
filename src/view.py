from threading import Thread
from time import sleep
from tkinter import *

from list import List

list_size = 300
default_width = 1200
default_height = 600
pad_x = 40
pad_y = 40
bar_spacing = 0
sleep_time = 0.01


class View:

    def __init__(self, master: 'Tk'):
        super().__init__()
        self.root = master
        self.canvas = Canvas(self.root, width=default_width, height=default_height)
        self.bars: '[]' = []
        self.comp_text = self.canvas.create_text(5, 5, text='Comparisons: 0', anchor=NW)
        self.mut_text = self.canvas.create_text(5, 20, text='Mutations: 0', anchor=NW)
        self.canvas.create_text(5, 35, text=('List size: ' + str(list_size)), anchor=NW)
        self.init_bars()
        self.canvas.pack()
        self.root.update()

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

    def update(self, l: 'List', highlight_change: 'bool', changed_index1=None, changed_index2=None):
        l_copy = l.copy()
        self.root.after_idle(self.draw_list, l_copy, highlight_change, changed_index1, changed_index2)

    def draw_list(self, l: 'List', highlight_change: 'bool', changed_index1, changed_index2):
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


# =====================================================
# =============== SORTING ALGORITHMS ==================
# =====================================================

def bubble_sort(l: List):
    changed = True
    while changed:
        changed = False
        for i in range(0, list_size - 1):
            sleep(sleep_time)
            if l[i] > l[i+1]:
                l.swap(i, i+1)
                changed = True

    l.high_lighted1 = -1
    l.high_lighted2 = -1
    l.view.update(l, True)


def insertion_sort(l: List):
    for i in range(1, list_size):
        j = i
        while j > 0 and l[j] < l[j-1]:
            sleep(sleep_time)
            l.swap(j, j-1)
            j -= 1

    l.high_lighted1 = -1
    l.high_lighted2 = -1
    l.view.update(l, True)


def selection_sort(l: List):
    for i in range(0, list_size):
        small_sub = i
        for j in range(i+1, list_size):
            sleep(sleep_time)
            if l[j] < l[small_sub]:
                small_sub = j
        l.swap(i, small_sub)

    l.high_lighted1 = -1
    l.high_lighted2 = -1
    l.view.update(l, True)


def quick_sort(l: List, lo=0, hi=list_size-1):
    if lo < hi:
        p = partition(l, lo, hi)
        quick_sort(l, lo, p - 1)
        quick_sort(l, p + 1, hi)
    if lo == 0 and hi == list_size-1:
        l.high_lighted1 = -1
        l.high_lighted2 = -1
        l.view.update(l, True)


def partition(l, lo, hi):  # Quick sort helper function
    pivot = l[hi]
    i = lo - 1
    for j in range(lo, hi):
        sleep(sleep_time)
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
                sleep(sleep_time)
                l.swap(inner - interval, inner)
                inner = inner - interval
        interval = int((interval-1) / 3)

# =====================================================
# =====================================================
# =====================================================

screen = Tk()
view = View(screen)
main_list = List(list_size, view)
view.update(main_list, False)
Thread(target=quick_sort, args=(main_list,)).start()
screen.mainloop()

