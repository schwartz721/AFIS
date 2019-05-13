from tkinter import *
from tk_valid import validate_int, validate_float
from plant_classes import Long_Cycle_Plant, Short_Cycle_Plant, Planting_Params
import pickle
import color_window


class Growth_Parameters():
    def __init__(self, master, action, cycle, unit, x, y):
        self.master = master
        self.master.config(borderwidth=3, relief=RAISED)
        self.cycle = cycle
        self.unit = unit
        if self.unit == 'm':
            self.small_unit = 100
            self.convert = 1
        else:
            self.small_unit = 12
            self.convert = 3.28

        with open('plant_dicts_v0_5', 'rb') as load_file:
            self.plant_dicts = pickle.load(load_file)
            self.cycle_dict = self.plant_dicts[cycle]
            options = list(self.cycle_dict.keys())
            options.remove('New Plant')
            options.remove('New Plant + Save')
            options.sort()
        if action != 'edit plant':
            options += ['New Plant', 'New Plant + Save']

        self.name_label = Label(self.master, text='Plant name:')
        self.name_entry = Entry(self.master)
        self.plant_label = Label(self.master, text='Select a plant:')
        self.plant_label.grid(row=0, column=0, columnspan=2, sticky=E)
        self.plant_choice = StringVar()
        self.plant_choice.trace('w', self.auto_pop)
        self.dropdown = OptionMenu(self.master, self.plant_choice, *options)
        self.dropdown.grid(row=0, column=2, columnspan=1, sticky=W)

        Label(self.master, text='Diameter').grid(row=1, column=0, columnspan=3)
        Label(self.master, text='Height').grid(row=1, column=3, columnspan=3)
        Label(self.master, text='Initial:').grid(row=2, column=0, sticky=E)
        self.initial_d = DoubleVar()
        self.initial_d_entry = Entry(self.master, validate='key',
                                     vcmd=(self.master.register(validate_float), "%P"),
                                     textvariable=self.initial_d, width=5)
        self.initial_d_entry.grid(row=2, column=1)
        Label(self.master, text='Initial:').grid(row=2, column=3, sticky=E)
        self.initial_h = DoubleVar()
        Entry(self.master, validate='key', vcmd=(self.master.register(validate_float), "%P"),
              textvariable=self.initial_h, width=5).grid(row=2, column=4)
        Label(self.master, text='Maximum:').grid(row=3, column=0, sticky=E)
        self.max_d = DoubleVar()
        Entry(self.master, validate='key', vcmd=(self.master.register(validate_float), "%P"),
              textvariable=self.max_d, width=5).grid(row=3, column=1)
        Label(self.master, text='Maximum:').grid(row=3, column=3, sticky=E)
        self.max_h = DoubleVar()
        Entry(self.master, validate='key', vcmd=(self.master.register(validate_float), "%P"),
              textvariable=self.max_h, width=5).grid(row=3, column=4)
        if self.cycle == 'long':
            Label(self.master, text='Rate of Growth:').grid(row=4, column=0, sticky=E)
            self.rate_d = DoubleVar()
            Entry(self.master, validate='key', vcmd=(self.master.register(validate_float), "%P"),
                  textvariable=self.rate_d, width=5).grid(row=4, column=1)
            Label(self.master, text='Rate of Growth:').grid(row=4, column=3, sticky=E)
            self.rate_h = DoubleVar()
            Entry(self.master, validate='key', vcmd=(self.master.register(validate_float), "%P"),
                  textvariable=self.rate_h, width=5).grid(row=4, column=4)

        if self.unit == 'm':
            Label(self.master, text='cm').grid(row=2, column=2, sticky=W)
            Label(self.master, text='cm').grid(row=2, column=5, sticky=W)
            Label(self.master, text='m').grid(row=3, column=2, sticky=W)
            Label(self.master, text='m').grid(row=3, column=5, sticky=W)
            if self.cycle == 'long':
                Label(self.master, text='m/year').grid(row=4, column=2, sticky=W)
                Label(self.master, text='m/year').grid(row=4, column=5, sticky=W)
        else:
            Label(self.master, text='in').grid(row=2, column=2, sticky=W)
            Label(self.master, text='in').grid(row=2, column=5, sticky=W)
            Label(self.master, text='ft').grid(row=3, column=2, sticky=W)
            Label(self.master, text='ft').grid(row=3, column=5, sticky=W)
            if self.cycle == 'long':
                Label(self.master, text='ft/year').grid(row=4, column=2, sticky=W)
                Label(self.master, text='ft/year').grid(row=4, column=5, sticky=W)

        if action == 'new crop':
            self.master.geometry('+%d+%d' % (x, y))
            Button(self.master, text='Continue', command=lambda: self.destroy('planting params')
                   ).grid(row=5, column=1)
        else:
            self.master.update_idletasks()
            x = x - self.master.winfo_width() / 2
            y = y - self.master.winfo_height() / 2
            self.master.geometry('+%d+%d' % (x, y))
            Button(self.master, text='Save', command=lambda: self.destroy('save plant')
                   ).grid(row=5, column=1)
            if action == 'new plant':
                self.plant_label.grid_forget()
                self.dropdown.grid_forget()
                self.plant_choice.set('New Plant')
            else:
                Button(self.master, text='Delete', command=lambda: self.destroy('delete plant')
                       ).grid(row=5, column=2, columnspan=2)
        Button(self.master, text='Close', command=lambda: self.destroy(None)).grid(row=5, column=4)
        Button(self.master, text='*', command=lambda: self.focus()).grid(row=5, column=5)

    def auto_pop(self, *args):
        self.plant = self.cycle_dict[self.plant_choice.get()]
        if self.plant:
            self.name_label.grid_forget()
            self.name_entry.grid_forget()
            self.initial_d.set(round(self.plant.radius * 2 * self.small_unit * self.convert, 2))
            self.max_d.set(round(self.plant.max_radius * 2 * self.convert, 2))
            self.initial_h.set(round(self.plant.height * self.small_unit * self.convert, 2))
            self.max_h.set(round(self.plant.max_height * self.convert, 2))
            if self.cycle == 'long':
                self.rate_d.set(round(self.plant.radius_rate * 2 * self.convert, 2))
                self.rate_h.set(round(self.plant.height_rate * self.convert, 2))
        else:
            self.name_label.grid(row=0, column=3, sticky=E)
            self.name_entry.grid(row=0, column=4, columnspan=2, sticky=W)
            self.name_entry.focus_force()
            self.initial_d.set(0.0)
            self.max_d.set(0.0)
            self.initial_h.set(0.0)
            self.max_h.set(0.0)
            if self.cycle == 'long':
                self.rate_d.set(0.0)
                self.rate_h.set(0.0)

    def focus(self):
        self.initial_d_entry.focus_force()

    def destroy(self, action):
        if action == 'planting params' or action == 'save plant':
            try:
                if self.plant:
                    name = self.plant.name
                else:
                    name = self.name_entry.get()
            except AttributeError:
                return
            diameter = self.initial_d.get() / self.convert / self.small_unit
            height = self.initial_h.get() / self.convert / self.small_unit
            max_diameter = self.max_d.get() / self.convert
            max_height = self.max_h.get() / self.convert
            reqs = ''
            services = ''
            if self.cycle == 'long':
                diameter_rate = self.rate_d.get() / self.convert
                height_rate = self.rate_h.get() / self.convert
                self.plant = Long_Cycle_Plant(name, diameter, height, max_diameter, max_height,
                                              diameter_rate, height_rate, reqs, services)
            else:
                self.plant = Short_Cycle_Plant(name, diameter, height, max_diameter, max_height,
                                               reqs, services)
            if action == 'save plant' or self.plant_choice.get() == 'New Plant + Save':
                self.cycle_dict[name] = self.plant
                with open('plant_dicts_v0_5', 'wb') as save_file:
                    pickle.dump(self.plant_dicts, save_file)
        elif action == 'delete plant':
            try:
                del self.cycle_dict[self.plant.name]
            except AttributeError:
                return
            with open('plant_dicts_v0_5', 'wb') as save_file:
                pickle.dump(self.plant_dicts, save_file)
        else:
            self.plant = None
        self.master.destroy()

    def wait(self):
        self.master.wait_window()
        return (self.plant, self.unit)


