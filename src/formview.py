import math
from tkinter import *
from tkinter import messagebox


class FormView:

    def __init__(self, master: Tk):
        self.root = master
        self.start = False

        master.withdraw()          # Temporarily hide the window to prevent it from appearing in the corner of the
        master.update_idletasks()  # screen and then jumping to the centre

        Label(master, text="List size").grid(row=0, column=0, padx=10, pady=10)

        self.list_size = StringVar(master)
        vcmd = (master.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        e = Entry(master, textvariable=self.list_size, validate='key', validatecommand=vcmd)
        e.grid(row=0, column=1, padx=(0, 10))
        e.focus()

        self.sort_algo = StringVar(master)
        self.sort_algo.set("bubble sort")
        OptionMenu(master, self.sort_algo, "bubble sort", "insertion sort", "selection sort"
                   , "quick sort", "shell sort", "heap sort", "cocktail shaker sort", "bitonic sort"
                   , "merge sort").grid(row=1, columnspan=2, pady=(0, 10))
        Button(master, text="Start", command=self.on_start).grid(row=2, columnspan=2, pady=(0, 10))
        self.root.update()

        w = master.winfo_width()
        h = master.winfo_height()
        x = master.winfo_screenwidth() / 2 - w / 2
        y = master.winfo_screenheight() / 2 - h / 2
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        master.deiconify()  # Show the window again

    def on_start(self):
        if len(self.list_size.get()) > 0:
            if self.sort_algo.get() == "bitonic sort":
                if math.log(int(self.list_size.get()), 2) % 1 > 0:
                    messagebox.showerror('Error', 'List length must be a power of 2 when using bitonic sort.')
                    return
            self.start = True
            self.root.destroy()

    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if len(value_if_allowed) == 0:
            return True
        if text in '0123456789':
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

