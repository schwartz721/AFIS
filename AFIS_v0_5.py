from tkinter import *
import sim_class
import home_windows
import sim_windows
import crop_windows
import plant_classes
import pickle


class Application():
    def __init__(self, master):
        self.master = master
        self.window_w = self.master.winfo_width()
        self.window_h = self.master.winfo_height()
        self.setup_home()

    # Setup for the home screen of the application
    def setup_home(self):
        self.home_frame = Frame(self.master, background='pale green')
        self.home_frame.pack(expand=1, fill=BOTH)
        Label(self.master, text='AgroForestry Intercropping Simulator',
              font=('Courier', 50), bg='pale green').place(relx=.5, rely=.25, anchor=CENTER)
        center_screen = Frame(self.home_frame, bg='pale green')
        center_screen.place(relx=.5, rely=.5, anchor=CENTER)
        Button(center_screen, text='New Simulation', command=lambda: self.setup_sim(None)).pack()
        Button(center_screen, text='Load Simulation',
               command=lambda: self.open_window_home('load')).pack()
        Button(center_screen, text='Manage Plant Profiles',
               command=lambda: self.open_window_home('manage plants')).pack()
        Button(center_screen, text='Quit Application', command=lambda: self.quit()).pack()

    # Functions used by the home screen
    def open_window_home(self, window):
        root2 = Toplevel(self.master)
        root2.overrideredirect(1)
        root2.attributes('-topmost', True)
        root2.grab_set()

        if window == 'load':
            sim = home_windows.Load(root2, self.window_w, self.window_h).wait()
            if type(sim).__name__ == 'Simulation':
                self.setup_sim(sim)
            elif type(sim).__name__ == 'str':
                root2 = Toplevel(self.master)
                root2.overrideredirect(1)
                root2.attributes('-topmost', True)
                root2.grab_set()
                home_windows.Delete_Savefile(root2, sim, self.window_w, self.window_h)
        elif window == 'manage plants':
            with open('plant_dicts_v0_5', 'rb') as load_file:
                plant_dicts = pickle.load(load_file)
            if len(plant_dicts['long']) - 2:
                long_state = 'normal'
            else:
                long_state = 'disabled'
            if len(plant_dicts['short']) - 2:
                short_state = 'normal'
            else:
                short_state = 'disabled'
            action, cycle, unit = home_windows.Manage_Plants(root2, self.window_w, self.window_h,
                                                             long_state, short_state).wait()
            if action:
                self.open_window_plant_specs(action, cycle, unit)
        elif window == 'delete savefile':
            home_windows.Delete_Savefile(root2, savefile, self.window_w, self.window_h)

    def quit(self):
        self.master.destroy()

    # Setup for the simulation screen
    def setup_sim(self, sim):
        self.sim = sim
        self.home_frame.destroy()
        self.sim_frame = Frame(self.master)
        self.sim_frame.pack(expand=1, fill=BOTH)

        top_bar = Frame(self.sim_frame, bg='gray70')
        top_bar.pack(fill=X, side=TOP)
        top_left_bar = Frame(top_bar, bg='gray70')
        top_left_bar.pack(side=LEFT, pady=(0, 5))
        top_right_bar = Frame(top_bar, bg='gray70')
        top_right_bar.pack(side=RIGHT, pady=(0, 5))
        top_rest_bar = Frame(top_bar, bg='gray70')
        top_rest_bar.pack(side=RIGHT, fill=BOTH, expand=1)
        top_center_bar = Frame(top_rest_bar, bg='gray70')
        top_center_bar.pack(pady=(0, 5))

        Button(top_left_bar, text='Quit to Main Menu', highlightbackground='gray70',
               command=lambda: self.open_window_sim('home')).pack(side=LEFT)
        Button(top_left_bar, text='Save Simulation', highlightbackground='gray70',
               command=lambda: self.open_window_sim('save')).pack(side=LEFT)
        Button(top_right_bar, text='Resize Plot', highlightbackground='gray70',
               command=lambda: self.open_window_sim('set dims')).pack(side=RIGHT)
        self.dim_text = StringVar()
        self.dim_text.set('Dimensions: 0 x 0 ')
        Label(top_right_bar, bd=0, textvariable=self.dim_text).pack(side=RIGHT)

        Button(top_center_bar, highlightbackground='gray70', text='Next Year',
               command=lambda: self.change_year(1)).pack(side=RIGHT)
        self.b_prev_year = Button(top_center_bar, state='disabled', highlightbackground='gray70',
                                  text='Previous Year', command=lambda: self.change_year(-1))
        self.b_prev_year.pack(side=LEFT)
        Button(top_center_bar, highlightbackground='gray70', text='Next Season',
               command=lambda: self.change_year(0.5)).pack(side=RIGHT)
        self.b_prev_season = Button(top_center_bar, state='disabled', highlightbackground='gray70',
                                    text='Previous Season', command=lambda: self.change_year(-0.5))
        self.b_prev_season.pack(side=LEFT)

        self.season = StringVar()
        self.season.set('Planting')
        Label(top_center_bar, bd=0, textvariable=self.season).pack(side=RIGHT)
        Label(top_center_bar, bd=0, text='Season:').pack(side=RIGHT)
        Label(top_center_bar, bd=0, text='Year:').pack(side=LEFT)
        self.year = DoubleVar()
        self.year.set(0)
        self.year.trace('w', self.display_year)
        self.year_rounded = IntVar()
        Label(top_center_bar, bd=0, textvariable=self.year_rounded).pack(side=LEFT)

        self.side_bar = Frame(self.sim_frame, bg='black')
        self.side_bar.pack(fill=Y, side=LEFT)
        side_top = Frame(self.side_bar, bg='black', bd=3)
        side_top.pack(side=TOP)
        side_bottom = Frame(self.side_bar, bg='black', bd=3)
        side_bottom.pack(side=BOTTOM, padx=20, fill=BOTH)
        self.side_mid = Frame(self.side_bar, bg='black', bd=3)
        self.side_mid.pack(side=TOP, fill=BOTH)

        Button(side_top, highlightbackground='black', text='Add Long-Cycle Crop',
               command=lambda: self.open_window_plant_specs('new crop', 'long', self.sim.unit)).pack()
        Button(side_top, highlightbackground='black', text='Add Short-Cycle Crop',
               command=lambda: self.open_window_plant_specs('new crop', 'short', self.sim.unit)).pack()
        Label(side_bottom, bg='black', fg='gray70', bd=0, text='AFIS version 0.5.0\n'
              'Andrew Schwartz\nCreated 2019').pack(side=BOTTOM)

        instruction_bar = Frame(self.sim_frame, bg='black')
        instruction_bar.pack(fill=X, side=TOP)
        self.instructions = StringVar()
        Label(instruction_bar, textvariable=self.instructions, bg='black', fg='white').pack()

        visual = Frame(self.sim_frame)
        visual.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(visual, bg='pale green', highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.bind('<Key>', self.keypress)
        self.master.update_idletasks()
        self.canvas_h = self.canvas.winfo_height()
        self.canvas_w = self.canvas.winfo_width()

        if self.sim:
            x = str(round(self.sim.x_dim, 2))
            y = str(round(self.sim.y_dim, 2))
            unit = self.sim.unit
            self.dim_text.set('Dimensions: %s %s x %s %s ' % (x, unit, y, unit))
            self.draw_sim()
            self.draw_sidebar()
        else:
            self.sim = sim_class.Simulation()
            self.open_window_sim('set dims')

    # Functions used by the simulation screen
    def open_window_sim(self, window):
        root2 = Toplevel(self.master)
        root2.overrideredirect(1)
        root2.attributes('-topmost', True)
        root2.grab_set()
        x = self.window_w - self.canvas_w + 10
        y = self.window_h - self.canvas_h + 10

        if window == 'home':
            go_home = sim_windows.Quit_To_Menu(root2, x, y).wait()
            if go_home:
                self.sim_frame.destroy()
                self.setup_home()
        elif window == 'save':
            sim_windows.Save_Sim(root2, self.sim, x, y)
        elif window == 'set dims':
            try:
                dims = (self.sim.x_dim, self.sim.y_dim, self.sim.unit)
            except AttributeError:
                dims = None
            x_dim, y_dim, unit = sim_windows.Dimensions(root2, dims, x, y).wait()
            self.sim.resize(x_dim, y_dim, unit)
            x = str(round(x_dim, 2))
            y = str(round(y_dim, 2))
            self.dim_text.set('Dimensions: %s %s x %s %s ' % (x, unit, y, unit))
            for crop in self.sim.long_crop_dict.values():
                crop.planting_params.position_crop(self.sim.x_dim, self.sim.y_dim)
            for crop in self.sim.short_crop_dict.values():
                crop.planting_params.position_crop(self.sim.x_dim, self.sim.y_dim)
            self.draw_sim()

    def change_year(self, delta):
        self.year.set(self.year.get() + delta)
        if self.year.get() < 1:
            self.b_prev_year.config(state='disabled')
        else:
            self.b_prev_year.config(state='normal')
        if self.year.get() < 0.5:
            self.b_prev_season.config(state='disabled')
        else:
            self.b_prev_season.config(state='normal')
        self.draw_sim()

    def display_year(self, *args):
        self.year_rounded.set(int(self.year.get()))
        season_dict = {0: 'Planting', 0.5: 'Harvest'}
        self.season.set(season_dict[self.year.get() % 1])

    def draw_sim(self, *args):
        year = self.year.get()
        margin = 10  # gutter between canvas edge and plot edge

        # establishes the scale that the plot and crops will be drawn to fit in the canvas
        h_ratio = self.sim.y_dim / (self.canvas_h - margin * 2)
        w_ratio = self.sim.x_dim / (self.canvas_w - margin * 2)
        if h_ratio > w_ratio:
            plot_h = self.canvas_h - margin * 2
            scale = plot_h / self.sim.y_dim
            plot_w = self.sim.x_dim * scale
            y1 = margin
            y2 = y1 + plot_h
            x1 = (self.canvas_w - plot_w) / 2
            x2 = x1 + plot_w
        else:
            plot_w = self.canvas_w - margin * 2
            scale = plot_w / self.sim.x_dim
            plot_h = self.sim.y_dim * scale
            x1 = margin
            x2 = x1 + plot_w
            y1 = (self.canvas_h - plot_h) / 2
            y2 = y1 + plot_h
        self.plot_corners = (x1, y1, x2, y2)
        self.scale = scale

        # clears canvas, then draws the plot
        self.canvas.delete(ALL)
        self.plot = self.canvas.create_rectangle(x1, y1, x2, y2, fill='bisque2', outline='bisque3',
                                                 width=4)

        # sorts the list of long crops by radius, from larger to smaller
        sorted_crop_list = []
        for crop in self.sim.long_crop_dict.values():
            if year >= crop.plant_year:
                height, radius = crop.size(year)
                sorted_crop_list.append((crop, radius))
        for crop in self.sim.short_crop_dict.values():
            if int(year) == crop.plant_year:
                height, radius = crop.size(year)
                sorted_crop_list.append((crop, radius))
        sorted_crop_list.sort(key=lambda x: x[1], reverse=True)
        coord_list = []  # a list of corner coords and color for every plant. used to find overlaps
        overlaps = []  # a list of corner coords and colors of overlapping areas

        # places and draws each plant
        for crop, radius in sorted_crop_list:
            radius *= scale
            for center in crop.planting_params.crop_locations:
                x, y = center
                x *= scale
                y *= scale
                # corner coords are the corner of the plot + scaled center coord +- scaled radius
                x1_new = x1 + x - radius
                y1_new = y1 + y - radius
                x2_new = x1 + x + radius
                y2_new = y1 + y + radius
                color_new = crop.color
                self.canvas.create_rectangle(x1_new, y1_new, x2_new, y2_new,
                                             fill=color_new)

                # finds overlapping areas
                for coord in coord_list:
                    x1_old, x2_old, y1_old, y2_old, color_old = coord
                    cond1 = x1_old <= x1_new <= x2_old
                    cond2 = y1_old <= y1_new <= y2_old
                    cond3 = x1_old <= x2_new <= x2_old
                    cond4 = y1_old <= y2_new <= y2_old
                    if (cond1 or cond3) and (cond2 or cond4):
                        cond_as_index = (cond1, cond2, cond3, cond4)
                        corners = ((x1_old, x1_new), (y1_old, y1_new), (x2_old, x2_new),
                                   (y2_old, y2_new))
                        specs = []
                        for i, corner in zip(cond_as_index, corners):
                            specs.append(corner[i])
                        specs += [color_new, color_old]
                        overlaps.append(specs)

                # new coords are added to coord_list after overlaps are found,
                # to avoid finding overlaps with itself
                coord_list.append((x1_new, x2_new, y1_new, y2_new, color_new))

        # draws overlapping areas
        for specs in overlaps:
            x1, y1, x2, y2, color1, color2 = specs
            r1, g1, b1 = self.canvas.winfo_rgb(color1)
            r2, g2, b2 = self.canvas.winfo_rgb(color2)
            r3 = (r1 + r2) // 512
            g3 = (g1 + g2) // 512
            b3 = (b1 + b2) // 512
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='#%02x%02x%02x' % (r3, g3, b3))

    def add_to_sidebar(self, key):
        if key[0] == 'L':
            d = self.sim.long_crop_dict
        else:
            d = self.sim.short_crop_dict
        crop = d[key]
        self.sim.frame_list.append(sim_class.Frame_Info(crop, key))
        self.draw_sidebar()

    def draw_sidebar(self):
        self.side_mid.destroy()
        self.side_mid = Frame(self.side_bar, bg='black', bd=3)
        self.side_mid.pack(side=TOP, fill=BOTH)
        for i in range(len(self.sim.frame_list)):
            crop = self.sim.frame_list[i].crop
            frame = Frame(self.side_mid, bg=crop.color, bd=2)
            frame.pack(side=TOP, fill=X)
            if max(int(crop.color[1:3], 16), int(crop.color[3:5], 16)) < 128:
                text_color = 'white'
            else:
                text_color = 'black'
            Label(frame, text=crop.plant.name, bg=crop.color, fg=text_color, bd=0).pack()
            Button(frame, text='Edit', highlightbackground=crop.color,
                   command=lambda i=i: self.open_window_crop_specs(i, 'edit crop')).pack(side=RIGHT)
            Button(frame, text='Delete', highlightbackground=crop.color,
                   command=lambda i=i: self.open_window_crop_specs(i, 'delete')).pack(side=LEFT)
            Button(frame, text='Visual Edit', highlightbackground=crop.color,
                   command=lambda i=i: self.visual_edit(i)).pack()

    def open_window_plant_specs(self, action, cycle, unit):
        root2 = Toplevel(self.master)
        root2.overrideredirect(1)
        root2.attributes('-topmost', True)
        root2.grab_set()
        if 'crop' in action:
            x = self.window_w - self.canvas_w + 10
            y = self.window_h - self.canvas_h + 10
        else:
            x = self.window_w / 2
            y = self.window_h / 2
        plant, unit = crop_windows.Growth_Parameters(root2, action, cycle, unit, x, y).wait()
        if action == 'new crop' and plant:
            self.open_window_crop_specs(plant, 'edit crop')

    def open_window_crop_specs(self, index_or_plant, window):
        root2 = Toplevel(self.master)
        root2.overrideredirect(1)
        root2.attributes('-topmost', True)
        root2.grab_set()
        x = self.window_w - self.canvas_w + 10
        y = self.window_h - self.canvas_h + 10
        if isinstance(index_or_plant, int):
            index = index_or_plant
            key = self.sim.frame_list[index].key
            if key[0] == 'L':
                d = self.sim.long_crop_dict
            else:
                d = self.sim.short_crop_dict
            crop = self.sim.frame_list[index].crop
            plant = crop.plant
            name = plant.name
            color = crop.color
        else:
            plant = index_or_plant
            crop = None
        if window == 'edit crop':
            unit = self.sim.unit
            year = self.year_rounded.get()
            plot_x = self.sim.x_dim
            plot_y = self.sim.y_dim
            planting_params, plant_year, color, visual =\
                crop_windows.Planting_Parameters(root2, plant, unit, crop, year, x, y,
                                                 plot_x, plot_y).wait()
            if planting_params and not visual:
                try:
                    del d[key]
                    del self.sim.frame_list[index]
                except UnboundLocalError:
                    pass
                key = self.sim.add_crop(plant, planting_params, plant_year, color)
                self.add_to_sidebar(key)
                self.draw_sim()
            if planting_params and visual:
                try:
                    del d[key]
                    del self.sim.frame_list[index]
                    key = self.sim.add_crop(plant, planting_params, plant_year, color)
                    self.add_to_sidebar(key)
                    self.visual_edit(len(self.sim.frame_list) - 1)
                except UnboundLocalError:
                    self.visual_edit(plant_classes.Crop(plant, planting_params, plant_year, color))
        elif window == 'delete':
            if crop_windows.Delete_Crop(root2, name, color, x, y).wait():
                del self.sim.frame_list[index]
                del d[key]
                self.draw_sim()
                self.draw_sidebar()

    def visual_edit(self, index_or_crop):
        if isinstance(index_or_crop, int):
            self.index_in_progress = index_or_crop
            self.crop_in_progress = self.sim.frame_list[self.index_in_progress].crop
        else:
            self.crop_in_progress = index_or_crop
        self.draw_visual_edit(self.crop_in_progress)
        self.instructions.set('Use the arrow keys to position and crop and WASD to change the '
                              'spacing. Press Enter to accept the placement, or Esc to cancel.')
        self.toggle_buttons(self.sim_frame, 'disabled')
        self.canvas.focus_force()

    def draw_visual_edit(self, crop):
        try:
            for oval in self.in_progress_ovals:
                self.canvas.delete(oval)
        except AttributeError:
            pass
        plot_x1, plot_y1 = self.plot_corners[:2]
        radius = crop.plant.max_radius * self.scale
        self.in_progress_ovals = []
        for center in crop.planting_params.crop_locations:
            x, y = center
            x *= self.scale
            y *= self.scale
            # corner coords are the corner of the plot + scaled center coord +- scaled radius
            x1 = plot_x1 + x - radius
            y1 = plot_y1 + y - radius
            x2 = plot_x1 + x + radius
            y2 = plot_y1 + y + radius
            oval = self.canvas.create_oval(x1, y1, x2, y2, fill=crop.color)
            self.in_progress_ovals.append(oval)

    def toggle_buttons(self, widget, state):
        for child in widget.winfo_children():
            try:
                if 'button' in str(child):
                    child.config(state=state)
            except TclError:
                pass
            self.toggle_buttons(child, state)

    def keypress(self, event):
        try:
            crop = self.crop_in_progress
            x = self.sim.x_dim
            y = self.sim.y_dim
            if event.char == '\uf700':  # up arrow
                crop.planting_params.y_offset = max(crop.planting_params.y_offset - crop.plant.max_radius, 0)
                crop.planting_params.position_crop(x, y)
                self.draw_visual_edit(crop)
            elif event.char == '\uf701':  # down arrow
                crop.planting_params.y_offset = min(crop.planting_params.y_offset + crop.plant.max_radius, y)
                crop.planting_params.position_crop(x, y)
                self.draw_visual_edit(crop)
            elif event.char == '\uf702':  # left arrow
                crop.planting_params.x_offset = max(crop.planting_params.x_offset - 1, 0)
                crop.planting_params.position_crop(x, y)
                self.draw_visual_edit(crop)
            elif event.char == '\uf703':  # right arrow
                crop.planting_params.x_offset = min(crop.planting_params.x_offset + 1, x)
                crop.planting_params.position_crop(x, y)
                self.draw_visual_edit(crop)
            elif event.char == 'w':
                crop.planting_params.crop_spacing += 0.1
                crop.planting_params.position_crop(x, y)
                self.draw_visual_edit(crop)
            elif event.char == 'a':
                crop.planting_params.row_spacing = max(crop.planting_params.row_spacing - 0.1,
                                                       crop.plant.max_radius * 2)
                crop.planting_params.position_crop(x, y)
                self.draw_visual_edit(crop)
            elif event.char == 's':
                crop.planting_params.crop_spacing = max(crop.planting_params.crop_spacing - 0.1,
                                                        crop.plant.max_radius * 2)
                crop.planting_params.position_crop(x, y)
                self.draw_visual_edit(crop)
            elif event.char == 'd':
                crop.planting_params.row_spacing += 0.1
                crop.planting_params.position_crop(x, y)
                self.draw_visual_edit(crop)
            elif event.char == '\r':  # return
                self.toggle_buttons(self.sim_frame, 'normal')
                crop = self.crop_in_progress
                try:
                    del self.index_in_progress
                    self.draw_sidebar()
                except AttributeError:
                    key = self.sim.add_crop(crop.plant, crop.planting_params, crop.plant_year,
                                            crop.color)
                    self.add_to_sidebar(key)
                self.change_year(0)  # this makes sure the states of the prev_ buttons are correct
                self.instructions.set('')
                del self.in_progress_ovals
                del self.crop_in_progress
            elif event.char == '\x1b':  # escape
                self.toggle_buttons(self.sim_frame, 'normal')
                for oval in self.in_progress_ovals:
                    self.canvas.delete(oval)
                self.instructions.set('')
                del self.in_progress_ovals
                del self.crop_in_progress
                try:
                    del self.index_in_progress
                except AttributeError:
                    pass
        except AttributeError:
            pass


root = Tk()
root.attributes('-fullscreen', True)
Application(root)
root.mainloop()