class Planting_Parameters():
    def __init__(self, master, plant, unit, crop, year, x, y, plot_x, plot_y):
        self.master = master
        self.master.geometry('+%d+%d' % (x, y))
        self.master.config(borderwidth=3, relief=RAISED)
        self.plot_x = plot_x
        self.plot_y = plot_y

        self.instructions = StringVar()
        self.instructions.set('Enter planting parameters for %s' % plant.name)
        Label(self.master, textvariable=self.instructions).grid(row=0, column=0, columnspan=7)
        Label(self.master, text='Plant Spacing:').grid(row=1, column=0, sticky=E)
        Label(self.master, text='Row Spacing:').grid(row=2, column=0, sticky=E)
        Label(self.master, text='First Row Location:').grid(row=1, column=4, sticky=E)
        Label(self.master, text='Row Edge Margin:').grid(row=2, column=4, sticky=E)

        self.crop_spacing = DoubleVar()
        self.crop_spacing_entry = Entry(self.master, width=5, validate='key',
                                        vcmd=(self.master.register(validate_float), "%P"),
                                        textvariable=self.crop_spacing)
        self.crop_spacing_entry.grid(row=1, column=1)
        self.row_spacing = DoubleVar()
        Entry(self.master, validate='key', vcmd=(self.master.register(validate_float), "%P"),
              textvariable=self.row_spacing, width=5).grid(row=2, column=1)
        self.x_offset = DoubleVar()
        Entry(self.master, validate='key', vcmd=(self.master.register(validate_float), "%P"),
              textvariable=self.x_offset, width=5).grid(row=1, column=5)
        self.y_offset = DoubleVar()
        Entry(self.master, validate='key', vcmd=(self.master.register(validate_float), "%P"),
              textvariable=self.y_offset, width=5).grid(row=2, column=5)

        Label(self.master, text=unit).grid(row=1, column=2, sticky=W)
        Label(self.master, text=unit).grid(row=2, column=2, sticky=W)
        Label(self.master, text=unit).grid(row=1, column=6, sticky=W)
        Label(self.master, text=unit).grid(row=2, column=6, sticky=W)

        Label(self.master, text='Planting Year:').grid(row=3, column=0, sticky=E)
        self.planting_year = IntVar()
        Entry(self.master, validate='key', vcmd=(self.master.register(validate_int), "%P"),
              textvariable=self.planting_year, width=3).grid(row=3, column=1)

        Button(self.master, text='Choose Color',
               command=lambda: self.choose_color(x, y)).grid(row=3, column=4)
        self.color_demo = Label(self.master, text='Color Preview', bd=2, relief='solid')
        self.color_demo.grid(row=3, column=5, columnspan=2)

        self.fill = IntVar()
        self.fill.trace('w', self.row_specify)
        Radiobutton(self.master, text='Fill plot with rows',
                    variable=self.fill, value=1).grid(row=4, column=0, columnspan=2)
        Radiobutton(self.master, text='Specify row count',
                    variable=self.fill, value=0).grid(row=4, column=2, columnspan=2)
        self.row_count_label = Label(self.master, text='Enter desired number of rows:')
        self.row_count = IntVar()
        self.row_count_entry = Entry(self.master, validate='key',
                                     vcmd=(self.master.register(validate_int), "%P"),
                                     textvariable=self.row_count, width=3)

        Button(self.master, text='Close', command=lambda: self.destroy(0, 0)).grid(row=5, column=4)
        Button(self.master, text='Visual Edit', command=lambda: self.destroy(1, 1)).grid(row=5, column=3)
        Button(self.master, text='Plant Crop', command=lambda: self.destroy(1, 0)).grid(row=5, column=1)

        if crop:
            params = crop.planting_params
            self.crop_spacing.set(params.crop_spacing)
            self.row_spacing.set(params.row_spacing)
            self.x_offset.set(params.x_offset)
            self.y_offset.set(params.y_offset)
            self.planting_year.set(crop.plant_year)
            if params.repeat:
                self.fill.set(0)
            else:
                self.fill.set(1)
            self.row_count.set(params.repeat)
            self.color = crop.color
            self.color_demo.config(bg=self.color)
        else:
            if unit == 'm':
                convert = 1
            else:
                convert = 3.28
            self.crop_spacing.set(plant.max_radius * 2 * convert)
            self.row_spacing.set(plant.max_radius * 2 * convert)
            self.x_offset.set(plant.max_radius * convert)
            self.y_offset.set(plant.max_radius * convert)
            self.planting_year.set(year)
            self.row_count.set(0)
            self.fill.set(1)
            self.color = '#ffffff'

        self.crop_spacing_entry.focus_force()

    def row_specify(self, *args):
        self.master.update_idletasks()
        if self.fill.get():
            self.row_count.set(0)
            self.row_count_label.grid_forget()
            self.row_count_entry.grid_forget()
        else:
            self.row_count.set(1)
            self.row_count_label.grid(row=4, column=4, columnspan=2, sticky=E)
            self.row_count_entry.grid(row=4, column=6)
            self.row_count_entry.focus_force()

    def choose_color(self, x, y):
        root3 = Toplevel(self.master)
        root3.overrideredirect(1)
        root3.attributes('-topmost', True)
        root3.grab_set()
        self.color = color_window.Color_Selection(root3, self.color, x, y).wait()
        if max(int(self.color[1:3], 16), int(self.color[3:5], 16)) < 128:
            text_color = 'white'
        else:
            text_color = 'black'
        self.color_demo.config(bg=self.color, fg=text_color)
        self.master.overrideredirect(1)
        self.master.attributes('-topmost', True)
        self.master.grab_set()

    def destroy(self, boolean, visual):
        self.visual = visual
        if boolean:
            if self.crop_spacing.get() == 0 or self.row_spacing.get() == 0:
                self.instructions.set('Plant Spacing and Row Spacing must be greater than zero')
                return
            self.planting_params = Planting_Params(self.crop_spacing.get(), self.row_spacing.get(),
                                                   self.x_offset.get(), self.y_offset.get(),
                                                   self.row_count.get(), self.plot_x, self.plot_y)
            self.plant_year = self.planting_year.get()
        else:
            self.planting_params = None
            self.plant_year = None
        self.master.destroy()

    def wait(self):
        self.master.wait_window()
        return (self.planting_params, self.plant_year, self.color, self.visual)


class Delete_Crop():
    def __init__(self, master, name, color, x, y):
        self.master = master
        self.master.geometry('+%d+%d' % (x, y))
        self.master.config(borderwidth=3, relief=RAISED)
        Label(self.master, text="Press 'Confirm' to delete:").pack()
        Label(self.master, text=name, bg=color).pack(fill=X)
        Button(self.master, text='Confirm', command=lambda: self.destroy(1)).pack(side=RIGHT)
        Button(self.master, text='Cancel', command=lambda: self.destroy(0)).pack(side=LEFT)

    def destroy(self, boolean):
        self.delete = boolean
        self.master.destroy()

    def wait(self):
        self.master.wait_window()
        return self.delete
