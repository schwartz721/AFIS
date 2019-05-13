from tkinter import *
import os
import pickle


class Manage_Plants():
    def __init__(self, master, window_w, window_h, long_state, short_state):
        self.master = master
        self.instructions = StringVar()
        self.instructions.set('Select units:')
        Label(self.master, textvariable=self.instructions).grid(row=0, column=0, columnspan=2)
        self.unit = StringVar()
        Radiobutton(self.master, text='Metric (meters)', variable=self.unit,
                    value='m').grid(row=1, column=0)
        Radiobutton(self.master, text='English (feet)', variable=self.unit,
                    value='ft').grid(row=1, column=1)
        Button(self.master, text='Edit long cycle plants', state=long_state,
               command=lambda: self.destroy('edit plant', 'long')).grid(row=2, column=0)
        Button(self.master, text='Edit short cycle plants', state=short_state,
               command=lambda: self.destroy('edit plant', 'short')).grid(row=2, column=1)
        Button(self.master, text='New long cycle plant',
               command=lambda: self.destroy('new plant', 'long')).grid(row=3, column=0)
        Button(self.master, text='New short cycle plant',
               command=lambda: self.destroy('new plant', 'short')).grid(row=3, column=1)
        Button(self.master, text='Close', command=lambda: self.destroy(None, None)
               ).grid(row=4, column=0, columnspan=2)
        self.master.update_idletasks()
        x = window_w / 2 - self.master.winfo_width() / 2
        y = window_h / 2 - self.master.winfo_height() / 2
        self.master.geometry('+%d+%d' % (x, y))
        self.master.config(borderwidth=3, relief=RAISED)

    def destroy(self, action, cycle):
        if action:
            if not self.unit.get():
                self.instructions.set('Please select units to continue')
                return
            self.action = action
            self.cycle = cycle
            self.unit = self.unit.get()
        else:
            self.action = None
            self.cycle = None
            self.unit = None
        self.master.destroy()

    def wait(self):
        self.master.wait_window()
        return (self.action, self.cycle, self.unit)


class Load():
    def __init__(self, master, window_w, window_h):
        self.master = master
        files = os.listdir()
        files = [i for i in files if i.isalnum() is True]
        if files:
            Label(self.master, text='Choose a file to load:').grid(row=0, column=0, columnspan=2)
            self.file_choice = StringVar()
            self.file_choice.set(files[0])
            OptionMenu(self.master, self.file_choice, *files).grid(row=0, column=2)
            Button(self.master, text='Close', command=lambda: self.destroy('close')).grid(row=1, column=0)
            Button(self.master, text='Delete', command=lambda: self.destroy('delete')).grid(row=1, column = 1)
            Button(self.master, text='Load', command=lambda: self.destroy('load')).grid(row=1, column=2)
        else:
            Label(self.master, text='There are no saved simulations to load').pack()
            Button(self.master, text='Close', command=lambda: self.destroy('close')).pack()
        self.master.update_idletasks()
        x = window_w / 2 - self.master.winfo_width() / 2
        y = window_h / 2 - self.master.winfo_height() / 2
        self.master.geometry('+%d+%d' % (x, y))
        self.master.config(borderwidth=3, relief=RAISED)

    def destroy(self, action):
        if action == 'load':
            with open(self.file_choice.get(), 'rb') as load_file:
                self.sim = pickle.load(load_file)
        elif action == 'delete':
            self.sim = self.file_choice.get()
        elif action == 'close':
            self.sim = None
        self.master.destroy()

    def wait(self):
        self.master.wait_window()
        return self.sim


class Delete_Savefile():
    def __init__(self, master, savefile, window_w, window_h):
        self.master = master
        self.savefile = savefile
        Label(self.master, text="Press 'Confirm' to delete '%s' savefile" % self.savefile
              ).grid(row=0, column=0, columnspan=2)
        Button(self.master, text='Cancel', command=lambda: self.destroy(0)).grid(row=1, column=0)
        Button(self.master, text='Confirm', command=lambda: self.destroy(1)).grid(row=1, column=1)
        self.master.update_idletasks()
        x = window_w / 2 - self.master.winfo_width() / 2
        y = window_h / 2 - self.master.winfo_height() / 2
        self.master.geometry('+%d+%d' % (x, y))
        self.master.config(borderwidth=3, relief=RAISED)

    def destroy(self, boolean):
        if boolean:
            os.remove(self.savefile)
        self.master.destroy()
