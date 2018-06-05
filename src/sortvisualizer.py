from threading import Thread
from time import sleep
from tkinter import Tk

from formview import FormView
from list import List
from sort import *
from sortview import SortView


def sort(l: List, func):
    sleep(1)

    func(l)

    l.high_lighted1 = -1
    l.high_lighted2 = -1
    l.view.update(l, True)


sort_algos = dict()
sort_algos["bubble sort"] = bubble_sort
sort_algos["insertion sort"] = insertion_sort
sort_algos["selection sort"] = selection_sort
sort_algos["quick sort"] = quick_sort
sort_algos["shell sort"] = shell_sort
sort_algos["heap sort"] = heap_sort
sort_algos["cocktail shaker sort"] = cocktail_shaker_sort
sort_algos["bitonic sort"] = bitonic_sort
sort_algos["merge sort"] = merge_sort


screen = Tk()
form_view = FormView(screen)
screen.mainloop()

if form_view.start:
    screen = Tk()
    list_size = int(form_view.list_size.get())
    view = SortView(screen, list_size)
    main_list = List(list_size, view)
    view.update(main_list, False)
    Thread(target=sort, args=(main_list, sort_algos[form_view.sort_algo.get()], ), daemon=True).start()
    screen.mainloop()
