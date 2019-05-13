from tkinter import *
from tk_valid import validate_alphanum, validate_float
import os
import pickle


class Quit_To_Menu():
    def __init__(self, master, x, y):
        self.master = master
        self.master.geometry('+%d+%d' % (x, y))
        self.master.config(borderwidth=3, relief=RAISED)
        Label(self.master, text='Are you sure you want to quit to the main menu?'
              ).grid(row=0, column=0, columnspan=2)
        Button(self.master, text='Yes, quit to main menu',
               command=lambda: self.destroy(1)).grid(row=1, column=0)
        Button(self.master, text='No, return to simulation',
               command=lambda: self.destroy(0)).grid(row=1, column=1)

    def destroy(self, boolean):
        self.go_home = boolean
        self.master.destroy()

    def wait(self):
        self.master.wait_window()
        return self.go_home


class Save_Sim():
    def __init__(self, master, sim, x, y):
        self.master = master
        self.master.geometry('+%d+%d' % (x, y))
        self.master.config(borderwidth=3, relief=RAISED)
        self.sim = sim
        self.instructions = StringVar()
        self.instructions.set('Choose a name for the save file:')
        Label(self.master, textvariable=self.instructions).pack()
        self.save_name = StringVar()
        self.save_name.trace('w', self.callback)  # reverts from error/overwrite instructions
        entry = Entry(self.master, textvariable=self.save_name, validate='key',
                      vcmd=(self.master.register(validate_alphanum), "%P"))
        entry.pack()
        Button(self.master, text='Close', command=lambda: self.close()).pack(side=LEFT)
        self.b_text = StringVar()
        self.b_text.set('Save')
        Button(self.master, textvariable=self.b_text, command=lambda: self.save()).pack(side=RIGHT)
        entry.focus_force()

    def save(self):
        file_name = self.save_name.get()
        files = os.listdir()
        files = [i for i in files if i.isalnum() is True]
        if file_name == '':
            self.instructions.set('File name must contain alpha or numeric characters only')
            return
        elif file_name in files and self.b_text.get() != 'Overwrite':
            self.instructions.set('File name already exists. Do you want to overwrite the file?')
            self.b_text.set('Overwrite')
            return

        with open(file_name, 'wb') as save_file:
            pickle.dump(self.sim, save_file)
        self.master.destroy()

    def callback(self, *args):
        self.instructions.set('Choose a name for the save file:')
        self.b_text.set('Save')

    def close(self):
        self.master.destroy()


class Dimensions():
    def __init__(self, master, dims, x, y):
        self.master = master
        self.master.geometry('+%d+%d' % (x, y))
        self.master.config(borderwidth=3, relief=RAISED)
        self.instructions = StringVar()
        self.instructions.set('Enter plot dimensions and select units')
        Label(self.master, textvariable=self.instructions).grid(row=0, column=0, columnspan=4)
        Label(self.master, text='Width:').grid(row=1, column=0)
        Label(self.master, text='Length:').grid(row=1, column=2)
        self.width = DoubleVar()
        width_entry = Entry(self.master, validate='key',
                            vcmd=(self.master.register(validate_float), "%P"),
                            textvariable=self.width)
        width_entry.grid(row=1, column=1)
        width_entry.focus_force()
        self.length = DoubleVar()
        Entry(self.master, validate='key', vcmd=(self.master.register(validate_float), "%P"),
              textvariable=self.length).grid(row=1, column=3)
        self.unit = StringVar()
        Radiobutton(self.master, text='Metric (meters)', variable=self.unit,
                    value='m').grid(row=2, column=0, columnspan=2)
        Radiobutton(self.master, text='English (feet)', variable=self.unit,
                    value='ft').grid(row=2, column=2, columnspan=2)
        Button(self.master, text='Set Dimensions',
               command=lambda: self.set_dims()).grid(row=3, column=0, columnspan=4)
        if dims:
            x_dim, y_dim, unit = dims
            self.width.set(x_dim)
            self.length.set(y_dim)
            self.unit.set(unit)

    def set_dims(self):
        try:
            if not self.width.get() or not self.length.get():
                self.instructions.set('Please enter width and length dimensions')
                return
        except TclError:  # in case user submits form with blank fields
            self.instructions.set('Please enter width and length dimensions')
            return
        if not self.unit.get():
            self.instructions.set('Please select Metric or English units')
            return
        else:
            self.x_dim = self.width.get()
            self.y_dim = self.length.get()
            self.unit = self.unit.get()
            self.master.destroy()

    def wait(self):
        self.master.wait_window()
        return (self.x_dim, self.y_dim, self.unit)
